from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.recommendation_schema import RecommendationRequest, RecommendationResponse, MeasurementRequest
from app.services.recommendation_service import get_recommendation, get_measurement_recommendation

router = APIRouter(tags=["Recommendation"])

@router.post("/recommend-size", response_model=RecommendationResponse)
def recommend_size(request: RecommendationRequest, db: Session = Depends(get_db)):
    """
    Get a size recommendation based on the source brand and size.
    """
    return get_recommendation(db, request)

@router.post("/recommend-measurements", response_model=RecommendationResponse)
def recommend_measurements(request: MeasurementRequest, db: Session = Depends(get_db)):
    """
    Get a size recommendation based on actual body measurements.
    """
    return get_measurement_recommendation(db, request)
