from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User, ComplianceRecord
from app.schemas import ComplianceRecordResponse

router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.get("/", response_model=list[ComplianceRecordResponse])
def list_compliance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(ComplianceRecord).order_by(ComplianceRecord.last_checked.desc()).all()


@router.get("/summary")
def compliance_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = db.query(ComplianceRecord).all()
    total = len(records) or 1
    compliant = sum(1 for r in records if r.status == "compliant")
    partial = sum(1 for r in records if r.status == "partial")
    gaps = sum(1 for r in records if r.status == "gap")
    score = round((compliant + partial * 0.5) / total * 100, 1)

    by_regulation = {}
    for r in records:
        if r.regulation not in by_regulation:
            by_regulation[r.regulation] = {"compliant": 0, "partial": 0, "gap": 0}
        by_regulation[r.regulation][r.status] = by_regulation[r.regulation].get(r.status, 0) + 1

    return {
        "compliance_score": score,
        "total_checks": total,
        "compliant": compliant,
        "partial": partial,
        "gaps": gaps,
        "by_regulation": by_regulation,
        "critical_gaps": [r for r in records if r.status == "gap" and r.severity == "high"],
    }
