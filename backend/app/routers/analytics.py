from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.auth import get_current_user
from app.database import get_db
from app.models import User, Document, ComplianceRecord, MaintenanceRecord, IncidentRecord, ChatMessage
from app.schemas import AnalyticsResponse
from app.services.faiss_store import get_faiss_store
from app.services.neo4j_service import get_neo4j_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=AnalyticsResponse)
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    docs = db.query(Document).filter(Document.user_id == current_user.id).all()
    total_docs = len(docs)
    processed = sum(1 for d in docs if d.status == "processed")
    total_chunks = sum(d.chunk_count for d in docs)

    compliance_records = db.query(ComplianceRecord).all()
    total_cr = len(compliance_records) or 1
    compliant = sum(1 for r in compliance_records if r.status == "compliant")
    partial = sum(1 for r in compliance_records if r.status == "partial")
    compliance_score = round((compliant + partial * 0.5) / total_cr * 100, 1)

    open_maint = db.query(MaintenanceRecord).filter(MaintenanceRecord.status == "open").count()
    critical = db.query(IncidentRecord).filter(IncidentRecord.severity == "high").count()

    graph = get_neo4j_service().get_graph()
    kg_nodes = len(graph.get("nodes", []))

    recent_docs = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .order_by(Document.created_at.desc())
        .limit(5)
        .all()
    )
    recent_activity = [
        {
            "type": "document",
            "title": d.title,
            "status": d.status,
            "timestamp": d.created_at.isoformat(),
        }
        for d in recent_docs
    ]

    return AnalyticsResponse(
        total_documents=total_docs,
        processed_documents=processed,
        total_chunks=total_chunks or get_faiss_store().total_chunks,
        compliance_score=compliance_score,
        open_maintenance=open_maint,
        critical_incidents=critical,
        knowledge_graph_nodes=kg_nodes,
        recent_activity=recent_activity,
    )
