import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.database import get_db
from backend.app.models.entities import OPDQueue, Patient, Doctor, Hospital
from backend.app.schemas.all_schemas import QueueOut, QueueIssueRequest, QueueStatusUpdate

router = APIRouter(prefix="/queue", tags=["OPD Queue"])

@router.get("", response_model=List[QueueOut])
def list_queue(
    hospital_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    target_date: Optional[datetime.date] = None,
    db: Session = Depends(get_db)
):
    date_val = target_date or datetime.date.today()
    query = db.query(OPDQueue).join(Patient).join(Hospital).outerjoin(Doctor).filter(
        OPDQueue.queue_date == date_val
    )
    if hospital_id:
        query = query.filter(OPDQueue.hospital_id == hospital_id)
    if doctor_id:
        query = query.filter(OPDQueue.doctor_id == doctor_id)
    if status_filter and status_filter.upper() != "ALL":
        query = query.filter(OPDQueue.status == status_filter)
        
    items = query.order_by(OPDQueue.queue_id.asc()).all()
    results = []
    for q in items:
        results.append(QueueOut(
            queue_id=q.queue_id,
            token_number=q.token_number,
            aadhaar_number=q.aadhaar_number,
            patient_name=q.patient.full_name if q.patient else "Patient",
            doctor_id=q.doctor_id,
            doctor_name=q.doctor.doctor_name if q.doctor else "General Consultation",
            hospital_id=q.hospital_id,
            hospital_name=q.hospital.hospital_name if q.hospital else "Hospital",
            queue_date=q.queue_date,
            status=q.status,
            time_issued=q.time_issued,
            completed_at=q.completed_at
        ))
    return results

@router.post("/issue", response_model=QueueOut, status_code=status.HTTP_201_CREATED)
def issue_queue_token(req: QueueIssueRequest, db: Session = Depends(get_db)):
    # 1. Verify patient
    patient = db.query(Patient).filter(Patient.aadhaar_number == req.aadhaar_number).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient {req.aadhaar_number} not found.")

    today = datetime.date.today()
    
    # 2. Check if patient already has an active (Waiting or Serving) token today
    existing = db.query(OPDQueue).filter(
        OPDQueue.aadhaar_number == req.aadhaar_number,
        OPDQueue.queue_date == today,
        OPDQueue.status.in_(["Waiting", "Serving"])
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Patient {patient.full_name} already has active token {existing.token_number} with status '{existing.status}' today."
        )

    # 3. Collision-safe daily token numbering
    count_today = db.query(func.count(OPDQueue.queue_id)).filter(
        OPDQueue.queue_date == today,
        OPDQueue.hospital_id == req.hospital_id
    ).scalar() or 0
    
    next_num = 101 + count_today
    token_str = f"A-{next_num}"
    
    # Double check unique token for today
    while db.query(OPDQueue).filter(OPDQueue.queue_date == today, OPDQueue.token_number == token_str).first():
        next_num += 1
        token_str = f"A-{next_num}"
        
    time_str = datetime.datetime.now().strftime("%I:%M %p")
    
    new_q = OPDQueue(
        token_number=token_str,
        aadhaar_number=req.aadhaar_number,
        doctor_id=req.doctor_id,
        hospital_id=req.hospital_id,
        queue_date=today,
        status="Waiting",
        time_issued=time_str
    )
    db.add(new_q)
    db.commit()
    db.refresh(new_q)
    
    doc = db.query(Doctor).filter(Doctor.doctor_id == req.doctor_id).first() if req.doctor_id else None
    hosp = db.query(Hospital).filter(Hospital.hospital_id == req.hospital_id).first()

    return QueueOut(
        queue_id=new_q.queue_id,
        token_number=new_q.token_number,
        aadhaar_number=new_q.aadhaar_number,
        patient_name=patient.full_name,
        doctor_id=new_q.doctor_id,
        doctor_name=doc.doctor_name if doc else "General Consultation",
        hospital_id=new_q.hospital_id,
        hospital_name=hosp.hospital_name if hosp else "Hospital",
        queue_date=new_q.queue_date,
        status=new_q.status,
        time_issued=new_q.time_issued,
        completed_at=new_q.completed_at
    )

@router.put("/{queue_id}/status", response_model=QueueOut)
def update_queue_status(queue_id: int, req: QueueStatusUpdate, db: Session = Depends(get_db)):
    q = db.query(OPDQueue).filter(OPDQueue.queue_id == queue_id).first()
    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue token not found.")

    if req.status not in ["Waiting", "Serving", "Completed", "Cancelled"]:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid queue status.")

    # If setting to Serving, set any other currently Serving token for this doctor/hospital to Waiting or Completed
    if req.status == "Serving":
        currently_serving = db.query(OPDQueue).filter(
            OPDQueue.queue_date == q.queue_date,
            OPDQueue.hospital_id == q.hospital_id,
            OPDQueue.status == "Serving",
            OPDQueue.queue_id != q.queue_id
        ).all()
        for c in currently_serving:
            c.status = "Waiting"

    q.status = req.status
    if req.status == "Completed":
        q.completed_at = datetime.datetime.now(datetime.timezone.utc)

    db.commit()
    db.refresh(q)

    return QueueOut(
        queue_id=q.queue_id,
        token_number=q.token_number,
        aadhaar_number=q.aadhaar_number,
        patient_name=q.patient.full_name if q.patient else "Patient",
        doctor_id=q.doctor_id,
        doctor_name=q.doctor.doctor_name if q.doctor else "General Consultation",
        hospital_id=q.hospital_id,
        hospital_name=q.hospital.hospital_name if q.hospital else "Hospital",
        queue_date=q.queue_date,
        status=q.status,
        time_issued=q.time_issued,
        completed_at=q.completed_at
    )
