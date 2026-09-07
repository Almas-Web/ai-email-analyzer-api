from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.email import Email, EmailAnalysis as EmailAnalysisModel

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    # Total emails for the user
    total_emails = db.query(Email).filter(Email.user_id == user_id).count()

    # Analyzed emails count
    analyzed_emails = db.query(EmailAnalysisModel).join(Email).filter(Email.user_id == user_id).count()

    # High priority count
    high_priority = db.query(EmailAnalysisModel).join(Email).filter(Email.user_id == user_id, EmailAnalysisModel.priority == "high").count()

    # Urgent count
    urgent = db.query(EmailAnalysisModel).join(Email).filter(Email.user_id == user_id, EmailAnalysisModel.priority == "urgent").count()

    # Negative sentiment count
    negative = db.query(EmailAnalysisModel).join(Email).filter(Email.user_id == user_id, EmailAnalysisModel.sentiment == "negative").count()

    # Category counts
    billing = db.query(EmailAnalysisModel).join(Email).filter(Email.user_id == user_id, EmailAnalysisModel.category == "billing").count()
    technical_support = db.query(EmailAnalysisModel).join(Email).filter(Email.user_id == user_id, EmailAnalysisModel.category == "technical_support").count()

    return {
        "total_emails": total_emails,
        "analyzed_emails": analyzed_emails,
        "high_priority": high_priority,
        "urgent": urgent,
        "negative": negative,
        "billing": billing,
        "technical_support": technical_support
    }