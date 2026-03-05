from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, Boolean
from app.database import Base


class AISettings(Base):
    __tablename__ = "ai_settings"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    provider = Column(String(50), default="ollama")  # ollama, openai, gemini, anthropic
    api_key = Column(String, nullable=True)
    model_name = Column(String(200), default="llama3")
    base_url = Column(String, nullable=True)  # custom endpoint for ollama or openai-compatible
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow)
