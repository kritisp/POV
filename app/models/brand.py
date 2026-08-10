from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    country = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    source_mappings = relationship("SizeMapping", foreign_keys="[SizeMapping.source_brand_id]", back_populates="source_brand")
    target_mappings = relationship("SizeMapping", foreign_keys="[SizeMapping.target_brand_id]", back_populates="target_brand")
