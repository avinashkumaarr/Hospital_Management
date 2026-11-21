import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import BedAllocation, Patient, Hospital, AccessLog, User
from backend.app.schemas.all_schemas import BedOut, BedAdmitRequest, BedStatusUpdate
from backend.app.routers.auth import get_optional_user

router = APIRouter(prefix="/beds", tags=["Beds & Wards"])

@router.get("", response_model=List[BedOut])
def list_beds(
    hospital_id: Optional[int] = None,
    ward: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(BedAllocation).join(Hospital).outerjoin(Patient)
    if hospital_id:
        query = query.filter(BedAllocation.hospital_id == hospital_id)
    if ward and ward.upper() != "ALL":
        query = query.filter(BedAllocation.ward_name == ward)
    if status_filter and status_filter.upper() != "ALL":
        query = query.filter(BedAllocation.status == status_filter)
        
    beds = query.order_by(BedAllocation.ward_name, BedAllocation.bed_number).all()
    results = []
    for b in beds:
        results.append(BedOut(
            allocation_id=b.allocation_id,
            hospital_id=b.hospital_id,
            ward_name=b.ward_name,
            bed_number=b.bed_number,
            aadhaar_number=b.aadhaar_number,
            patient_name=b.patient.full_name if b.patient else None,
            status=b.status,
            admitted_at=b.admitted_at,
            expected_discharge=b.expected_discharge,
            hospital_name=b.hospital.hospital_name if b.hospital else "Hospital"
        ))
    return results

@router.post("/admit", response_model=BedOut)
def admit_patient(
    req: BedAdmitRequest,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    # 1. Check patient exists
    patient = db.query(Patient).filter(Patient.aadhaar_number == req.aadhaar_number).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient {req.aadhaar_number} not found.")

    # 2. Check if patient already has an active occupied bed across any hospital (Fix Phase 4 Bug 4)
    existing_bed = db.query(BedAllocation).filter(
        BedAllocation.aadhaar_number == req.aadhaar_number,
        BedAllocation.status == "Occupied"
    ).first()
    if existing_bed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Patient {patient.full_name} is already admitted in {existing_bed.ward_name} (Bed {existing_bed.bed_number}). Discharge or transfer before re-admitting."
        )

    # 3. Check bed availability
    bed = db.query(BedAllocation).filter(
        BedAllocation.hospital_id == req.hospital_id,
        BedAllocation.bed_number == req.bed_number
    ).first()
    if not bed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bed {req.bed_number} not found in hospital {req.hospital_id}.")
        
    if bed.status != "Vacant":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bed {bed.bed_number} is currently '{bed.status}'. Only Vacant beds can be allocated."
        )

    # 4. Atomic allocation update
    bed.status = "Occupied"
    bed.aadhaar_number = patient.aadhaar_number
    bed.admitted_at = datetime.datetime.now(datetime.timezone.utc)
    bed.expected_discharge = req.expected_discharge
    
    # Audit log bed admission
    accessor = user.full_name if user else "Inpatient Coordinator"
    client_ip = request.client.host if request.client else "127.0.0.1"
    audit = AccessLog(
        aadhaar_number=patient.aadhaar_number,
        hospital_id=req.hospital_id,
        accessed_by=accessor,
        purpose=f"Bed Admission: {bed.ward_name} ({bed.bed_number})",
        ip_address=client_ip,
        status="Authorized"
    )
    db.add(audit)
    db.commit()
    db.refresh(bed)

    return BedOut(
        allocation_id=bed.allocation_id,
        hospital_id=bed.hospital_id,
        ward_name=bed.ward_name,
        bed_number=bed.bed_number,
        aadhaar_number=bed.aadhaar_number,
        patient_name=patient.full_name,
        status=bed.status,
        admitted_at=bed.admitted_at,
        expected_discharge=bed.expected_discharge,
        hospital_name=bed.hospital.hospital_name if bed.hospital else "Hospital"
    )

@router.post("/{allocation_id}/discharge", response_model=BedOut)
def discharge_bed(
    allocation_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    bed = db.query(BedAllocation).filter(BedAllocation.allocation_id == allocation_id).first()
    if not bed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bed allocation not found.")

    old_aadhaar = bed.aadhaar_number
    old_patient_name = bed.patient.full_name if bed.patient else "Patient"

    bed.status = "Cleaning"
    bed.aadhaar_number = None
    bed.expected_discharge = None
    
    if old_aadhaar:
        accessor = user.full_name if user else "Discharge Coordinator"
        client_ip = request.client.host if request.client else "127.0.0.1"
        audit = AccessLog(
            aadhaar_number=old_aadhaar,
            hospital_id=bed.hospital_id,
            accessed_by=accessor,
            purpose=f"Bed Discharge & Sanitization: {bed.ward_name} ({bed.bed_number})",
            ip_address=client_ip,
            status="Authorized"
        )
        db.add(audit)

    db.commit()
    db.refresh(bed)

    return BedOut(
        allocation_id=bed.allocation_id,
        hospital_id=bed.hospital_id,
        ward_name=bed.ward_name,
        bed_number=bed.bed_number,
        aadhaar_number=None,
        patient_name=None,
        status=bed.status,
        admitted_at=bed.admitted_at,
        expected_discharge=bed.expected_discharge,
        hospital_name=bed.hospital.hospital_name if bed.hospital else "Hospital"
    )

@router.post("/{allocation_id}/clean", response_model=BedOut)
def mark_bed_clean(allocation_id: int, db: Session = Depends(get_db)):
    bed = db.query(BedAllocation).filter(BedAllocation.allocation_id == allocation_id).first()
    if not bed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bed allocation not found.")

    bed.status = "Vacant"
    bed.aadhaar_number = None
    bed.admitted_at = None
    bed.expected_discharge = None
    db.commit()
    db.refresh(bed)

    return BedOut(
        allocation_id=bed.allocation_id,
        hospital_id=bed.hospital_id,
        ward_name=bed.ward_name,
        bed_number=bed.bed_number,
        aadhaar_number=None,
        patient_name=None,
        status=bed.status,
        admitted_at=None,
        expected_discharge=None,
        hospital_name=bed.hospital.hospital_name if bed.hospital else "Hospital"
    )
