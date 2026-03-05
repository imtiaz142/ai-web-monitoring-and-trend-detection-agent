from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.trend import Trend
from app.models.trend_snapshot import TrendSnapshot
from app.models.article import Article
from app.schemas.trend import TrendResponse, TrendSnapshotResponse
from app.schemas.article import ArticleResponse

router = APIRouter(prefix="/api/trends", tags=["trends"])


def _api_response(data, count=None):
    from datetime import datetime
    resp = {"success": True, "data": data, "timestamp": datetime.utcnow().isoformat()}
    if count is not None:
        resp["count"] = count
    return resp


@router.get("")
async def get_all_trends(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Trend).order_by(Trend.velocity_score.desc())
    )
    trends = result.scalars().all()
    data = [TrendResponse.model_validate(t).model_dump() for t in trends]
    return _api_response(data, count=len(data))


@router.get("/emerging")
async def get_emerging_trends(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Trend)
        .where(Trend.trend_status.in_(["emerging", "rising"]))
        .order_by(Trend.velocity_score.desc())
    )
    trends = result.scalars().all()
    data = [TrendResponse.model_validate(t).model_dump() for t in trends]
    return _api_response(data, count=len(data))


@router.get("/{trend_id}")
async def get_trend(trend_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Trend).where(Trend.id == trend_id))
    trend = result.scalar_one_or_none()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    trend_data = TrendResponse.model_validate(trend).model_dump()

    # Find articles mentioning this keyword
    keyword = trend.keyword
    articles_result = await session.execute(
        select(Article)
        .where(Article.title.ilike(f"%{keyword}%"))
        .order_by(Article.scraped_at.desc())
        .limit(20)
    )
    articles = articles_result.scalars().all()
    trend_data["articles"] = [ArticleResponse.model_validate(a).model_dump() for a in articles]

    return _api_response(trend_data)


@router.get("/{trend_id}/history")
async def get_trend_history(trend_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Trend).where(Trend.id == trend_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Trend not found")

    result = await session.execute(
        select(TrendSnapshot)
        .where(TrendSnapshot.trend_id == trend_id)
        .order_by(TrendSnapshot.snapshot_at.asc())
    )
    snapshots = result.scalars().all()
    data = [TrendSnapshotResponse.model_validate(s).model_dump() for s in snapshots]
    return _api_response(data, count=len(data))
