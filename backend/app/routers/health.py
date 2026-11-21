import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.database import get_db, active_db_engine
from backend.app.config import settings
from backend.app.models.entities import Patient, Hospital, MedicalRecord, BedAllocation

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint validating database connectivity, latency, and core table counts."""
    t0 = time.perf_counter()
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
        error = None
    except Exception as e:
        db_ok = False
        error = str(e)
    t1 = time.perf_counter()
    latency_ms = round((t1 - t0) * 1000, 2)

    patients_count = db.query(Patient).count() if db_ok else 0
    hospitals_count = db.query(Hospital).count() if db_ok else 0
    records_count = db.query(MedicalRecord).count() if db_ok else 0
    beds_count = db.query(BedAllocation).count() if db_ok else 0

    return {
        "status": "healthy" if db_ok else "unhealthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": {
            "engine": active_db_engine,
            "connected": db_ok,
            "latency_ms": latency_ms,
            "error": error,
            "counts": {
                "patients": patients_count,
                "hospitals": hospitals_count,
                "records": records_count,
                "beds": beds_count
            }
        }
    }
