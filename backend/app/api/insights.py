from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.insight import AIInsight
from app.schemas.insight import InsightResponse
from app.services.scheduler import run_ai_insight

router = APIRouter(prefix="/api/insights", tags=["insights"])


def _api_response(data, count=None):
    from datetime import datetime
    resp = {"success": True, "data": data, "timestamp": datetime.utcnow().isoformat()}
    if count is not None:
        resp["count"] = count
    return resp


@router.get("")
async def get_all_insights(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(AIInsight).order_by(AIInsight.generated_at.desc())
    )
    insights = result.scalars().all()
    data = [InsightResponse.model_validate(i).model_dump() for i in insights]
    return _api_response(data, count=len(data))


@router.get("/latest")
async def get_latest_insight(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(AIInsight).order_by(AIInsight.generated_at.desc()).limit(1)
    )
    insight = result.scalar_one_or_none()
    if not insight:
        return _api_response(None)
    data = InsightResponse.model_validate(insight).model_dump()
    return _api_response(data)


@router.post("/generate")
async def trigger_insight_generation():
    try:
        await run_ai_insight()
        return _api_response({"message": "Insight generation triggered"})
    except Exception as e:
        return {"success": False, "error": str(e)}
