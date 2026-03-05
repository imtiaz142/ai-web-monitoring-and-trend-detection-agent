import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.api.router import master_router
from app.services.scheduler import start_scheduler, scheduler
from app.services.ai_analyst import check_ollama_available
from app.services.rss_fetcher import run_scrape_cycle
from app.services.trend_analyzer import run_trend_analysis

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def _initial_scrape_and_analyze():
    """Run first scrape + trend analysis in background."""
    try:
        await run_scrape_cycle()
        logger.info("First scrape done, running trend analysis...")
        await run_trend_analysis()
        logger.info("Initial trend analysis complete")
    except Exception as e:
        logger.error(f"Initial scrape/analyze failed: {e}", exc_info=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    logger.info("Database ready at trendagent.db")

    ollama_ok = await check_ollama_available()
    if ollama_ok:
        logger.info(f"Ollama online - using {settings.OLLAMA_MODEL}")
    else:
        logger.warning("Ollama offline - AI insights disabled (app still works)")

    # Start scheduler inside the running event loop
    start_scheduler()

    # Trigger first scrape + trend analysis in background
    logger.info("First scrape started...")
    asyncio.create_task(_initial_scrape_and_analyze())

    yield

    # Shutdown
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")


app = FastAPI(
    title="AI Trend Detection Agent",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(master_router)
