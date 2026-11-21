from typing import Optional, List, Any, Dict
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime

# Token & Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
    full_name: str
    doctor_id: Optional[int] = None
    hospital_id: Optional[int] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    role: str
    doctor_id: Optional[int] = None
    hospital_id: Optional[int] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    username: str
    full_name: str
    role: str
    doctor_id: Optional[int] = None
    hospital_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    hospital_name: Optional[str] = None
    is_active: bool
    created_at: datetime

# Hospital & Doctor
class HospitalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    hospital_id: int
    hospital_name: str
    registration_no: Optional[str] = None
    hospital_type: str
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    is_active: bool

class DoctorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    doctor_id: int
    hospital_id: int
    doctor_name: str
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    license_no: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    is_active: bool
    hospital_name: Optional[str] = None

# Lab Report
class LabReportCreate(BaseModel):
    record_id: Optional[int] = None
    aadhaar_number: str
    test_name: str
    result: Optional[str] = None
    normal_range: Optional[str] = None
    unit: Optional[str] = None
    is_abnormal: bool = False
    report_date: date

class LabReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    report_id: int
    record_id: Optional[int] = None
    aadhaar_number: str
    test_name: str
    result: Optional[str] = None
    normal_range: Optional[str] = None
    unit: Optional[str] = None
    is_abnormal: bool
    report_date: date
    file_path: Optional[str] = None
    created_at: datetime
    hospital_name: Optional[str] = None

# Medical Record
class MedicalRecordCreate(BaseModel):
    aadhaar_number: str
    hospital_id: int
    doctor_id: Optional[int] = None
    visit_date: date
    visit_type: str
    department: Optional[str] = None
    chief_complaint: Optional[str] = None
    diagnosis: str
    icd10_code: Optional[str] = None
    vitals_summary: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None

class MedicalRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    record_id: int
    aadhaar_number: str
    hospital_id: int
    doctor_id: Optional[int] = None
    visit_date: date
    visit_type: str
    department: Optional[str] = None
    chief_complaint: Optional[str] = None
    diagnosis: str
    icd10_code: Optional[str] = None
    vitals_summary: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None
    created_at: datetime
    hospital_name: Optional[str] = None
    doctor_name: Optional[str] = None
    lab_reports: List[LabReportOut] = []

# Patient
class PatientCreate(BaseModel):
    aadhaar_number: str
    full_name: str
    date_of_birth: date
    gender: str
    blood_group: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    emergency_contact: Optional[str] = None

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    emergency_contact: Optional[str] = None

class PatientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    aadhaar_number: str
    masked_aadhaar: Optional[str] = None
    full_name: str
    date_of_birth: date
    gender: str
    blood_group: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    emergency_contact: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    records: List[MedicalRecordOut] = []
    lab_reports: List[LabReportOut] = []

# Bed Allocation
class BedAdmitRequest(BaseModel):
    hospital_id: int
    bed_number: str
    aadhaar_number: str
    expected_discharge: Optional[date] = None

class BedStatusUpdate(BaseModel):
    status: str  # Vacant, Occupied, Cleaning, Reserved

class BedOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    allocation_id: int
    hospital_id: int
    ward_name: str
    bed_number: str
    aadhaar_number: Optional[str] = None
    patient_name: Optional[str] = None
    status: str
    admitted_at: Optional[datetime] = None
    expected_discharge: Optional[date] = None
    hospital_name: Optional[str] = None

# Appointment
class AppointmentCreate(BaseModel):
    aadhaar_number: str
    doctor_id: int
    hospital_id: int
    department: Optional[str] = None
    appointment_date: date
    time_slot: str
    reason: Optional[str] = None

class AppointmentReschedule(BaseModel):
    appointment_date: date
    time_slot: str
    reason: Optional[str] = None

class AppointmentStatusUpdate(BaseModel):
    status: str  # Scheduled, Completed, Cancelled, Rescheduled

class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    appointment_id: int
    aadhaar_number: str
    patient_name: Optional[str] = None
    doctor_id: int
    doctor_name: Optional[str] = None
    hospital_id: int
    hospital_name: Optional[str] = None
    department: Optional[str] = None
    appointment_date: date
    time_slot: str
    reason: Optional[str] = None
    status: str
    created_at: datetime

# OPD Queue
class QueueIssueRequest(BaseModel):
    aadhaar_number: str
    doctor_id: Optional[int] = None
    hospital_id: int

class QueueStatusUpdate(BaseModel):
    status: str  # Waiting, Serving, Completed, Cancelled

class QueueOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    queue_id: int
    token_number: str
    aadhaar_number: str
    patient_name: Optional[str] = None
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None
    hospital_id: int
    hospital_name: Optional[str] = None
    queue_date: date
    status: str
    time_issued: str
    completed_at: Optional[datetime] = None

# Audit Log
class AuditLogCreate(BaseModel):
    aadhaar_number: str
    hospital_id: Optional[int] = None
    purpose: str

class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    log_id: int
    aadhaar_number: str
    masked_aadhaar: Optional[str] = None
    hospital_id: Optional[int] = None
    hospital_name: Optional[str] = None
    accessed_by: str
    access_time: datetime
    purpose: Optional[str] = None
    ip_address: Optional[str] = None
    status: str

# Notifications
class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    notification_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    link: Optional[str] = None
    created_at: datetime

# Dashboard Stats
class DashboardStats(BaseModel):
    total_patients: int
    total_records: int
    today_consultations: int
    total_beds: int
    occupied_beds: int
    vacant_beds: int
    cleaning_beds: int
    bed_occupancy_percent: float
    waiting_queue_count: int
    scheduled_appointments: int
    recent_emergency_count: int
