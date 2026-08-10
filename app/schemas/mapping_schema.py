from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MappingBase(BaseModel):
    source_brand: str
    source_size: str
    target_brand: str
    target_size: str
    category: str
    confidence_score: int
    reason: Optional[str] = None

class MappingCreate(MappingBase):
    pass

class MappingResponse(MappingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
