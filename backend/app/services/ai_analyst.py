import json
import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


async def check_ollama_available() -> bool:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=3.0)
            return r.status_code == 200
    except Exception:
        return False


async def generate_insight(top_trends: list[dict], recent_articles: list[dict]) -> dict | None:
    if not await check_ollama_available():
        return None

    trend_names = [t["keyword"] for t in top_trends[:10]]
    article_titles = [a["title"] for a in recent_articles[:20]]

    prompt = f"""You are an AI technology trend analyst. Analyze the following trending topics and recent article headlines, then respond ONLY with a valid JSON object (no explanation, no markdown, no code fences).

Trending keywords right now: {', '.join(trend_names)}

Recent article headlines:
{chr(10).join(f'- {t}' for t in article_titles)}

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

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3},
                },
            )
            raw = response.json().get("response", "")
            clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
            return json.loads(clean)
    except Exception as e:
        logger.warning(f"Ollama insight generation failed: {e}")
        return None


async def summarize_article(title: str, content: str) -> str:
    if not await check_ollama_available():
        return ""
    prompt = f"Summarize this article in one sentence:\nTitle: {title}\nContent: {content[:500]}"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False},
            )
            return response.json().get("response", "").strip()
    except Exception:
        return ""
