import csv
import io
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.entities import Patient, MedicalRecord, BedAllocation, Appointment, Hospital

def mask_aadhaar(aadhaar: str) -> str:
    """Mask Aadhaar to format XXXX-XXXX-1234."""
    clean = aadhaar.replace(" ", "").replace("-", "")
    if len(clean) >= 4:
        return f"XXXX-XXXX-{clean[-4:]}"
    return "XXXX-XXXX-XXXX"

def export_records_csv(db: Session, hospital_id: Optional[int] = None) -> str:
    """Generate CSV string of medical encounters with masked sensitive identifiers."""
    query = db.query(MedicalRecord).join(Patient).join(Hospital)
    if hospital_id:
        query = query.filter(MedicalRecord.hospital_id == hospital_id)
    
    records = query.order_by(MedicalRecord.visit_date.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Record ID", "Visit Date", "Patient Name", "Masked Aadhaar",
        "Hospital", "Department", "Visit Type", "Diagnosis", "ICD-10", "Prescription", "Follow Up"
    ])
    
    for r in records:
        writer.writerow([
            f"REC-{r.record_id:04d}",
            r.visit_date.strftime("%Y-%m-%d"),
            r.patient.full_name,
            mask_aadhaar(r.aadhaar_number),
            r.hospital.hospital_name,
            r.department or "General",
            r.visit_type,
            r.diagnosis,
            r.icd10_code or "",
            (r.prescription or "").replace("\n", " ; "),
            r.follow_up_date.strftime("%Y-%m-%d") if r.follow_up_date else ""
        ])
    
    return output.getvalue()

def export_bed_utilization_csv(db: Session, hospital_id: Optional[int] = None) -> str:
    """Generate CSV of bed utilization status across wards."""
    query = db.query(BedAllocation).join(Hospital)
    if hospital_id:
        query = query.filter(BedAllocation.hospital_id == hospital_id)
        
    beds = query.order_by(BedAllocation.ward_name, BedAllocation.bed_number).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Allocation ID", "Hospital", "Ward Name", "Bed Number", "Status", "Patient Name", "Masked Aadhaar", "Admitted At", "Expected Discharge"])
    
    for b in beds:
        writer.writerow([
            b.allocation_id,
            b.hospital.hospital_name,
            b.ward_name,
            b.bed_number,
            b.status,
            b.patient.full_name if b.patient else "",
            mask_aadhaar(b.aadhaar_number) if b.aadhaar_number else "",
            b.admitted_at.strftime("%Y-%m-%d %H:%M") if b.admitted_at else "",
            b.expected_discharge.strftime("%Y-%m-%d") if b.expected_discharge else ""
        ])
    return output.getvalue()

def export_appointments_csv(db: Session, hospital_id: Optional[int] = None) -> str:
    """Generate CSV of appointments."""
    query = db.query(Appointment).join(Patient).join(Hospital)
    if hospital_id:
        query = query.filter(Appointment.hospital_id == hospital_id)
        
    appts = query.order_by(Appointment.appointment_date.desc(), Appointment.time_slot).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Appt ID", "Date", "Slot", "Hospital", "Department", "Doctor", "Patient", "Masked Aadhaar", "Reason", "Status"])
    
    for a in appts:
        writer.writerow([
            f"APT-{a.appointment_id:04d}",
            a.appointment_date.strftime("%Y-%m-%d"),
            a.time_slot,
            a.hospital.hospital_name,
            a.department or "",
            a.doctor.doctor_name if a.doctor else "",
            a.patient.full_name if a.patient else "",
            mask_aadhaar(a.aadhaar_number),
            a.reason or "",
            a.status
        ])
    return output.getvalue()
