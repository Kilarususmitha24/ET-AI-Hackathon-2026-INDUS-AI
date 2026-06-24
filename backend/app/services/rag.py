import json
import re

from app.services.gemini_service import GeminiService
from app.services.faiss_store import get_faiss_store
from app.config import get_settings

settings = get_settings()


def rag_query(question: str) -> dict:
    faiss_store = get_faiss_store()
    gemini = GeminiService()

    retrieved = faiss_store.search(question, top_k=settings.top_k_retrieval)

    if not retrieved:
        return {
            "answer": "No relevant documents found in the knowledge base. Please upload industrial documents first.",
            "citations": [],
        }

    context_parts = []
    citations = []
    for i, chunk in enumerate(retrieved):
        context_parts.append(f"[Source {i+1}] {chunk['text']}")
        citations.append({
            "document_id": chunk["document_id"],
            "document_title": chunk["document_title"],
            "chunk_text": chunk["text"][:300],
            "page": chunk.get("page"),
            "score": chunk.get("score", 0.0),
        })

    context = "\n\n".join(context_parts)
    system = (
        "You are INDUS-AI, an industrial knowledge intelligence assistant. "
        "Answer based ONLY on the provided context from industrial documents. "
        "Be precise, technical, and cite source numbers. "
        "If information is insufficient, say so clearly."
    )
    prompt = f"""Context from industrial knowledge base:
{context}

Question: {question}

Provide a detailed, professional answer with references to source numbers [Source N]."""

    answer = gemini.generate(prompt, system)
    return {"answer": answer, "citations": citations}


def analyze_root_cause(incident_description: str, equipment: str, symptoms: str) -> dict:
    faiss_store = get_faiss_store()
    gemini = GeminiService()

    query = f"{incident_description} {equipment} {symptoms}"
    retrieved = faiss_store.search(query, top_k=5)

    context = "\n".join(c["text"] for c in retrieved) if retrieved else "No historical documents available."

    prompt = f"""Analyze this industrial incident for root cause.

Equipment: {equipment or 'Not specified'}
Incident: {incident_description}
Symptoms: {symptoms or 'Not specified'}

Historical context:
{context}

Return ONLY valid JSON with keys:
probable_causes (list of 3 strings),
contributing_factors (list of 3 strings),
recommended_actions (list of 4 strings),
analysis_summary (string)"""

    response = gemini.generate(prompt, "You are an expert industrial reliability engineer.")

    try:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            data = json.loads(match.group())
        else:
            raise ValueError("No JSON found")
    except (json.JSONDecodeError, ValueError):
        data = {
            "probable_causes": ["Mechanical wear", "Process deviation", "Human error"],
            "contributing_factors": ["Inadequate maintenance", "Training gaps", "Environmental conditions"],
            "recommended_actions": ["Conduct 5-Why analysis", "Inspect equipment", "Review procedures", "Update training"],
            "analysis_summary": response[:500],
        }

    citations = [
        {
            "document_id": c["document_id"],
            "document_title": c["document_title"],
            "chunk_text": c["text"][:300],
            "page": c.get("page"),
            "score": c.get("score", 0.0),
        }
        for c in retrieved
    ]

    return {
        "probable_causes": data.get("probable_causes", []),
        "contributing_factors": data.get("contributing_factors", []),
        "recommended_actions": data.get("recommended_actions", []),
        "related_documents": citations,
        "analysis_summary": data.get("analysis_summary", ""),
    }
