from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Integer, Float, DateTime, JSON
from app.database import Base


class Trend(Base):
    __tablename__ = "trends"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    keyword = Column(String(200), unique=True, nullable=False)
    first_seen_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow)
    mention_count = Column(Integer, default=1)
    velocity_score = Column(Float, default=0.0)
    trend_status = Column(String(20), default="emerging")
    related_keywords = Column(JSON)
    article_count = Column(Integer, default=0)
