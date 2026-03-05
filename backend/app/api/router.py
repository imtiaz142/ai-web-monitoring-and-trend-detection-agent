import time
from datetime import datetime

from fastapi import APIRouter

from app.api.trends import router as trends_router
from app.api.articles import router as articles_router
from app.api.insights import router as insights_router
from app.api.stats import router as stats_router
from app.api.ai_settings import router as ai_settings_router
from app.services.rss_fetcher import run_scrape_cycle
from app.services.trend_analyzer import run_trend_analysis
from app.services.scheduler import get_scheduler_jobs

master_router = APIRouter()

master_router.include_router(trends_router)
master_router.include_router(articles_router)
master_router.include_router(insights_router)
master_router.include_router(stats_router)
master_router.include_router(ai_settings_router)


@master_router.post("/api/scrape/trigger", tags=["scrape"])
async def trigger_scrape():
    start = time.time()
    try:
        articles_added = await run_scrape_cycle()
        analysis_stats = await run_trend_analysis()
        duration = round(time.time() - start, 2)
        return {
            "success": True,
            "data": {
                "articles_added": articles_added,
                "trends_created": analysis_stats.get("trends_created", 0),
                "trends_updated": analysis_stats.get("trends_updated", 0),
                "duration_seconds": duration,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@master_router.get("/api/debug/run-analysis", tags=["debug"])
async def debug_run_analysis():
    try:
        stats = await run_trend_analysis()
        return {
            "success": True,
            "data": stats,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {"success": False, "error": str(e), "timestamp": datetime.utcnow().isoformat()}


@master_router.get("/api/debug/scheduler-jobs", tags=["debug"])
async def debug_scheduler_jobs():
    jobs = get_scheduler_jobs()
    return {
        "success": True,
        "data": jobs,
        "count": len(jobs),
        "timestamp": datetime.utcnow().isoformat(),
    }
