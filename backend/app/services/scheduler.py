import json
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, delete

from app.config import settings
from app.database import AsyncSessionLocal
from app.models.article import Article
from app.models.trend import Trend
from app.models.insight import AIInsight
from app.services.rss_fetcher import run_scrape_cycle
from app.services.trend_analyzer import run_trend_analysis
from app.services.ai_analyst import generate_insight

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def run_ai_insight():
    logger.info("Generating AI insight via Ollama...")
    async with AsyncSessionLocal() as session:
        trends_result = await session.execute(
            select(Trend).order_by(Trend.velocity_score.desc()).limit(10)
        )
        trends = trends_result.scalars().all()

        articles_result = await session.execute(
            select(Article).order_by(Article.scraped_at.desc()).limit(20)
        )
        articles = articles_result.scalars().all()

        if not trends:
            logger.info("No trends available for insight generation")
            return

        top_trends = [{"keyword": t.keyword, "velocity_score": t.velocity_score} for t in trends]
        recent_articles = [{"title": a.title} for a in articles]

        insight_data = await generate_insight(top_trends, recent_articles)
        if not insight_data:
            logger.warning("Ollama unavailable or insight generation failed")
            return

        insight = AIInsight(
            insight_type="daily_summary",
            title=insight_data.get("title", "AI & Tech Trend Briefing"),
            content=json.dumps(insight_data),
            top_trends=[t.keyword for t in trends[:5]],
            model_used=settings.OLLAMA_MODEL,
            generated_at=datetime.utcnow(),
        )
        session.add(insight)
        await session.commit()
        logger.info(f"Insight generated ({settings.OLLAMA_MODEL})")


async def cleanup_old_articles():
    cutoff = datetime.utcnow() - timedelta(days=30)
    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(Article).where(Article.scraped_at < cutoff)
        )
        await session.commit()
    logger.info("Old articles cleaned up")


async def run_scrape_and_analyze():
    """Combined job: scrape then analyze."""
    await run_scrape_cycle()
    await run_trend_analysis()


def start_scheduler():
    """Start the scheduler with all jobs. Must be called when event loop is running."""
    if scheduler.running:
        logger.info("Scheduler already running")
        return

    scheduler.add_job(
        run_scrape_and_analyze,
        "interval",
        minutes=settings.SCRAPE_INTERVAL_MINUTES,
        id="scraper",
        replace_existing=True,
    )
    scheduler.add_job(
        run_trend_analysis,
        "interval",
        minutes=settings.TREND_ANALYSIS_INTERVAL_MINUTES,
        id="trend_analyzer",
        replace_existing=True,
    )
    scheduler.add_job(
        run_ai_insight,
        "cron",
        hour=settings.AI_INSIGHT_HOUR_UTC,
        minute=0,
        id="daily_insight",
        replace_existing=True,
    )
    scheduler.add_job(
        cleanup_old_articles,
        "cron",
        day_of_week="sun",
        hour=2,
        id="cleanup",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started with %d jobs", len(scheduler.get_jobs()))
    for job in scheduler.get_jobs():
        logger.info(f"  Job '{job.id}' next run: {job.next_run_time}")


def get_scheduler_jobs() -> list[dict]:
    """Return info about all scheduled jobs."""
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger),
        })
    return jobs
