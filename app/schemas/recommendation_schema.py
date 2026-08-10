from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    source_brand: str
    source_size: str
    target_brand: str
    category: str

class RecommendationResponse(BaseModel):
    recommended_size: str
    confidence: int
    reason: str

class MeasurementRequest(BaseModel):
    category: str
    target_brand: str
    chest: int | None = None
    waist: int | None = None

