from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base

class SizeMapping(Base):
    __tablename__ = "size_mappings"

    id = Column(Integer, primary_key=True, index=True)
    source_brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    source_size = Column(String, nullable=False)
    target_brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    target_size = Column(String, nullable=False)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    confidence_score = Column(Integer, nullable=False)  # 0 to 100
    reason = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    source_brand = relationship("Brand", foreign_keys=[source_brand_id], back_populates="source_mappings")
    target_brand = relationship("Brand", foreign_keys=[target_brand_id], back_populates="target_mappings")
    category = relationship("Category", back_populates="mappings")
