from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article


async def url_exists(session: AsyncSession, url: str) -> bool:
    result = await session.execute(select(Article.id).where(Article.url == url))
    return result.scalar_one_or_none() is not None
