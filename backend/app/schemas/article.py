from datetime import datetime
from pydantic import BaseModel


class ArticleResponse(BaseModel):
    id: str
    url: str
    title: str
    content: str | None = None
    summary: str | None = None
    source_name: str | None = None
    published_at: datetime | None = None
    scraped_at: datetime | None = None
    keywords: list[str] | None = None
    is_processed: bool = False

    class Config:
        from_attributes = True
