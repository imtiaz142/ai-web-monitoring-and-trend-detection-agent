from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Text, DateTime, JSON
from app.database import Base


class AIInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    generated_at = Column(DateTime, default=datetime.utcnow)
    insight_type = Column(String(50))
    title = Column(String)
    content = Column(Text)
    top_trends = Column(JSON)
    model_used = Column(String(100), default="llama3")
