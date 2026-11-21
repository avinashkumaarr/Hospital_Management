import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.database import Base

def get_utc_now():
    """Return timezone-aware current UTC time."""
    return datetime.datetime.now(datetime.timezone.utc)

class Hospital(Base):
    __tablename__ = "hospital"
    
    hospital_id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_name = Column(String(100), nullable=False, index=True)
    registration_no = Column(String(50), unique=True, nullable=True)
    hospital_type = Column(String(20), default="Private")
    city = Column(String(50), index=True)
    state = Column(String(50), index=True)
    pincode = Column(String(10), nullable=True)
    contact = Column(String(25), nullable=True)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=get_utc_now)
    
    doctors = relationship("Doctor", back_populates="hospital", cascade="all, delete-orphan")
    records = relationship("MedicalRecord", back_populates="hospital")
    beds = relationship("BedAllocation", back_populates="hospital", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="hospital")
    queue_entries = relationship("OPDQueue", back_populates="hospital")

class Doctor(Base):
    __tablename__ = "doctor"
    
    doctor_id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey("hospital.hospital_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    doctor_name = Column(String(100), nullable=False, index=True)
    specialization = Column(String(50), index=True)
    qualification = Column(String(100), nullable=True)
    license_no = Column(String(30), unique=True, nullable=True)
    contact = Column(String(25), nullable=True)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    
    hospital = relationship("Hospital", back_populates="doctors")
    records = relationship("MedicalRecord", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    queue_entries = relationship("OPDQueue", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patient"
    
    aadhaar_number = Column(String(14), primary_key=True)  # Format: "XXXX XXXX XXXX" or 12 digits
    full_name = Column(String(100), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    blood_group = Column(String(10), nullable=True)
    mobile = Column(String(25), unique=True, nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    emergency_contact = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    
    records = relationship("MedicalRecord", back_populates="patient", cascade="all, delete-orphan", order_by="desc(MedicalRecord.visit_date)")
    lab_reports = relationship("LabReport", back_populates="patient", cascade="all, delete-orphan", order_by="desc(LabReport.report_date)")
    bed_allocations = relationship("BedAllocation", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    queue_entries = relationship("OPDQueue", back_populates="patient", cascade="all, delete-orphan")
    access_logs = relationship("AccessLog", back_populates="patient", cascade="all, delete-orphan")

class MedicalRecord(Base):
    __tablename__ = "medical_record"
    
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    aadhaar_number = Column(String(14), ForeignKey("patient.aadhaar_number", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    hospital_id = Column(Integer, ForeignKey("hospital.hospital_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    visit_date = Column(Date, nullable=False, index=True)
    visit_type = Column(String(50), nullable=False)
    department = Column(String(50), nullable=True)
    chief_complaint = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=False)
    icd10_code = Column(String(20), nullable=True)
    vitals_summary = Column(String(255), nullable=True)
    prescription = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    follow_up_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    
    patient = relationship("Patient", back_populates="records")
    hospital = relationship("Hospital", back_populates="records")
    doctor = relationship("Doctor", back_populates="records")
    lab_reports = relationship("LabReport", back_populates="record", cascade="all, delete-orphan")

class LabReport(Base):
    __tablename__ = "lab_report"
    
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey("medical_record.record_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    aadhaar_number = Column(String(14), ForeignKey("patient.aadhaar_number", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    test_name = Column(String(100), nullable=False, index=True)
    result = Column(Text, nullable=True)
    normal_range = Column(String(50), nullable=True)
    unit = Column(String(20), nullable=True)
    is_abnormal = Column(Boolean, default=False)
    report_date = Column(Date, nullable=False)
    file_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    
    record = relationship("MedicalRecord", back_populates="lab_reports")
    patient = relationship("Patient", back_populates="lab_reports")

class AccessLog(Base):
    __tablename__ = "access_log"
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    aadhaar_number = Column(String(14), ForeignKey("patient.aadhaar_number", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    hospital_id = Column(Integer, ForeignKey("hospital.hospital_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=True)
    accessed_by = Column(String(100), nullable=False)
    access_time = Column(DateTime, default=get_utc_now, index=True)
    purpose = Column(String(150), nullable=True)
    ip_address = Column(String(45), nullable=True)
    status = Column(String(20), default="Authorized")
    
    patient = relationship("Patient", back_populates="access_logs")
    hospital = relationship("Hospital")

class BedAllocation(Base):
    __tablename__ = "bed_allocation"
    
    allocation_id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey("hospital.hospital_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ward_name = Column(String(50), nullable=False)
    bed_number = Column(String(20), nullable=False)
    aadhaar_number = Column(String(14), ForeignKey("patient.aadhaar_number", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    status = Column(String(20), default="Vacant")  # 'Occupied', 'Vacant', 'Cleaning', 'Reserved'
    admitted_at = Column(DateTime, nullable=True)
    expected_discharge = Column(Date, nullable=True)
    
    __table_args__ = (
        UniqueConstraint("hospital_id", "bed_number", name="uk_hospital_bed"),
    )
    
    hospital = relationship("Hospital", back_populates="beds")
    patient = relationship("Patient", back_populates="bed_allocations")

class Appointment(Base):
    __tablename__ = "appointment"
    
    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    aadhaar_number = Column(String(14), ForeignKey("patient.aadhaar_number", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    hospital_id = Column(Integer, ForeignKey("hospital.hospital_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    department = Column(String(50), nullable=True)
    appointment_date = Column(Date, nullable=False, index=True)
    time_slot = Column(String(20), nullable=False)  # e.g. "09:30 AM"
    reason = Column(String(255), nullable=True)
    status = Column(String(20), default="Scheduled")  # Scheduled, Completed, Cancelled, Rescheduled
    created_at = Column(DateTime, default=get_utc_now)
    
    __table_args__ = (
        UniqueConstraint("doctor_id", "appointment_date", "time_slot", name="uk_doctor_slot"),
    )
    
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    hospital = relationship("Hospital", back_populates="appointments")

class OPDQueue(Base):
    __tablename__ = "opd_queue"
    
    queue_id = Column(Integer, primary_key=True, autoincrement=True)
    token_number = Column(String(20), nullable=False, index=True)
    aadhaar_number = Column(String(14), ForeignKey("patient.aadhaar_number", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    hospital_id = Column(Integer, ForeignKey("hospital.hospital_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    queue_date = Column(Date, nullable=False, index=True)
    status = Column(String(20), default="Waiting")  # Waiting, Serving, Completed, Cancelled
    time_issued = Column(String(20), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    patient = relationship("Patient", back_populates="queue_entries")
    doctor = relationship("Doctor", back_populates="queue_entries")
    hospital = relationship("Hospital", back_populates="queue_entries")

class User(Base):
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(30), nullable=False)  # Administrator, Doctor, Receptionist, Emergency Staff
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id", ondelete="SET NULL"), nullable=True)
    hospital_id = Column(Integer, ForeignKey("hospital.hospital_id", ondelete="SET NULL"), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=get_utc_now)

class Notification(Base):
    __tablename__ = "notification"
    
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=True)
    role = Column(String(30), nullable=True)  # Target specific role or user
    title = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(30), default="info")  # info, alert, appointment, bed, queue
    is_read = Column(Boolean, default=False)
    link = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
