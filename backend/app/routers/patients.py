import datetime
import re
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.app.database import get_db
from backend.app.models.entities import Patient, MedicalRecord, LabReport, AccessLog, User, BedAllocation
from backend.app.schemas.all_schemas import PatientCreate, PatientUpdate, PatientOut
from backend.app.routers.auth import get_current_user, get_optional_user
from backend.app.services.report import mask_aadhaar

router = APIRouter(prefix="/patients", tags=["Patients"])

def normalize_aadhaar(aadhaar: str) -> str:
    """Normalize Aadhaar into standard 'XXXX XXXX XXXX' format."""
    clean = re.sub(r'[\s\-]', '', aadhaar)
    if len(clean) != 12 or not clean.isdigit():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Aadhaar must be exactly 12 digits (e.g., 2345 6789 0123)"
        )
    return f"{clean[0:4]} {clean[4:8]} {clean[8:12]}"

@router.get("", response_model=List[PatientOut])
def list_patients(
    search: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Patient)
    if search:
        s = f"%{search.strip()}%"
        # Search by name, raw aadhaar digits, phone, or blood group
        clean_digits = re.sub(r'\D', '', search)
        if len(clean_digits) >= 4:
            query = query.filter(
                (Patient.full_name.ilike(s)) |
                (Patient.aadhaar_number.like(f"%{clean_digits}%")) |
                (Patient.mobile.like(f"%{clean_digits}%"))
            )
        else:
            query = query.filter(
                (Patient.full_name.ilike(s)) |
                (Patient.blood_group.ilike(s)) |
                (Patient.allergies.ilike(s))
            )
            
    patients = query.order_by(Patient.created_at.desc()).offset(offset).limit(limit).all()
    results = []
    for p in patients:
        p_dict = {
            "aadhaar_number": p.aadhaar_number,
            "masked_aadhaar": mask_aadhaar(p.aadhaar_number),
            "full_name": p.full_name,
            "date_of_birth": p.date_of_birth,
            "gender": p.gender,
            "blood_group": p.blood_group,
            "mobile": p.mobile,
            "email": p.email,
            "address": p.address,
            "allergies": p.allergies,
            "chronic_conditions": p.chronic_conditions,
            "emergency_contact": p.emergency_contact,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
            "records": [],
            "lab_reports": []
        }
        results.append(PatientOut(**p_dict))
    return results

@router.get("/{aadhaar}", response_model=PatientOut)
def get_patient(
    aadhaar: str,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    norm_aadhaar = normalize_aadhaar(aadhaar)
    p = db.query(Patient).filter(Patient.aadhaar_number == norm_aadhaar).first()
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with Aadhaar {norm_aadhaar} not found.")

    # Record backend audit log for patient chart lookup
    accessor = user.full_name if user else "Hospital Clinician (AIIMS Delhi)"
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    audit = AccessLog(
        aadhaar_number=norm_aadhaar,
        hospital_id=user.hospital_id if user else 1,
        accessed_by=accessor,
        purpose="Patient Clinical Record Lookup",
        ip_address=client_ip,
        status="Authorized"
    )
    db.add(audit)
    db.commit()

    # Format records with hospital & doctor names
    records_out = []
    for r in p.records:
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
            "hospital_name": r.hospital.hospital_name if r.hospital else "Unknown Hospital",
            "doctor_name": r.doctor.doctor_name if r.doctor else "Hospital Physician",
            "lab_reports": []
        }
        records_out.append(r_dict)

    labs_out = []
    for l in p.lab_reports:
        l_dict = {
            "report_id": l.report_id,
            "record_id": l.record_id,
            "aadhaar_number": l.aadhaar_number,
            "test_name": l.test_name,
            "result": l.result,
            "normal_range": l.normal_range,
            "unit": l.unit,
            "is_abnormal": l.is_abnormal,
            "report_date": l.report_date,
            "file_path": l.file_path,
            "created_at": l.created_at,
            "hospital_name": l.record.hospital.hospital_name if l.record and l.record.hospital else "Hospital Pathology"
        }
        labs_out.append(l_dict)

    return PatientOut(
        aadhaar_number=p.aadhaar_number,
        masked_aadhaar=mask_aadhaar(p.aadhaar_number),
        full_name=p.full_name,
        date_of_birth=p.date_of_birth,
        gender=p.gender,
        blood_group=p.blood_group,
        mobile=p.mobile,
        email=p.email,
        address=p.address,
        allergies=p.allergies,
        chronic_conditions=p.chronic_conditions,
        emergency_contact=p.emergency_contact,
        created_at=p.created_at,
        updated_at=p.updated_at,
        records=records_out,
        lab_reports=labs_out
    )

@router.post("", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def register_patient(
    p_in: PatientCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    norm_aadhaar = normalize_aadhaar(p_in.aadhaar_number)
    
    # Check duplicate Aadhaar
    if db.query(Patient).filter(Patient.aadhaar_number == norm_aadhaar).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Patient with Aadhaar number {norm_aadhaar} is already registered."
        )

    # Validate mobile
    mobile_clean = None
    if p_in.mobile:
        m_digits = re.sub(r'\D', '', p_in.mobile)
        if len(m_digits) < 10:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Mobile number must contain at least 10 digits.")
        mobile_clean = f"+91 {m_digits[-10:-5]} {m_digits[-5:]}"
        # Check duplicate mobile
        if db.query(Patient).filter(Patient.mobile == mobile_clean).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A patient with this mobile number already exists.")

    # Validate DOB
    if p_in.date_of_birth > datetime.date.today():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Date of birth cannot be in the future.")

    new_p = Patient(
        aadhaar_number=norm_aadhaar,
        full_name=p_in.full_name.strip(),
        date_of_birth=p_in.date_of_birth,
        gender=p_in.gender,
        blood_group=p_in.blood_group,
        mobile=mobile_clean,
        email=p_in.email.strip() if p_in.email else None,
        address=p_in.address.strip() if p_in.address else None,
        allergies=p_in.allergies.strip() if p_in.allergies else "None",
        chronic_conditions=p_in.chronic_conditions.strip() if p_in.chronic_conditions else "None",
        emergency_contact=p_in.emergency_contact.strip() if p_in.emergency_contact else None
    )
    db.add(new_p)
    
    # Audit log registration
    accessor = user.full_name if user else "Registration Desk"
    client_ip = request.client.host if request.client else "127.0.0.1"
    audit = AccessLog(
        aadhaar_number=norm_aadhaar,
        hospital_id=user.hospital_id if user else 1,
        accessed_by=accessor,
        purpose="New Patient Enrollment",
        ip_address=client_ip,
        status="Authorized"
    )
    db.add(audit)
    db.commit()
    db.refresh(new_p)
    
    return PatientOut(
        aadhaar_number=new_p.aadhaar_number,
        masked_aadhaar=mask_aadhaar(new_p.aadhaar_number),
        full_name=new_p.full_name,
        date_of_birth=new_p.date_of_birth,
        gender=new_p.gender,
        blood_group=new_p.blood_group,
        mobile=new_p.mobile,
        email=new_p.email,
        address=new_p.address,
        allergies=new_p.allergies,
        chronic_conditions=new_p.chronic_conditions,
        emergency_contact=new_p.emergency_contact,
        created_at=new_p.created_at,
        updated_at=new_p.updated_at,
        records=[],
        lab_reports=[]
    )

@router.put("/{aadhaar}", response_model=PatientOut)
def update_patient(
    aadhaar: str,
    req: PatientUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    """Update existing patient clinical and contact details."""
    norm_aadhaar = normalize_aadhaar(aadhaar)
    p = db.query(Patient).filter(Patient.aadhaar_number == norm_aadhaar).first()
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")

    if req.full_name is not None and req.full_name.strip():
        p.full_name = req.full_name.strip()
    if req.blood_group is not None:
        p.blood_group = req.blood_group
    if req.mobile is not None:
        m_digits = re.sub(r'\D', '', req.mobile)
        if len(m_digits) >= 10:
            p.mobile = f"+91 {m_digits[-10:-5]} {m_digits[-5:]}"
    if req.email is not None:
        p.email = req.email.strip()
    if req.address is not None:
        p.address = req.address.strip()
    if req.allergies is not None:
        p.allergies = req.allergies.strip()
    if req.chronic_conditions is not None:
        p.chronic_conditions = req.chronic_conditions.strip()
    if req.emergency_contact is not None:
        p.emergency_contact = req.emergency_contact.strip()

    p.updated_at = datetime.datetime.now(datetime.timezone.utc)
    try:
        db.commit()
        db.refresh(p)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number or identifier is already in use by another patient record."
        )
    return get_patient(norm_aadhaar, request=request, db=db, user=user)

@router.post("/{aadhaar}/break-glass")
def trigger_break_glass(
    aadhaar: str,
    request: Request,
    reason: str = Query(..., min_length=5),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    """
    Emergency Break-Glass Protocol:
    Immediate trauma access with mandatory justification and immutable audit trail.
    """
    norm_aadhaar = normalize_aadhaar(aadhaar)
    p = db.query(Patient).filter(Patient.aadhaar_number == norm_aadhaar).first()
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
        
    accessor = user.full_name if user else "Emergency Physician"
    client_ip = request.client.host if request and request.client else "127.0.0.1"
    
    audit = AccessLog(
        aadhaar_number=norm_aadhaar,
        hospital_id=user.hospital_id if user else 1,
        accessed_by=f"[BREAK-GLASS] {accessor}",
        purpose=f"EMERGENCY OVERRIDE: {reason}",
        ip_address=client_ip,
        status="Authorized"
    )
    db.add(audit)
    db.commit()
    
    # Return vital emergency snapshot
    active_rx = p.records[0].prescription if p.records else "No active prescriptions on record."
    return {
        "status": "EMERGENCY_ACCESS_GRANTED",
        "aadhaar": norm_aadhaar,
        "name": p.full_name,
        "blood_group": p.blood_group,
        "allergies": p.allergies,
        "chronic_conditions": p.chronic_conditions,
        "emergency_contact": p.emergency_contact,
        "active_prescriptions": active_rx,
        "audit_id": audit.log_id,
        "timestamp": audit.access_time.isoformat()
    }
