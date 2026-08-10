from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database.connection import Base

class Category(Base):
    __tablename__ = "categories"

    # Using a string ID (e.g., 'shirt', 'jeans') makes lookups easier and readable
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # Relationships
    mappings = relationship("SizeMapping", back_populates="category")
