import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import engine, Base, SessionLocal
from app.models import User, IncidentRecord
from app.auth import get_password_hash, get_user_by_email
from app.routers import auth, documents, chat, knowledge_graph, compliance, maintenance, root_cause, analytics

logging.basicConfig(level=logging.INFO)
settings = get_settings()


def seed_demo_data():
    db = SessionLocal()
    try:
        if not get_user_by_email(db, "demo@indusai.com"):
            demo_user = User(
                email="demo@indusai.com",
                full_name="Kilaru Susmitha",
                hashed_password=get_password_hash("demo123"),
                role="engineer",
            )
            db.add(demo_user)
            db.commit()

        if db.query(IncidentRecord).count() == 0:
            incidents = [
                IncidentRecord(
                    title="Pump P-101 Vibration Alert",
                    equipment="Centrifugal Pump P-101",
                    description="Excessive vibration detected during peak load operation",
                    severity="high",
                    root_cause="Bearing wear due to insufficient lubrication",
                    corrective_action="Replaced bearings and updated lubrication schedule",
                ),
                IncidentRecord(
                    title="Compressor C-204 Overheat",
                    equipment="Air Compressor C-204",
                    description="Thermal sensor triggered shutdown at 95°C",
                    severity="medium",
                    root_cause="Clogged air filter reducing cooling efficiency",
                    corrective_action="Replaced filters and cleaned cooling fins",
                ),
            ]
            db.add_all(incidents)
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.faiss_index_dir).mkdir(parents=True, exist_ok=True)
    seed_demo_data()
    yield


app = FastAPI(
    title="INDUS-AI API",
    description="Unified Asset & Operations Brain - Industrial Knowledge Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(knowledge_graph.router, prefix="/api")
app.include_router(compliance.router, prefix="/api")
app.include_router(maintenance.router, prefix="/api")
app.include_router(root_cause.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "INDUS-AI",
        "version": "1.0.0",
    }
