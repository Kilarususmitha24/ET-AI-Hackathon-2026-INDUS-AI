import json
import re

from app.services.gemini_service import GeminiService
from app.services.faiss_store import get_faiss_store
from app.config import get_settings

settings = get_settings()

COMPLIANCE_RULES = [
    {"regulation": "OSHA 1910.147", "requirement": "Lockout/Tagout procedures must be documented and accessible", "keywords": ["lockout", "tagout", "loto", "energy isolation"]},
    {"regulation": "ISO 45001", "requirement": "Occupational health and safety management system documentation", "keywords": ["safety", "hazard", "risk assessment", "ppe"]},
    {"regulation": "API 510", "requirement": "Pressure vessel inspection and maintenance records", "keywords": ["pressure vessel", "inspection", "vessel", "api 510"]},
    {"regulation": "EPA 40 CFR", "requirement": "Environmental compliance and emissions monitoring", "keywords": ["emission", "environmental", "spill", "waste"]},
    {"regulation": "NFPA 70E", "requirement": "Electrical safety and arc flash protection", "keywords": ["electrical", "arc flash", "voltage", "grounding"]},
    {"regulation": "ASME B31.3", "requirement": "Process piping design and maintenance standards", "keywords": ["piping", "pipeline", "process pipe", "flange"]},
]


def analyze_compliance(text: str, document_id: int, category: str) -> list[dict]:
    text_lower = text.lower()
    results = []

    for rule in COMPLIANCE_RULES:
        matches = [kw for kw in rule["keywords"] if kw in text_lower]
        if matches or category == "compliance":
            status = "compliant" if len(matches) >= 2 else ("partial" if matches else "gap")
            severity = "low" if status == "compliant" else ("medium" if status == "partial" else "high")
            results.append({
                "regulation": rule["regulation"],
                "requirement": rule["requirement"],
                "status": status,
                "severity": severity,
                "document_id": document_id,
                "evidence": f"Keywords found: {', '.join(matches)}" if matches else "No direct evidence found",
                "gap_description": "" if status == "compliant" else f"Insufficient documentation for {rule['regulation']}",
            })

    return results[:6]
