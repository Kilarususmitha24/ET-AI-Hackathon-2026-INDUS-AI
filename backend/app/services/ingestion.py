import json
import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Document, ComplianceRecord, MaintenanceRecord
from app.services.ocr import extract_document_text
from app.services.faiss_store import get_faiss_store
from app.services.gemini_service import GeminiService
from app.services.neo4j_service import get_neo4j_service
from app.services.compliance_analyzer import analyze_compliance
from app.services.maintenance_engine import generate_maintenance_recommendations

logger = logging.getLogger(__name__)


def process_document(db: Session, document: Document) -> Document:
    document.status = "processing"
    db.commit()

    try:
        text, page_count, ocr_applied = extract_document_text(document.file_path, document.file_type)
        document.page_count = page_count
        document.ocr_applied = ocr_applied
        document.extracted_text_preview = text[:500] + ("..." if len(text) > 500 else "")

        faiss_store = get_faiss_store()
        chunk_count = faiss_store.add_document_chunks(
            document.id,
            document.title,
            text,
            page_count,
        )
        document.chunk_count = chunk_count

        gemini = GeminiService()
        entities = gemini.extract_entities(text)
        document.metadata_json = entities

        neo4j = get_neo4j_service()
        neo4j.add_document_knowledge(
            document.id,
            document.title,
            document.doc_category,
            entities,
        )

        compliance_items = analyze_compliance(text, document.id, document.doc_category)
        for item in compliance_items:
            db.add(ComplianceRecord(**item))

        maintenance_items = generate_maintenance_recommendations(text, document.id, entities)
        for item in maintenance_items:
            db.add(MaintenanceRecord(**item))

        document.status = "processed"
        document.processed_at = datetime.utcnow()
        db.commit()
        db.refresh(document)
        logger.info("Processed document %s: %d chunks", document.id, chunk_count)
    except Exception as e:
        logger.exception("Failed to process document %s", document.id)
        document.status = "failed"
        document.metadata_json = {"error": str(e)}
        db.commit()

    return document
