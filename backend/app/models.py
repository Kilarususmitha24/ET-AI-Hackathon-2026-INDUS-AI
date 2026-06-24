from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="operator")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    documents = relationship("Document", back_populates="owner")
    chat_sessions = relationship("ChatSession", back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    filename = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_type = Column(String(50), nullable=False)
    doc_category = Column(String(100), default="general")
    status = Column(String(50), default="pending")
    page_count = Column(Integer, default=0)
    chunk_count = Column(Integer, default=0)
    ocr_applied = Column(Boolean, default=False)
    extracted_text_preview = Column(Text, default="")
    metadata_json = Column(JSON, default=dict)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="documents")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), default="New Conversation")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    citations = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


class ComplianceRecord(Base):
    __tablename__ = "compliance_records"

    id = Column(Integer, primary_key=True, index=True)
    regulation = Column(String(500), nullable=False)
    requirement = Column(Text, nullable=False)
    status = Column(String(50), default="pending")
    severity = Column(String(50), default="medium")
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    evidence = Column(Text, default="")
    gap_description = Column(Text, default="")
    last_checked = Column(DateTime, default=datetime.utcnow)


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    equipment = Column(String(500), nullable=False)
    recommendation = Column(Text, nullable=False)
    priority = Column(String(50), default="medium")
    confidence = Column(Float, default=0.0)
    source_document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    estimated_downtime_hours = Column(Float, default=0.0)
    next_due_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="open")
    created_at = Column(DateTime, default=datetime.utcnow)


class IncidentRecord(Base):
    __tablename__ = "incident_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    equipment = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), default="medium")
    root_cause = Column(Text, default="")
    corrective_action = Column(Text, default="")
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    occurred_at = Column(DateTime, default=datetime.utcnow)
