from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.feedback import Feedback
from app.schemas.feedback_schema import FeedbackCreate, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("", response_model=FeedbackResponse)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Record user feedback for a recommendation.
    """
    new_feedback = Feedback(
        source_brand=feedback.source_brand,
        source_size=feedback.source_size,
        target_brand=feedback.target_brand,
        recommended_size=feedback.recommended_size,
        actual_size=feedback.actual_size,
        result=feedback.result,
        feedback_reason=feedback.feedback_reason
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback
