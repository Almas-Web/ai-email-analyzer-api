from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="emails")
    analysis = relationship("EmailAnalysis", backref="email", uselist=False, cascade="all, delete-orphan")

class EmailAnalysis(Base):
    __tablename__ = "email_analyses"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"), unique=True, nullable=False)
    category = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    intent = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    key_information = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())