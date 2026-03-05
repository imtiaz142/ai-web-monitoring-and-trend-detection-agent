from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.ai_settings import AISettings
from app.services.ai_analyst import check_ai_available

router = APIRouter(prefix="/api/ai-settings", tags=["ai-settings"])

PROVIDERS = {
    "ollama": {"label": "Ollama (Local)", "default_model": "llama3", "needs_key": False},
    "openai": {"label": "OpenAI", "default_model": "gpt-4o-mini", "needs_key": True},
    "gemini": {"label": "Google Gemini", "default_model": "gemini-2.0-flash", "needs_key": True},
    "anthropic": {"label": "Anthropic Claude", "default_model": "claude-sonnet-4-20250514", "needs_key": True},
}


class AISettingsUpdate(BaseModel):
    provider: str
    api_key: str | None = None
    model_name: str | None = None
    base_url: str | None = None


@router.get("")
async def get_ai_settings(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(AISettings).where(AISettings.is_active == True).limit(1)  # noqa: E712
    )
    current = result.scalar_one_or_none()

    if current:
        data = {
            "provider": current.provider,
            "api_key_set": bool(current.api_key),
            "api_key_preview": f"...{current.api_key[-4:]}" if current.api_key else None,
            "model_name": current.model_name,
            "base_url": current.base_url,
        }
    else:
        data = {
            "provider": "ollama",
            "api_key_set": False,
            "api_key_preview": None,
            "model_name": "llama3",
            "base_url": None,
        }

    status = await check_ai_available()

    return {
        "success": True,
        "data": {**data, "status": status},
        "providers": PROVIDERS,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.post("")
async def save_ai_settings(body: AISettingsUpdate, session: AsyncSession = Depends(get_session)):
    if body.provider not in PROVIDERS:
        return {"success": False, "error": f"Unknown provider: {body.provider}"}

    provider_info = PROVIDERS[body.provider]
    if provider_info["needs_key"] and not body.api_key:
        return {"success": False, "error": f"{provider_info['label']} requires an API key"}

    model_name = body.model_name or provider_info["default_model"]

    # Deactivate all existing settings
    await session.execute(
        update(AISettings).values(is_active=False)
    )

    # Create new active setting
    new_setting = AISettings(
        provider=body.provider,
        api_key=body.api_key,
        model_name=model_name,
        base_url=body.base_url,
        is_active=True,
        updated_at=datetime.utcnow(),
    )
    session.add(new_setting)
    await session.commit()

    status = await check_ai_available()

    return {
        "success": True,
        "data": {
            "provider": body.provider,
            "model_name": model_name,
            "status": status,
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/test")
async def test_ai_connection():
    """Quick test to verify the AI provider is working."""
    status = await check_ai_available()
    return {"success": True, "data": status, "timestamp": datetime.utcnow().isoformat()}
