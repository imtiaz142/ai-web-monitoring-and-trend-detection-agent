import json
import logging

import httpx
from sqlalchemy import select

from app.config import settings
from app.database import AsyncSessionLocal
from app.models.ai_settings import AISettings

logger = logging.getLogger(__name__)

INSIGHT_PROMPT_TEMPLATE = """You are an AI technology trend analyst. Analyze the following trending topics and recent article headlines, then respond ONLY with a valid JSON object (no explanation, no markdown, no code fences).

Trending keywords right now: {trend_names}

Recent article headlines:
{article_lines}

Respond with this exact JSON structure:
{{
  "title": "AI & Tech Trend Briefing",
  "executive_summary": "2-3 sentences summarizing what is happening in AI & tech right now",
  "key_trends": [
    {{
      "trend": "trend name",
      "why_it_matters": "1-2 sentence explanation",
      "momentum": "accelerating"
    }}
  ],
  "market_signals": ["signal 1", "signal 2", "signal 3"],
  "emerging_opportunities": ["opportunity 1", "opportunity 2"],
  "confidence_score": 0.85
}}"""


async def get_active_ai_settings() -> dict:
    """Get the active AI provider settings from DB, falling back to Ollama defaults."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(AISettings).where(AISettings.is_active == True).limit(1)  # noqa: E712
            )
            ai = result.scalar_one_or_none()
            if ai:
                return {
                    "provider": ai.provider,
                    "api_key": ai.api_key,
                    "model_name": ai.model_name,
                    "base_url": ai.base_url,
                }
    except Exception:
        pass

    return {
        "provider": "ollama",
        "api_key": None,
        "model_name": settings.OLLAMA_MODEL,
        "base_url": settings.OLLAMA_BASE_URL,
    }


async def check_ollama_available() -> bool:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=3.0)
            return r.status_code == 200
    except Exception:
        return False


async def check_ai_available() -> dict:
    """Check which AI provider is configured and if it's reachable."""
    ai = await get_active_ai_settings()
    provider = ai["provider"]

    if provider == "ollama":
        ok = await check_ollama_available()
        return {"provider": "ollama", "status": "online" if ok else "offline", "model": ai["model_name"]}

    # For cloud APIs, just check if API key is set
    if ai["api_key"]:
        return {"provider": provider, "status": "configured", "model": ai["model_name"]}

    return {"provider": provider, "status": "no_api_key", "model": ai["model_name"]}


def _parse_json_response(raw: str) -> dict | None:
    clean = raw.strip()
    # Strip markdown code fences
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[-1] if "\n" in clean else clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    clean = clean.strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        # Try to find JSON object in the response
        start = clean.find("{")
        end = clean.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(clean[start:end])
            except json.JSONDecodeError:
                pass
    return None


async def _call_ollama(prompt: str, ai: dict) -> str | None:
    base_url = ai["base_url"] or settings.OLLAMA_BASE_URL
    if not await check_ollama_available():
        return None
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{base_url}/api/generate",
                json={
                    "model": ai["model_name"],
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3},
                },
            )
            return response.json().get("response", "")
    except Exception as e:
        logger.warning(f"Ollama call failed: {e}")
        return None


async def _call_openai(prompt: str, ai: dict) -> str | None:
    if not ai["api_key"]:
        logger.warning("OpenAI API key not configured")
        return None
    base_url = ai["base_url"] or "https://api.openai.com/v1"
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{base_url}/chat/completions",
                headers={"Authorization": f"Bearer {ai['api_key']}", "Content-Type": "application/json"},
                json={
                    "model": ai["model_name"],
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                },
            )
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.warning(f"OpenAI call failed: {e}")
        return None


async def _call_gemini(prompt: str, ai: dict) -> str | None:
    if not ai["api_key"]:
        logger.warning("Gemini API key not configured")
        return None
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{ai['model_name']}:generateContent",
                params={"key": ai["api_key"]},
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.3},
                },
            )
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        logger.warning(f"Gemini call failed: {e}")
        return None


async def _call_anthropic(prompt: str, ai: dict) -> str | None:
    if not ai["api_key"]:
        logger.warning("Anthropic API key not configured")
        return None
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ai["api_key"],
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": ai["model_name"],
                    "max_tokens": 2048,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                },
            )
            data = response.json()
            return data["content"][0]["text"]
    except Exception as e:
        logger.warning(f"Anthropic call failed: {e}")
        return None


PROVIDER_CALLERS = {
    "ollama": _call_ollama,
    "openai": _call_openai,
    "gemini": _call_gemini,
    "anthropic": _call_anthropic,
}


async def call_ai(prompt: str) -> str | None:
    """Route prompt to the active AI provider."""
    ai = await get_active_ai_settings()
    caller = PROVIDER_CALLERS.get(ai["provider"])
    if not caller:
        logger.error(f"Unknown AI provider: {ai['provider']}")
        return None
    return await caller(prompt, ai)


async def generate_insight(top_trends: list[dict], recent_articles: list[dict]) -> dict | None:
    trend_names = [t["keyword"] for t in top_trends[:10]]
    article_titles = [a["title"] for a in recent_articles[:20]]

    prompt = INSIGHT_PROMPT_TEMPLATE.format(
        trend_names=", ".join(trend_names),
        article_lines="\n".join(f"- {t}" for t in article_titles),
    )

    raw = await call_ai(prompt)
    if not raw:
        return None

    result = _parse_json_response(raw)
    if not result:
        logger.warning(f"Failed to parse AI response as JSON: {raw[:200]}")
    return result


async def summarize_article(title: str, content: str) -> str:
    prompt = f"Summarize this article in one sentence:\nTitle: {title}\nContent: {content[:500]}"
    result = await call_ai(prompt)
    return result.strip() if result else ""
