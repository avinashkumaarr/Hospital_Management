from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import MedicalRecord, Patient, Doctor, Hospital, AccessLog, User
from backend.app.schemas.all_schemas import MedicalRecordCreate, MedicalRecordOut
from backend.app.routers.auth import get_optional_user
from backend.app.services.cdss import check_allergy_and_drug_safety

router = APIRouter(prefix="/records", tags=["Medical Records"])

@router.get("", response_model=List[MedicalRecordOut])
def list_records(
    aadhaar: Optional[str] = None,
    hospital_id: Optional[int] = None,
    department: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(MedicalRecord).join(Hospital).outerjoin(Doctor)
    if aadhaar:
        clean = aadhaar.strip()
        query = query.filter(MedicalRecord.aadhaar_number.like(f"%{clean}%"))
    if hospital_id:
        query = query.filter(MedicalRecord.hospital_id == hospital_id)
    if department:
        query = query.filter(MedicalRecord.department == department)
        
    records = query.order_by(MedicalRecord.visit_date.desc()).limit(limit).all()
    results = []
    for r in records:
        r_dict = {
            "record_id": r.record_id,
            "aadhaar_number": r.aadhaar_number,
            "hospital_id": r.hospital_id,
            "doctor_id": r.doctor_id,
            "visit_date": r.visit_date,
            "visit_type": r.visit_type,
            "department": r.department,
            "chief_complaint": r.chief_complaint,
            "diagnosis": r.diagnosis,
            "icd10_code": r.icd10_code,
            "vitals_summary": r.vitals_summary,
            "prescription": r.prescription,
            "notes": r.notes,
            "follow_up_date": r.follow_up_date,
            "created_at": r.created_at,
            "hospital_name": r.hospital.hospital_name if r.hospital else "Hospital",
            "doctor_name": r.doctor.doctor_name if r.doctor else "Physician",
            "lab_reports": []
        }
        results.append(MedicalRecordOut(**r_dict))
    return results

@router.get("/{record_id}", response_model=MedicalRecordOut)
def get_record(record_id: int, db: Session = Depends(get_db)):
    r = db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medical record #{record_id} not found.")
    
    r_dict = {
        "record_id": r.record_id,
        "aadhaar_number": r.aadhaar_number,
        "hospital_id": r.hospital_id,
        "doctor_id": r.doctor_id,
        "visit_date": r.visit_date,
        "visit_type": r.visit_type,
        "department": r.department,
        "chief_complaint": r.chief_complaint,
        "diagnosis": r.diagnosis,
        "icd10_code": r.icd10_code,
        "vitals_summary": r.vitals_summary,
        "prescription": r.prescription,
        "notes": r.notes,
        "follow_up_date": r.follow_up_date,
        "created_at": r.created_at,
        "hospital_name": r.hospital.hospital_name if r.hospital else "Hospital",
        "doctor_name": r.doctor.doctor_name if r.doctor else "Physician",
        "lab_reports": []
    }
    return MedicalRecordOut(**r_dict)

@router.post("", response_model=MedicalRecordOut, status_code=status.HTTP_201_CREATED)
def create_record(
    r_in: MedicalRecordCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    patient = db.query(Patient).filter(Patient.aadhaar_number == r_in.aadhaar_number).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with Aadhaar {r_in.aadhaar_number} not found.")
        
    hospital = db.query(Hospital).filter(Hospital.hospital_id == r_in.hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hospital ID {r_in.hospital_id} not found.")

    # CDSS Safety Evaluation
    safety = check_allergy_and_drug_safety(patient.allergies, r_in.prescription or "")

    new_record = MedicalRecord(
        aadhaar_number=r_in.aadhaar_number,
        hospital_id=r_in.hospital_id,
        doctor_id=r_in.doctor_id,
        visit_date=r_in.visit_date,
        visit_type=r_in.visit_type,
        department=r_in.department,
        chief_complaint=r_in.chief_complaint,
        diagnosis=r_in.diagnosis,
        icd10_code=r_in.icd10_code,
        vitals_summary=r_in.vitals_summary,
        prescription=r_in.prescription,
        notes=r_in.notes,
        follow_up_date=r_in.follow_up_date
    )
    db.add(new_record)
    
    # Audit log encounter entry
    accessor = user.full_name if user else "Consulting Doctor"
    client_ip = request.client.host if request.client else "127.0.0.1"
    audit = AccessLog(
        aadhaar_number=r_in.aadhaar_number,
        hospital_id=r_in.hospital_id,
        accessed_by=accessor,
        purpose=f"Clinical Encounter: {r_in.diagnosis[:40]}",
        ip_address=client_ip,
        status="Authorized"
    )
    db.add(audit)
    db.commit()
    db.refresh(new_record)

    doc = db.query(Doctor).filter(Doctor.doctor_id == new_record.doctor_id).first() if new_record.doctor_id else None
    
    r_dict = {
        "record_id": new_record.record_id,
        "aadhaar_number": new_record.aadhaar_number,
        "hospital_id": new_record.hospital_id,
        "doctor_id": new_record.doctor_id,
        "visit_date": new_record.visit_date,
        "visit_type": new_record.visit_type,
        "department": new_record.department,
        "chief_complaint": new_record.chief_complaint,
        "diagnosis": new_record.diagnosis,
        "icd10_code": new_record.icd10_code,
        "vitals_summary": new_record.vitals_summary,
        "prescription": new_record.prescription,
        "notes": new_record.notes,
        "follow_up_date": new_record.follow_up_date,
        "created_at": new_record.created_at,
        "hospital_name": hospital.hospital_name,
        "doctor_name": doc.doctor_name if doc else "Physician",
        "lab_reports": []
    }
    return MedicalRecordOut(**r_dict)
