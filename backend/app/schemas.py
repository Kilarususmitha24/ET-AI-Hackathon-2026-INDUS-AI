from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=6)
    role: str = "operator"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class DocumentResponse(BaseModel):
    id: int
    title: str
    filename: str
    file_type: str
    doc_category: str
    status: str
    page_count: int
    chunk_count: int
    ocr_applied: bool
    extracted_text_preview: str
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChatMessageCreate(BaseModel):
    message: str
    session_id: Optional[int] = None


class Citation(BaseModel):
    document_id: int
    document_title: str
    chunk_text: str
    page: Optional[int] = None
    score: float = 0.0


class ChatMessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    citations: list[Citation] = []
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: list[ChatMessageResponse] = []

    class Config:
        from_attributes = True


class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    properties: dict = {}


class GraphEdge(BaseModel):
    source: str
    target: str
    label: str


class KnowledgeGraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class ComplianceRecordResponse(BaseModel):
    id: int
    regulation: str
    requirement: str
    status: str
    severity: str
    evidence: str
    gap_description: str
    last_checked: datetime

    class Config:
        from_attributes = True


class MaintenanceRecordResponse(BaseModel):
    id: int
    equipment: str
    recommendation: str
    priority: str
    confidence: float
    estimated_downtime_hours: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class RootCauseRequest(BaseModel):
    incident_description: str
    equipment: str = ""
    symptoms: str = ""


class RootCauseResponse(BaseModel):
    probable_causes: list[str]
    contributing_factors: list[str]
    recommended_actions: list[str]
    related_documents: list[Citation]
    analysis_summary: str


class AnalyticsResponse(BaseModel):
    total_documents: int
    processed_documents: int
    total_chunks: int
    compliance_score: float
    open_maintenance: int
    critical_incidents: int
    knowledge_graph_nodes: int
    recent_activity: list[dict]
