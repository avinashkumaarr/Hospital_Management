import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.database import get_db
from backend.app.models.entities import Hospital, Doctor, MedicalRecord, Appointment
from backend.app.schemas.all_schemas import HospitalOut, DoctorOut

router = APIRouter(tags=["Hospitals & Doctors"])

@router.get("/hospitals", response_model=List[HospitalOut])
def list_hospitals(db: Session = Depends(get_db)):
    hospitals = db.query(Hospital).filter(Hospital.is_active == True).all()
    return hospitals

@router.get("/doctors")
def list_doctors_with_metrics(db: Session = Depends(get_db)):
    """List doctors with today's consultation count and upcoming appointment counts."""
    doctors = db.query(Doctor).join(Hospital).filter(Doctor.is_active == True).all()
    today = datetime.date.today()
    
    results = []
    for d in doctors:
        # Consultations today
        today_consults = db.query(func.count(MedicalRecord.record_id)).filter(
            MedicalRecord.doctor_id == d.doctor_id,
            MedicalRecord.visit_date == today
        ).scalar() or 0
        
        # Upcoming appointments
        upcoming_appts = db.query(func.count(Appointment.appointment_id)).filter(
            Appointment.doctor_id == d.doctor_id,
            Appointment.appointment_date >= today,
            Appointment.status == "Scheduled"
        ).scalar() or 0
        
        results.append({
            "doctor_id": d.doctor_id,
            "hospital_id": d.hospital_id,
            "hospital_name": d.hospital.hospital_name if d.hospital else "Hospital",
            "doctor_name": d.doctor_name,
            "specialization": d.specialization,
            "qualification": d.qualification,
            "license_no": d.license_no,
            "contact": d.contact,
            "email": d.email,
            "is_active": d.is_active,
            "today_consultations": today_consults,
            "upcoming_appointments": upcoming_appts,
            "scheduled_slots": ["09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM"]
        })
    return results
