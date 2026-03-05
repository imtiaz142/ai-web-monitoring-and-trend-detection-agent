from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON
from app.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text)
    summary = Column(Text)
    source_name = Column(String(100))
    published_at = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    keywords = Column(JSON)
    is_processed = Column(Boolean, default=False)
