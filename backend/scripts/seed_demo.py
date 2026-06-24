"""Seed demo data by uploading sample documents and processing them."""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine, Base
from app.models import Document, User
from app.auth import get_user_by_email
from app.services.ingestion import process_document

SAMPLE_DIR = Path(__file__).parent.parent.parent / "sample_documents"

CATEGORIES = {
    "pump_p101_maintenance_manual.txt": "maintenance",
    "safety_manual_process_area.txt": "safety",
    "compressor_inspection_report.txt": "incident",
    "boiler_operating_procedure.txt": "procedure",
    "incident_report_conveyor.txt": "incident",
}


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        user = get_user_by_email(db, "demo@indusai.com")
        if not user:
            print("Demo user not found. Start the server first to create demo user.")
            return

        existing = {d.filename for d in db.query(Document).filter(Document.user_id == user.id).all()}

        for filename, category in CATEGORIES.items():
            if filename in existing:
                print(f"Skipping {filename} (already exists)")
                continue

            filepath = SAMPLE_DIR / filename
            if not filepath.exists():
                print(f"File not found: {filepath}")
                continue

            upload_dir = Path("./uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)
            dest = upload_dir / filename
            dest.write_text(filepath.read_text(encoding="utf-8"), encoding="utf-8")

            doc = Document(
                title=filename.replace("_", " ").replace(".txt", "").title(),
                filename=filename,
                file_path=str(dest),
                file_type="txt",
                doc_category=category,
                user_id=user.id,
                status="pending",
            )
            db.add(doc)
            db.commit()
            db.refresh(doc)

            print(f"Processing {filename}...")
            process_document(db, doc)
            print(f"  -> {doc.status}, {doc.chunk_count} chunks")

        print("\nDemo data seeded successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
