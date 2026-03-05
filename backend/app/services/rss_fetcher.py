import asyncio
import logging
from datetime import datetime
from urllib.parse import urlparse

import feedparser
import httpx

from app.config import NEWS_SOURCES, settings
from app.database import AsyncSessionLocal
from app.models.article import Article
from app.utils.text_cleaner import strip_html, clean_title
from app.utils.deduplicator import url_exists

logger = logging.getLogger(__name__)

_domain_last_request: dict[str, float] = {}
RATE_LIMIT_SECONDS = 2.0


async def _rate_limit(url: str):
    domain = urlparse(url).netloc
    now = asyncio.get_event_loop().time()
    last = _domain_last_request.get(domain, 0)
    wait = RATE_LIMIT_SECONDS - (now - last)
    if wait > 0:
        await asyncio.sleep(wait)
    _domain_last_request[domain] = asyncio.get_event_loop().time()


async def fetch_feed(source: dict) -> list[dict]:
    url = source["url"]
    name = source["name"]
    articles = []

    for attempt in range(3):
        try:
            await _rate_limit(url)
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(url, headers={"User-Agent": "TrendAgent/1.0"})
                response.raise_for_status()

            feed = feedparser.parse(response.text)
            for entry in feed.entries[: settings.MAX_ARTICLES_PER_SOURCE]:
                link = getattr(entry, "link", None)
                title = getattr(entry, "title", None)
                if not link or not title:
                    continue

                content_raw = ""
                if hasattr(entry, "content") and entry.content:
                    content_raw = entry.content[0].get("value", "")
                elif hasattr(entry, "summary"):
                    content_raw = entry.summary or ""

                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    try:
                        published = datetime(*entry.published_parsed[:6])
                    except Exception:
                        pass

                cleaned_title = clean_title(title)
                if not cleaned_title or len(cleaned_title) < 5:
                    logger.debug(f"Skipping entry with bad title: '{title}' -> '{cleaned_title}'")
                    continue

                articles.append({
                    "url": link,
                    "title": cleaned_title,
                    "content": strip_html(content_raw),
                    "source_name": name,
                    "published_at": published,
                })
            break
        except Exception as e:
            if attempt < 2:
                wait = 2 ** (attempt + 1)
                logger.warning(f"Retry {attempt+1} for {name}: {e}")
                await asyncio.sleep(wait)
            else:
                logger.error(f"Failed to fetch {name} after 3 attempts: {e}")

    return articles


async def run_scrape_cycle():
    logger.info("Starting scrape cycle...")
    total_new = 0

    for source in NEWS_SOURCES:
        try:
            articles = await fetch_feed(source)
            async with AsyncSessionLocal() as session:
                for art in articles:
                    if await url_exists(session, art["url"]):
                        continue
                    article = Article(
                        url=art["url"],
                        title=art["title"],
                        content=art["content"],
                        source_name=art["source_name"],
                        published_at=art["published_at"],
                        scraped_at=datetime.utcnow(),
                    )
                    session.add(article)
                    total_new += 1
                await session.commit()
            logger.info(f"Scraped {source['name']} ({len(articles)} fetched)")
        except Exception as e:
            logger.error(f"Error scraping {source['name']}: {e}")

    logger.info(f"Scrape cycle complete - {total_new} new articles")
    return total_new
