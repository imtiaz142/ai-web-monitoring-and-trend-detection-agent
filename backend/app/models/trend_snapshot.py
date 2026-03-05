from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from app.database import Base


class TrendSnapshot(Base):
    __tablename__ = "trend_snapshots"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    trend_id = Column(String, ForeignKey("trends.id"))
    snapshot_at = Column(DateTime, default=datetime.utcnow)
    mention_count = Column(Integer)
    velocity_score = Column(Float)
