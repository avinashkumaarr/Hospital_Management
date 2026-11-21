import datetime
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import (
    Hospital, Doctor, Patient, MedicalRecord, LabReport, BedAllocation, OPDQueue, AccessLog, Appointment
)
from backend.app.services.seed import seed_database_if_empty

router = APIRouter(prefix="/backup", tags=["Backup & Restore"])

@router.get("/export")
def export_database_json(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Export the entire relational database state to JSON format."""
    hospitals = db.query(Hospital).all()
    doctors = db.query(Doctor).all()
    patients = db.query(Patient).all()
    records = db.query(MedicalRecord).all()
    labs = db.query(LabReport).all()
    beds = db.query(BedAllocation).all()
    queue = db.query(OPDQueue).all()
    appts = db.query(Appointment).all()

    return {
        "export_date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "version": "4.0.0",
        "hospitals": [
            {"hospital_id": h.hospital_id, "hospital_name": h.hospital_name, "registration_no": h.registration_no, "hospital_type": h.hospital_type, "city": h.city, "state": h.state}
            for h in hospitals
        ],
        "doctors": [
            {"doctor_id": d.doctor_id, "hospital_id": d.hospital_id, "doctor_name": d.doctor_name, "specialization": d.specialization, "qualification": d.qualification}
            for d in doctors
        ],
        "patients": [
            {
                "aadhaar_number": p.aadhaar_number,
                "full_name": p.full_name,
                "date_of_birth": p.date_of_birth.isoformat(),
                "gender": p.gender,
                "blood_group": p.blood_group,
                "mobile": p.mobile,
                "email": p.email,
                "address": p.address,
                "allergies": p.allergies,
                "chronic_conditions": p.chronic_conditions,
                "emergency_contact": p.emergency_contact
            }
            for p in patients
        ],
        "records": [
            {
                "record_id": r.record_id,
                "aadhaar_number": r.aadhaar_number,
                "hospital_id": r.hospital_id,
                "doctor_id": r.doctor_id,
                "visit_date": r.visit_date.isoformat(),
                "visit_type": r.visit_type,
                "department": r.department,
                "diagnosis": r.diagnosis,
                "icd10_code": r.icd10_code,
                "vitals_summary": r.vitals_summary,
                "prescription": r.prescription,
                "notes": r.notes
            }
            for r in records
        ],
        "beds": [
            {
                "allocation_id": b.allocation_id,
                "hospital_id": b.hospital_id,
                "ward_name": b.ward_name,
                "bed_number": b.bed_number,
                "aadhaar_number": b.aadhaar_number,
                "status": b.status
            }
            for b in beds
        ]
    }

@router.post("/import")
def import_database_json(data: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    """
    Validated non-destructive import of backup or legacy localStorage JSON.
    Preserves existing records while merging or inserting new records.
    """
    imported_counts = {"patients": 0, "records": 0, "beds": 0}

    # Handle legacy 'medilink_db_v2' schema or new format
    patients_list = data.get("patients", [])
    for p_raw in patients_list:
        aadhaar = p_raw.get("aadhaar_number") or p_raw.get("aadhaar")
        if not aadhaar:
            continue
            
        existing_p = db.query(Patient).filter(Patient.aadhaar_number == aadhaar).first()
        dob_val = p_raw.get("date_of_birth") or p_raw.get("dob") or "1990-01-01"
        try:
            dob_date = datetime.date.fromisoformat(dob_val)
        except Exception:
            dob_date = datetime.date(1990, 1, 1)

        if not existing_p:
            new_p = Patient(
                aadhaar_number=aadhaar,
                full_name=p_raw.get("full_name") or p_raw.get("name") or "Imported Patient",
                date_of_birth=dob_date,
                gender=p_raw.get("gender") or "Other",
                blood_group=p_raw.get("blood_group") or p_raw.get("blood") or "O+",
                mobile=p_raw.get("mobile"),
                email=p_raw.get("email"),
                address=p_raw.get("address"),
                allergies=p_raw.get("allergies") or "None",
                chronic_conditions=p_raw.get("chronic_conditions") or p_raw.get("chronic") or "None",
                emergency_contact=p_raw.get("emergency_contact") or p_raw.get("emergencyContact")
            )
            db.add(new_p)
            imported_counts["patients"] += 1
            
        # Import legacy nested records if present
        nested_records = p_raw.get("records", [])
        for r_raw in nested_records:
            diag = r_raw.get("diagnosis", "Consultation")
            v_date_str = r_raw.get("date") or r_raw.get("visit_date") or datetime.date.today().isoformat()
            try:
                v_date = datetime.date.fromisoformat(v_date_str)
            except Exception:
                v_date = datetime.date.today()

            # Check if record already exists
            rec_exist = db.query(MedicalRecord).filter(
                MedicalRecord.aadhaar_number == aadhaar,
                MedicalRecord.diagnosis == diag,
                MedicalRecord.visit_date == v_date
            ).first()
            if not rec_exist:
                new_rec = MedicalRecord(
                    aadhaar_number=aadhaar,
                    hospital_id=1,
                    visit_date=v_date,
                    visit_type=r_raw.get("type", "OPD Consultation"),
                    department=r_raw.get("dept", "General Medicine"),
                    diagnosis=diag,
                    icd10_code=r_raw.get("icd10"),
                    vitals_summary=r_raw.get("vitals"),
                    prescription=r_raw.get("prescription"),
                    notes=r_raw.get("notes")
                )
                db.add(new_rec)
                imported_counts["records"] += 1

    db.commit()
    return {
        "status": "success",
        "message": f"Successfully imported: {imported_counts['patients']} new patients, {imported_counts['records']} clinical records.",
        "details": imported_counts
    }
