from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.connection import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    source_brand = Column(String, nullable=False)
    source_size = Column(String, nullable=False)
    target_brand = Column(String, nullable=False)
    recommended_size = Column(String, nullable=False)
    actual_size = Column(String, nullable=True)
    result = Column(String, nullable=False)  # e.g., 'kept', 'returned'
    feedback_reason = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
