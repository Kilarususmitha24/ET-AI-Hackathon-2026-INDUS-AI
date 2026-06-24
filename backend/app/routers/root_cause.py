from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models import User
from app.schemas import RootCauseRequest, RootCauseResponse, Citation
from app.services.rag import analyze_root_cause

router = APIRouter(prefix="/root-cause", tags=["Root Cause Analysis"])


@router.post("/analyze", response_model=RootCauseResponse)
def root_cause_analysis(
    payload: RootCauseRequest,
    current_user: User = Depends(get_current_user),
):
    result = analyze_root_cause(
        payload.incident_description,
        payload.equipment,
        payload.symptoms,
    )
    return RootCauseResponse(
        probable_causes=result["probable_causes"],
        contributing_factors=result["contributing_factors"],
        recommended_actions=result["recommended_actions"],
        related_documents=[Citation(**c) for c in result["related_documents"]],
        analysis_summary=result["analysis_summary"],
    )
