import logging
from datetime import datetime, timedelta

import yake
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.article import Article
from app.models.trend import Trend
from app.models.trend_snapshot import TrendSnapshot

logger = logging.getLogger(__name__)

kw_extractor = yake.KeywordExtractor(
    lan="en",
    n=3,
    dedupLim=0.7,
    top=15,
    features=None,
)


def extract_keywords(text: str) -> list[str]:
    if not text or len(text.strip()) < 20:
        return []
    try:
        keywords = kw_extractor.extract_keywords(text)
        results = [kw.lower() for kw, score in keywords if len(kw.split()) >= 2]
        return results
    except Exception as e:
        logger.error(f"YAKE extraction failed: {e}")
        return []


async def run_trend_analysis() -> dict:
    """Run trend analysis. Returns stats dict for debug endpoint."""
    logger.info("Starting trend analysis...")
    stats = {"articles_processed": 0, "trends_created": 0, "trends_updated": 0, "keywords_extracted": 0}

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Article).where(Article.is_processed == False)  # noqa: E712
            )
            articles = result.scalars().all()

            logger.info(f"Found {len(articles)} unprocessed articles")

            if not articles:
                logger.info("No unprocessed articles found")
                return stats

            keyword_counts: dict[str, int] = {}
            keyword_articles: dict[str, int] = {}

            for article in articles:
                text = f"{article.title or ''} {article.content or ''}"
                keywords = extract_keywords(text)

                if keywords:
                    logger.debug(f"Article '{article.title[:50]}' -> {len(keywords)} keywords: {keywords[:5]}")
                else:
                    logger.debug(f"Article '{article.title[:50]}' -> 0 keywords (text len: {len(text)})")

                article.keywords = keywords
                article.is_processed = True
                stats["articles_processed"] += 1

                for kw in set(keywords):
                    keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
                    keyword_articles[kw] = keyword_articles.get(kw, 0) + 1

            stats["keywords_extracted"] = len(keyword_counts)
            logger.info(f"Extracted {len(keyword_counts)} unique keywords from {len(articles)} articles")

            if not keyword_counts:
                logger.warning("No keywords extracted from any article - committing is_processed flags only")
                await session.commit()
                return stats

            now = datetime.utcnow()
            emerging_count = 0

            for keyword, count in keyword_counts.items():
                result = await session.execute(
                    select(Trend).where(Trend.keyword == keyword)
                )
                trend = result.scalar_one_or_none()

                if trend:
                    trend.mention_count += count
                    trend.last_seen_at = now
                    trend.article_count += keyword_articles[keyword]
                    stats["trends_updated"] += 1
                else:
                    trend = Trend(
                        keyword=keyword,
                        first_seen_at=now,
                        last_seen_at=now,
                        mention_count=count,
                        article_count=keyword_articles[keyword],
                        trend_status="emerging",
                    )
                    session.add(trend)
                    stats["trends_created"] += 1

                velocity = await _calculate_velocity(session, trend, now)
                trend.velocity_score = velocity

                if velocity >= 3.0:
                    trend.trend_status = "emerging"
                    emerging_count += 1
                elif velocity >= 1.5:
                    trend.trend_status = "rising"
                elif velocity >= 0.5:
                    trend.trend_status = "stable"
                else:
                    trend.trend_status = "declining"

                await session.flush()

                snapshot = TrendSnapshot(
                    trend_id=trend.id,
                    snapshot_at=now,
                    mention_count=trend.mention_count,
                    velocity_score=velocity,
                )
                session.add(snapshot)

            await session.commit()
            logger.info(
                f"Trend analysis complete - {stats['trends_created']} created, "
                f"{stats['trends_updated']} updated, {emerging_count} emerging"
            )

    except Exception as e:
        logger.error(f"Trend analysis FAILED: {e}", exc_info=True)
        raise

    return stats


async def _calculate_velocity(
    session: AsyncSession, trend: Trend, now: datetime
) -> float:
    two_hours_ago = now - timedelta(hours=2)
    four_hours_ago = now - timedelta(hours=4)

    result = await session.execute(
        select(func.count()).select_from(TrendSnapshot).where(
            TrendSnapshot.trend_id == trend.id,
            TrendSnapshot.snapshot_at >= two_hours_ago,
        )
    )
    recent = result.scalar() or 0

    result = await session.execute(
        select(func.count()).select_from(TrendSnapshot).where(
            TrendSnapshot.trend_id == trend.id,
            TrendSnapshot.snapshot_at >= four_hours_ago,
            TrendSnapshot.snapshot_at < two_hours_ago,
        )
    )
    previous = result.scalar() or 0

    # For new trends with no snapshots, use mention count as signal
    if recent == 0 and previous == 0:
        return min(float(trend.mention_count), 5.0)

    return recent / max(previous, 1)
