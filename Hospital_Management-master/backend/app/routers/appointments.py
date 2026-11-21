import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import Appointment, Patient, Doctor, Hospital, Notification
from backend.app.schemas.all_schemas import (
    AppointmentCreate, AppointmentReschedule, AppointmentStatusUpdate, AppointmentOut
)

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.get("", response_model=List[AppointmentOut])
def list_appointments(
    hospital_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    aadhaar: Optional[str] = None,
    date_filter: Optional[datetime.date] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Appointment).join(Patient).join(Hospital).join(Doctor)
    if hospital_id:
        query = query.filter(Appointment.hospital_id == hospital_id)
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if aadhaar:
        query = query.filter(Appointment.aadhaar_number == aadhaar)
    if date_filter:
        query = query.filter(Appointment.appointment_date == date_filter)
    if status_filter and status_filter.upper() != "ALL":
        query = query.filter(Appointment.status == status_filter)

    appts = query.order_by(Appointment.appointment_date.asc(), Appointment.time_slot.asc()).all()
    results = []
    for a in appts:
        results.append(AppointmentOut(
            appointment_id=a.appointment_id,
            aadhaar_number=a.aadhaar_number,
            patient_name=a.patient.full_name if a.patient else "Patient",
            doctor_id=a.doctor_id,
            doctor_name=a.doctor.doctor_name if a.doctor else "Doctor",
            hospital_id=a.hospital_id,
            hospital_name=a.hospital.hospital_name if a.hospital else "Hospital",
            department=a.department,
            appointment_date=a.appointment_date,
            time_slot=a.time_slot,
            reason=a.reason,
            status=a.status,
            created_at=a.created_at
        ))
    return results

@router.post("", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def book_appointment(req: AppointmentCreate, db: Session = Depends(get_db)):
    # 1. Verify patient
    patient = db.query(Patient).filter(Patient.aadhaar_number == req.aadhaar_number).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient {req.aadhaar_number} not found.")

    # 2. Verify doctor
    doctor = db.query(Doctor).filter(Doctor.doctor_id == req.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor ID {req.doctor_id} not found.")

    # 3. Check for double booking (same doctor, same date, same slot)
    slot_conflict = db.query(Appointment).filter(
        Appointment.doctor_id == req.doctor_id,
        Appointment.appointment_date == req.appointment_date,
        Appointment.time_slot == req.time_slot,
        Appointment.status != "Cancelled"
    ).first()
    if slot_conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{doctor.doctor_name} is already booked for {req.time_slot} on {req.appointment_date}. Please choose another slot."
        )

    # 4. Check date is not in past
    if req.appointment_date < datetime.date.today():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Cannot book appointments in the past.")

    new_appt = Appointment(
        aadhaar_number=req.aadhaar_number,
        doctor_id=req.doctor_id,
        hospital_id=req.hospital_id,
        department=req.department or doctor.specialization,
        appointment_date=req.appointment_date,
        time_slot=req.time_slot,
        reason=req.reason,
        status="Scheduled"
    )
    db.add(new_appt)
    
    # In-app notification
    notif = Notification(
        title="Appointment Confirmed",
        message=f"Appointment booked for {patient.full_name} with {doctor.doctor_name} on {req.appointment_date} at {req.time_slot}.",
        notification_type="appointment",
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(new_appt)

    hosp = db.query(Hospital).filter(Hospital.hospital_id == req.hospital_id).first()
    return AppointmentOut(
        appointment_id=new_appt.appointment_id,
        aadhaar_number=new_appt.aadhaar_number,
        patient_name=patient.full_name,
        doctor_id=doctor.doctor_id,
        doctor_name=doctor.doctor_name,
        hospital_id=new_appt.hospital_id,
        hospital_name=hosp.hospital_name if hosp else "Hospital",
        department=new_appt.department,
        appointment_date=new_appt.appointment_date,
        time_slot=new_appt.time_slot,
        reason=new_appt.reason,
        status=new_appt.status,
        created_at=new_appt.created_at
    )

@router.put("/{appointment_id}/reschedule", response_model=AppointmentOut)
def reschedule_appointment(appointment_id: int, req: AppointmentReschedule, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")

    if req.appointment_date < datetime.date.today():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Cannot reschedule to a past date.")

    # Check collision for new slot
    slot_conflict = db.query(Appointment).filter(
        Appointment.doctor_id == appt.doctor_id,
        Appointment.appointment_date == req.appointment_date,
        Appointment.time_slot == req.time_slot,
        Appointment.appointment_id != appointment_id,
        Appointment.status != "Cancelled"
    ).first()
    if slot_conflict:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Selected slot is already reserved. Please select an available slot.")

    appt.appointment_date = req.appointment_date
    appt.time_slot = req.time_slot
    if req.reason:
        appt.reason = f"{appt.reason or ''} (Rescheduled: {req.reason})".strip()
    appt.status = "Rescheduled"
    db.commit()
    db.refresh(appt)

    return AppointmentOut(
        appointment_id=appt.appointment_id,
        aadhaar_number=appt.aadhaar_number,
        patient_name=appt.patient.full_name if appt.patient else "Patient",
        doctor_id=appt.doctor_id,
        doctor_name=appt.doctor.doctor_name if appt.doctor else "Doctor",
        hospital_id=appt.hospital_id,
        hospital_name=appt.hospital.hospital_name if appt.hospital else "Hospital",
        department=appt.department,
        appointment_date=appt.appointment_date,
        time_slot=appt.time_slot,
        reason=appt.reason,
        status=appt.status,
        created_at=appt.created_at
    )

@router.put("/{appointment_id}/status", response_model=AppointmentOut)
def update_appointment_status(appointment_id: int, req: AppointmentStatusUpdate, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")

    if req.status not in ["Scheduled", "Completed", "Cancelled", "Rescheduled"]:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid status.")

    appt.status = req.status
    db.commit()
    db.refresh(appt)

    return AppointmentOut(
        appointment_id=appt.appointment_id,
        aadhaar_number=appt.aadhaar_number,
        patient_name=appt.patient.full_name if appt.patient else "Patient",
        doctor_id=appt.doctor_id,
        doctor_name=appt.doctor.doctor_name if appt.doctor else "Doctor",
        hospital_id=appt.hospital_id,
        hospital_name=appt.hospital.hospital_name if appt.hospital else "Hospital",
        department=appt.department,
        appointment_date=appt.appointment_date,
        time_slot=appt.time_slot,
        reason=appt.reason,
        status=appt.status,
        created_at=appt.created_at
    )
