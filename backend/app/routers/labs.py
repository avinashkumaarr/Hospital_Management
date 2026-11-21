import os
import shutil
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.config import settings
from backend.app.models.entities import LabReport, Patient, MedicalRecord
from backend.app.schemas.all_schemas import LabReportCreate, LabReportOut

router = APIRouter(prefix="/labs", tags=["Lab Reports"])

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.get("", response_model=List[LabReportOut])
def list_labs(
    aadhaar: Optional[str] = None,
    test_name: Optional[str] = None,
    is_abnormal: Optional[bool] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(LabReport).join(Patient).outerjoin(MedicalRecord)
    if aadhaar:
        clean = aadhaar.strip()
        query = query.filter(LabReport.aadhaar_number.like(f"%{clean}%"))
    if test_name:
        query = query.filter(LabReport.test_name.ilike(f"%{test_name.strip()}%"))
    if is_abnormal is not None:
        query = query.filter(LabReport.is_abnormal == is_abnormal)
        
    labs = query.order_by(LabReport.report_date.desc()).limit(limit).all()
    results = []
    for l in labs:
        hosp_name = "Central Pathology Lab"
        if l.record and l.record.hospital:
            hosp_name = l.record.hospital.hospital_name
        results.append(LabReportOut(
            report_id=l.report_id,
            record_id=l.record_id,
            aadhaar_number=l.aadhaar_number,
            test_name=l.test_name,
            result=l.result,
            normal_range=l.normal_range,
            unit=l.unit,
            is_abnormal=l.is_abnormal,
            report_date=l.report_date,
            file_path=l.file_path,
            created_at=l.created_at,
            hospital_name=hosp_name
        ))
    return results

@router.post("", response_model=LabReportOut, status_code=status.HTTP_201_CREATED)
def add_lab_report(req: LabReportCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.aadhaar_number == req.aadhaar_number).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient {req.aadhaar_number} not found.")

    new_lab = LabReport(
        record_id=req.record_id,
        aadhaar_number=req.aadhaar_number,
        test_name=req.test_name,
        result=req.result,
        normal_range=req.normal_range,
        unit=req.unit,
        is_abnormal=req.is_abnormal,
        report_date=req.report_date
    )
    db.add(new_lab)
    db.commit()
    db.refresh(new_lab)

    return LabReportOut(
        report_id=new_lab.report_id,
        record_id=new_lab.record_id,
        aadhaar_number=new_lab.aadhaar_number,
        test_name=new_lab.test_name,
        result=new_lab.result,
        normal_range=new_lab.normal_range,
        unit=new_lab.unit,
        is_abnormal=new_lab.is_abnormal,
        report_date=new_lab.report_date,
        file_path=new_lab.file_path,
        created_at=new_lab.created_at,
        hospital_name="Central Diagnostic Pathology"
    )

@router.post("/upload", response_model=LabReportOut)
def upload_lab_pdf(
    aadhaar_number: str = Form(...),
    test_name: str = Form(...),
    result: str = Form(""),
    normal_range: str = Form(""),
    unit: str = Form(""),
    is_abnormal: bool = Form(False),
    report_date: str = Form(...),
    record_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate PDF or image
    filename = file.filename or "unknown.pdf"
    if not filename.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF and standard image files (PNG, JPG) are allowed.")

    patient = db.query(Patient).filter(Patient.aadhaar_number == aadhaar_number).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")

    ext = os.path.splitext(filename)[1]
    safe_filename = f"lab_{uuid.uuid4().hex[:12]}{ext}"
    dest_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    import datetime
    try:
        date_obj = datetime.date.fromisoformat(report_date)
    except Exception:
        date_obj = datetime.date.today()

    new_lab = LabReport(
        record_id=record_id,
        aadhaar_number=aadhaar_number,
        test_name=test_name,
        result=result or f"Digital Report Attachment ({file.filename})",
        normal_range=normal_range,
        unit=unit,
        is_abnormal=is_abnormal,
        report_date=date_obj,
        file_path=safe_filename
    )
    db.add(new_lab)
    db.commit()
    db.refresh(new_lab)

    return LabReportOut(
        report_id=new_lab.report_id,
        record_id=new_lab.record_id,
        aadhaar_number=new_lab.aadhaar_number,
        test_name=new_lab.test_name,
        result=new_lab.result,
        normal_range=new_lab.normal_range,
        unit=new_lab.unit,
        is_abnormal=new_lab.is_abnormal,
        report_date=new_lab.report_date,
        file_path=new_lab.file_path,
        created_at=new_lab.created_at,
        hospital_name="Diagnostic Imaging / Pathology"
    )

@router.get("/{report_id}/download")
def download_lab_file(report_id: int, db: Session = Depends(get_db)):
    lab = db.query(LabReport).filter(LabReport.report_id == report_id).first()
    if not lab or not lab.file_path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File attachment not found for this report.")

    file_path = os.path.join(settings.UPLOAD_DIR, lab.file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stored report file is missing.")

    return FileResponse(file_path, filename=f"MediLink_LabReport_{lab.report_id}.pdf")
