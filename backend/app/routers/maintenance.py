from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User, MaintenanceRecord
from app.schemas import MaintenanceRecordResponse

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


@router.get("/", response_model=list[MaintenanceRecordResponse])
def list_maintenance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(MaintenanceRecord).order_by(MaintenanceRecord.created_at.desc()).all()


@router.get("/summary")
def maintenance_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = db.query(MaintenanceRecord).all()
    high = sum(1 for r in records if r.priority == "high" and r.status == "open")
    medium = sum(1 for r in records if r.priority == "medium" and r.status == "open")
    low = sum(1 for r in records if r.priority == "low" and r.status == "open")
    total_downtime = sum(r.estimated_downtime_hours for r in records if r.status == "open")

    return {
        "open_high_priority": high,
        "open_medium_priority": medium,
        "open_low_priority": low,
        "total_open": high + medium + low,
        "estimated_downtime_hours": round(total_downtime, 1),
        "recommendations": records[:10],
    }
