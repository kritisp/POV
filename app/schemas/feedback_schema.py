from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackBase(BaseModel):
    source_brand: str
    source_size: str
    target_brand: str
    recommended_size: str
    actual_size: Optional[str] = None
    result: str  # e.g., "kept", "returned"
    feedback_reason: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
