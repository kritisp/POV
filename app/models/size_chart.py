from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base

class BrandSizeChart(Base):
    __tablename__ = "brand_size_charts"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    target_size = Column(String, nullable=False)
    
    # Measurements in inches for simplicity in this MVP
    chest_min = Column(Integer, nullable=True)
    chest_max = Column(Integer, nullable=True)
    waist_min = Column(Integer, nullable=True)
    waist_max = Column(Integer, nullable=True)

    brand = relationship("Brand")
    category = relationship("Category")
