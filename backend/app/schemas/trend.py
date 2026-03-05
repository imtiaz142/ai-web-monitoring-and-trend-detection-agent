from datetime import datetime
from pydantic import BaseModel


class TrendResponse(BaseModel):
    id: str
    keyword: str
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    mention_count: int = 0
    velocity_score: float = 0.0
    trend_status: str = "emerging"
    related_keywords: list[str] | None = None
    article_count: int = 0

    class Config:
        from_attributes = True


class TrendSnapshotResponse(BaseModel):
    id: str
    trend_id: str
    snapshot_at: datetime | None = None
    mention_count: int = 0
    velocity_score: float = 0.0

    class Config:
        from_attributes = True
