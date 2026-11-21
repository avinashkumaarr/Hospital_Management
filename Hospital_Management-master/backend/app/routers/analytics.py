import datetime
from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.database import get_db
from backend.app.models.entities import (
    Patient, MedicalRecord, BedAllocation, OPDQueue, Appointment, Hospital
)
from backend.app.schemas.all_schemas import DashboardStats
from backend.app.services.report import (
    export_records_csv, export_bed_utilization_csv, export_appointments_csv
)

router = APIRouter(prefix="/analytics", tags=["Analytics & Reports"])

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(hospital_id: int = None, db: Session = Depends(get_db)):
    today = datetime.date.today()
    
    total_patients = db.query(func.count(Patient.aadhaar_number)).scalar() or 0
    
    rec_q = db.query(func.count(MedicalRecord.record_id))
    if hospital_id:
        rec_q = rec_q.filter(MedicalRecord.hospital_id == hospital_id)
    total_records = rec_q.scalar() or 0
    
    today_q = db.query(func.count(MedicalRecord.record_id)).filter(MedicalRecord.visit_date == today)
    if hospital_id:
        today_q = today_q.filter(MedicalRecord.hospital_id == hospital_id)
    today_consultations = today_q.scalar() or 0
    
    bed_q = db.query(BedAllocation)
    if hospital_id:
        bed_q = bed_q.filter(BedAllocation.hospital_id == hospital_id)
    all_beds = bed_q.all()
    total_beds = len(all_beds)
    occupied_beds = sum(1 for b in all_beds if b.status == "Occupied")
    vacant_beds = sum(1 for b in all_beds if b.status == "Vacant")
    cleaning_beds = sum(1 for b in all_beds if b.status == "Cleaning")
    occupancy_pct = round((occupied_beds / total_beds * 100), 1) if total_beds > 0 else 0.0
    
    queue_q = db.query(func.count(OPDQueue.queue_id)).filter(
        OPDQueue.queue_date == today,
        OPDQueue.status.in_(["Waiting", "Serving"])
    )
    if hospital_id:
        queue_q = queue_q.filter(OPDQueue.hospital_id == hospital_id)
    waiting_queue = queue_q.scalar() or 0
    
    appt_q = db.query(func.count(Appointment.appointment_id)).filter(
        Appointment.appointment_date >= today,
        Appointment.status == "Scheduled"
    )
    if hospital_id:
        appt_q = appt_q.filter(Appointment.hospital_id == hospital_id)
    scheduled_appts = appt_q.scalar() or 0
    
    emer_q = db.query(func.count(MedicalRecord.record_id)).filter(
        MedicalRecord.visit_type == "Emergency"
    )
    if hospital_id:
        emer_q = emer_q.filter(MedicalRecord.hospital_id == hospital_id)
    recent_emergency = emer_q.scalar() or 0
    
    return DashboardStats(
        total_patients=total_patients,
        total_records=total_records,
        today_consultations=today_consultations,
        total_beds=total_beds,
        occupied_beds=occupied_beds,
        vacant_beds=vacant_beds,
        cleaning_beds=cleaning_beds,
        bed_occupancy_percent=occupancy_pct,
        waiting_queue_count=waiting_queue,
        scheduled_appointments=scheduled_appts,
        recent_emergency_count=recent_emergency
    )

@router.get("/department-volume")
def get_department_volume(db: Session = Depends(get_db)):
    """Aggregate volume of visits grouped by department."""
    results = db.query(
        MedicalRecord.department,
        func.count(MedicalRecord.record_id)
    ).group_by(MedicalRecord.department).all()
    
    labels = []
    data = []
    for dept, count in results:
        labels.append(dept or "General")
        data.append(count)
        
    return {"labels": labels, "data": data}

@router.get("/hospital-volume")
def get_hospital_volume(db: Session = Depends(get_db)):
    """Aggregate visits grouped by hospital."""
    results = db.query(
        Hospital.hospital_name,
        func.count(MedicalRecord.record_id)
    ).outerjoin(MedicalRecord, Hospital.hospital_id == MedicalRecord.hospital_id)\
     .group_by(Hospital.hospital_id, Hospital.hospital_name).all()
     
    labels = []
    data = []
    for hname, count in results:
        labels.append(hname)
        data.append(count)
        
    return {"labels": labels, "data": data}

@router.get("/reports/csv")
def download_csv_report(
    report_type: str = Query("records", pattern="^(records|beds|appointments)$"),
    hospital_id: int = None,
    db: Session = Depends(get_db)
):
    if report_type == "records":
        csv_data = export_records_csv(db, hospital_id)
        filename = "medilink_clinical_records.csv"
    elif report_type == "beds":
        csv_data = export_bed_utilization_csv(db, hospital_id)
        filename = "medilink_bed_utilization.csv"
    else:
        csv_data = export_appointments_csv(db, hospital_id)
        filename = "medilink_appointments_schedule.csv"
        
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
