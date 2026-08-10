from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.brand import Brand
from app.schemas.brand_schema import BrandCreate, BrandResponse

router = APIRouter(prefix="/brands", tags=["Brands"])

@router.post("", response_model=BrandResponse)
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    db_brand = db.query(Brand).filter(Brand.name.ilike(brand.name)).first()
    if db_brand:
        raise HTTPException(status_code=400, detail="Brand already exists")
    
    new_brand = Brand(name=brand.name, country=brand.country)
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return new_brand

@router.get("", response_model=List[BrandResponse])
def get_brands(db: Session = Depends(get_db)):
    brands = db.query(Brand).all()
    return brands
