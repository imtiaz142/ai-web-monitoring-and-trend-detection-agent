from datetime import datetime
from pydantic import BaseModel


class InsightResponse(BaseModel):
    id: str
    generated_at: datetime | None = None
    insight_type: str | None = None
    title: str | None = None
    content: str | None = None
    top_trends: list[str] | None = None
    model_used: str = "llama3"

    class Config:
        from_attributes = True
