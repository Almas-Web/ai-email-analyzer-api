from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.email import Email, EmailAnalysis as EmailAnalysisModel
from app.schemas.email import EmailCreate, EmailResponse
from app.schemas.analysis import EmailAnalysisResponse
from app.services.llm_service import analyze_email_content

router = APIRouter(prefix="/emails", tags=["Emails & Analysis"])

@router.post("", response_model=EmailResponse, status_code=status.HTTP_201_CREATED)
def create_email(email_in: EmailCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_email = Email(
        user_id=current_user.id,
        sender=email_in.sender,
        subject=email_in.subject,
        body=email_in.body
    )
    db.add(new_email)
    db.commit()
    db.refresh(new_email)
    return new_email

@router.get("", response_model=List[EmailResponse])
def get_emails(
    category: Optional[str] = None,
    priority: Optional[str] = None,
    sentiment: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Email).join(EmailAnalysisModel, isouter=True).filter(Email.user_id == current_user.id)
    
    if category:
        query = query.filter(EmailAnalysisModel.category == category)
    if priority:
        query = query.filter(EmailAnalysisModel.priority == priority)
    if sentiment:
        query = query.filter(EmailAnalysisModel.sentiment == sentiment)
        
    return query.all()

@router.get("/{email_id}", response_model=EmailResponse)
def get_email(email_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    email = db.query(Email).filter(Email.id == email_id, Email.user_id == current_user.id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

@router.delete("/{email_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email(email_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    email = db.query(Email).filter(Email.id == email_id, Email.user_id == current_user.id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    db.delete(email)
    db.commit()
    return None

@router.post("/{email_id}/analyze", response_model=EmailAnalysisResponse)
def analyze_email(email_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    email = db.query(Email).filter(Email.id == email_id, Email.user_id == current_user.id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Check if already analyzed
    existing_analysis = db.query(EmailAnalysisModel).filter(EmailAnalysisModel.email_id == email_id).first()
    if existing_analysis:
        return existing_analysis

    # Call LLM Service
    ai_result = analyze_email_content(email.sender, email.subject, email.body)

    # Save to Database
    new_analysis = EmailAnalysisModel(
        email_id=email.id,
        category=ai_result.category,
        priority=ai_result.priority,
        sentiment=ai_result.sentiment,
        intent=ai_result.intent,
        summary=ai_result.summary,
        key_information=ai_result.key_information
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return new_analysis