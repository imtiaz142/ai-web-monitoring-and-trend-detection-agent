from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.article import Article
from app.schemas.article import ArticleResponse

router = APIRouter(prefix="/api/articles", tags=["articles"])


def _api_response(data, count=None):
    from datetime import datetime
    resp = {"success": True, "data": data, "timestamp": datetime.utcnow().isoformat()}
    if count is not None:
        resp["count"] = count
    return resp


@router.get("")
async def get_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    source: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Article).order_by(Article.scraped_at.desc())
    if source:
        query = query.where(Article.source_name == source)

    count_query = select(func.count()).select_from(Article)
    if source:
        count_query = count_query.where(Article.source_name == source)
    total = (await session.execute(count_query)).scalar() or 0

    query = query.offset((page - 1) * limit).limit(limit)
    result = await session.execute(query)
    articles = result.scalars().all()
    data = [ArticleResponse.model_validate(a).model_dump() for a in articles]
    return _api_response(data, count=total)


@router.get("/latest")
async def get_latest_articles(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Article).order_by(Article.scraped_at.desc()).limit(20)
    )
    articles = result.scalars().all()
    data = [ArticleResponse.model_validate(a).model_dump() for a in articles]
    return _api_response(data, count=len(data))
