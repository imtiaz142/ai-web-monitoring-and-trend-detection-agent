from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.article import Article
from app.models.trend import Trend
from app.services.ai_analyst import check_ollama_available

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("")
async def get_stats(session: AsyncSession = Depends(get_session)):
    total_articles = (
        await session.execute(select(func.count()).select_from(Article))
    ).scalar() or 0

    total_trends = (
        await session.execute(select(func.count()).select_from(Trend))
    ).scalar() or 0

    emerging_count = (
        await session.execute(
            select(func.count())
            .select_from(Trend)
            .where(Trend.trend_status.in_(["emerging", "rising"]))
        )
    ).scalar() or 0

    last_scrape_result = await session.execute(
        select(Article.scraped_at).order_by(Article.scraped_at.desc()).limit(1)
    )
    last_scrape = last_scrape_result.scalar_one_or_none()

    ollama_status = await check_ollama_available()

    return {
        "success": True,
        "data": {
            "total_articles": total_articles,
            "total_trends": total_trends,
            "emerging_count": emerging_count,
            "last_scrape_at": last_scrape.isoformat() if last_scrape else None,
            "ollama_status": "online" if ollama_status else "offline",
        },
        "timestamp": datetime.utcnow().isoformat(),
    }
