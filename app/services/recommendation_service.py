from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import or_, and_

from app.models.brand import Brand
from app.models.mapping import SizeMapping
from app.models.size_chart import BrandSizeChart
from app.schemas.recommendation_schema import RecommendationRequest, RecommendationResponse, MeasurementRequest

def get_recommendation(db: Session, request: RecommendationRequest) -> RecommendationResponse:
    source_brand = db.query(Brand).filter(Brand.name.ilike(request.source_brand)).first()
    if not source_brand:
        raise HTTPException(status_code=404, detail=f"Source brand '{request.source_brand}' not found")

    target_brand = db.query(Brand).filter(Brand.name.ilike(request.target_brand)).first()
    if not target_brand:
        raise HTTPException(status_code=404, detail=f"Target brand '{request.target_brand}' not found")

    mapping = db.query(SizeMapping).filter(
        SizeMapping.source_brand_id == source_brand.id,
        SizeMapping.target_brand_id == target_brand.id,
        SizeMapping.source_size == request.source_size.upper(),
        SizeMapping.category_id == request.category.lower()
    ).first()

    if not mapping:
        raise HTTPException(
            status_code=404, 
            detail="No size mapping found for these specifications."
        )

    return RecommendationResponse(
        recommended_size=mapping.target_size,
        confidence=mapping.confidence_score,
        reason=mapping.reason or "No specific reason provided."
    )

def get_measurement_recommendation(db: Session, request: MeasurementRequest) -> RecommendationResponse:
    target_brand = db.query(Brand).filter(Brand.name.ilike(request.target_brand)).first()
    if not target_brand:
        raise HTTPException(status_code=404, detail=f"Target brand '{request.target_brand}' not found")

    # Build the query based on provided measurements
    query = db.query(BrandSizeChart).filter(
        BrandSizeChart.brand_id == target_brand.id,
        BrandSizeChart.category_id == request.category.lower()
    )

    if request.chest:
        query = query.filter(
            or_(
                BrandSizeChart.chest_min == None,
                and_(
                    BrandSizeChart.chest_min <= request.chest,
                    or_(BrandSizeChart.chest_max >= request.chest, BrandSizeChart.chest_max == None)
                )
            )
        )
    if request.waist:
        query = query.filter(
            or_(
                BrandSizeChart.waist_min == None,
                and_(
                    BrandSizeChart.waist_min <= request.waist,
                    or_(BrandSizeChart.waist_max >= request.waist, BrandSizeChart.waist_max == None)
                )
            )
        )

    chart = query.first()

    if not chart:
        raise HTTPException(
            status_code=404, 
            detail="No size found for these body measurements in the selected brand."
        )

    return RecommendationResponse(
        recommended_size=chart.target_size,
        confidence=95,
        reason=f"Calculated directly from {target_brand.name}'s official size charts for your body measurements."
    )
