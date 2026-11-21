import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
from backend.app.services.seed import seed_database_if_empty

# Routers
from backend.app.routers import (
    auth, patients, records, labs, beds, queue,
    appointments, hospitals_doctors, analytics, audit,
    sql_workbench, notifications, backup, health
)

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("medilink")

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Create tables and seed data on load
try:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database_if_empty(db)
    db.close()
    logger.info("MediLink database verified and seeded successfully.")
except Exception as e:
    logger.error(f"Error initializing database: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Aadhaar-Based Unified Medical Records & Hospital Management System"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers under /api
api_prefix = settings.API_V1_STR
app.include_router(auth.router, prefix=api_prefix)
app.include_router(patients.router, prefix=api_prefix)
app.include_router(records.router, prefix=api_prefix)
app.include_router(labs.router, prefix=api_prefix)
app.include_router(beds.router, prefix=api_prefix)
app.include_router(queue.router, prefix=api_prefix)
app.include_router(appointments.router, prefix=api_prefix)
app.include_router(hospitals_doctors.router, prefix=api_prefix)
app.include_router(analytics.router, prefix=api_prefix)
app.include_router(audit.router, prefix=api_prefix)
app.include_router(sql_workbench.router, prefix=api_prefix)
app.include_router(notifications.router, prefix=api_prefix)
app.include_router(backup.router, prefix=api_prefix)
app.include_router(health.router, prefix=api_prefix)

# Uploads and Static files
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Frontend index.html route
@app.get("/")
def read_root():
    index_file = BASE_DIR / "index.html"
    if not index_file.exists():
        index_file = BASE_DIR / "Hospital_Management-master" / "index.html"
    return FileResponse(index_file)

@app.get("/favicon.ico", include_in_schema=False)
def serve_favicon():
    svg_icon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">⚕</text></svg>'
    return Response(content=svg_icon, media_type="image/svg+xml")

# Catch-all for assets if needed
@app.get("/{file_name}")
def serve_static_root_files(file_name: str):
    f = BASE_DIR / file_name
    if f.exists() and f.is_file():
        return FileResponse(f)
    return JSONResponse(status_code=404, content={"detail": f"File '{file_name}' not found"})
