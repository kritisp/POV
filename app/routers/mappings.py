from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.mapping import SizeMapping
from app.models.brand import Brand
from app.models.category import Category
from app.schemas.mapping_schema import MappingCreate, MappingResponse

router = APIRouter(prefix="/mappings", tags=["Mappings"])

@router.post("", response_model=MappingResponse)
def create_mapping(mapping: MappingCreate, db: Session = Depends(get_db)):
    # 1. Resolve source_brand name to id
    source_brand = db.query(Brand).filter(Brand.name.ilike(mapping.source_brand)).first()
    if not source_brand:
        raise HTTPException(status_code=404, detail=f"Source brand '{mapping.source_brand}' not found")
        
    # 2. Resolve target_brand name to id
    target_brand = db.query(Brand).filter(Brand.name.ilike(mapping.target_brand)).first()
    if not target_brand:
        raise HTTPException(status_code=404, detail=f"Target brand '{mapping.target_brand}' not found")

    # 3. Verify category exists
    category = db.query(Category).filter(Category.id == mapping.category.lower()).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category '{mapping.category}' not found")

    # 4. Check if mapping already exists to prevent duplicates (optional, based on MVP scope)
    existing = db.query(SizeMapping).filter(
        SizeMapping.source_brand_id == source_brand.id,
        SizeMapping.target_brand_id == target_brand.id,
        SizeMapping.source_size == mapping.source_size,
        SizeMapping.category_id == mapping.category.lower()
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="This mapping already exists")

    new_mapping = SizeMapping(
        source_brand_id=source_brand.id,
        source_size=mapping.source_size,
        target_brand_id=target_brand.id,
        target_size=mapping.target_size,
        category_id=mapping.category.lower(),
        confidence_score=mapping.confidence_score,
        reason=mapping.reason
    )
    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)
    
    # Transform response to match the Pydantic schema which expects brand names, not IDs
    return MappingResponse(
        id=new_mapping.id,
        source_brand=source_brand.name,
        source_size=new_mapping.source_size,
        target_brand=target_brand.name,
        target_size=new_mapping.target_size,
        category=new_mapping.category_id,
        confidence_score=new_mapping.confidence_score,
        reason=new_mapping.reason,
        created_at=new_mapping.created_at
    )
