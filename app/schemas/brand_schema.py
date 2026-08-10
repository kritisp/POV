from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BrandBase(BaseModel):
    name: str
    country: Optional[str] = None

class BrandCreate(BrandBase):
    pass

class BrandResponse(BrandBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
