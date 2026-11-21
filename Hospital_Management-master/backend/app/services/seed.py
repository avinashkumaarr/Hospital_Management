import datetime
import logging
from sqlalchemy.orm import Session
from backend.app.models.entities import (
    Hospital, Doctor, Patient, MedicalRecord, LabReport,
    BedAllocation, OPDQueue, AccessLog, User, Appointment, Notification
)
from backend.app.security import hash_password

logger = logging.getLogger("medilink.seed")

def seed_database_if_empty(db: Session):
    """Seed initial data idempotently into database."""
    # Check if hospitals exist
    if db.query(Hospital).count() > 0:
        logger.info("Database already initialized with data. Skipping default seed.")
        ensure_demo_users(db)
        return

    logger.info("Initializing fresh database with standard clinical seed data...")

    # 1. Hospitals
    hospitals_data = [
        Hospital(hospital_id=1, hospital_name="AIIMS Delhi", registration_no="REG-AIIMS-001", hospital_type="Government", city="New Delhi", state="Delhi", pincode="110029", contact="011-26588500", email="director@aiims.edu"),
        Hospital(hospital_id=2, hospital_name="Apollo Hospitals", registration_no="REG-APL-002", hospital_type="Private", city="New Delhi", state="Delhi", pincode="110076", contact="011-26925858", email="helpdesk@apollo.com"),
        Hospital(hospital_id=3, hospital_name="Fortis Healthcare", registration_no="REG-FRT-003", hospital_type="Private", city="Gurugram", state="Haryana", pincode="122002", contact="0124-4921021", email="care@fortis.com"),
        Hospital(hospital_id=4, hospital_name="Max Super Speciality", registration_no="REG-MAX-004", hospital_type="Private", city="New Delhi", state="Delhi", pincode="110017", contact="011-26515050", email="support@maxhealthcare.com"),
        Hospital(hospital_id=5, hospital_name="PGIMER Chandigarh", registration_no="REG-PGI-005", hospital_type="Government", city="Chandigarh", state="Chandigarh", pincode="160012", contact="0172-2746018", email="admin@pgimer.edu.in"),
        Hospital(hospital_id=6, hospital_name="Manipal Hospital", registration_no="REG-MAN-006", hospital_type="Private", city="Bengaluru", state="Karnataka", pincode="560017", contact="080-25024444", email="info@manipalhospitals.com")
    ]
    for h in hospitals_data:
        db.merge(h)
    db.commit()

    # 2. Doctors
    doctors_data = [
        Doctor(doctor_id=1, hospital_id=1, doctor_name="Dr. Ramesh Gupta", specialization="Cardiology", qualification="MBBS, MD, DM (Cardio)", license_no="DMC-CARD-1049", contact="9811122334", email="ramesh.gupta@aiims.edu"),
        Doctor(doctor_id=2, hospital_id=2, doctor_name="Dr. Anita Verma", specialization="General Medicine", qualification="MBBS, MD (Internal Med)", license_no="DMC-GEN-2201", contact="9822233445", email="anita.verma@apollo.com"),
        Doctor(doctor_id=3, hospital_id=3, doctor_name="Dr. Sanjay Mehta", specialization="Pathology", qualification="MBBS, MD (Pathology)", license_no="HMC-PATH-9811", contact="9833344556", email="sanjay.mehta@fortis.com"),
        Doctor(doctor_id=4, hospital_id=4, doctor_name="Dr. Vikram Singh", specialization="Orthopaedics", qualification="MBBS, MS (Orthopaedics)", license_no="DMC-ORTH-5541", contact="9844455667", email="vikram.singh@max.com"),
        Doctor(doctor_id=5, hospital_id=5, doctor_name="Dr. Priya Nair", specialization="Neurology", qualification="MBBS, MD, DM (Neuro)", license_no="PMC-NEUR-7782", contact="9855566778", email="priya.nair@pgimer.edu.in"),
        Doctor(doctor_id=6, hospital_id=6, doctor_name="Dr. Rajesh Kulkarni", specialization="Emergency Medicine", qualification="MBBS, MD (Emergency)", license_no="KMC-EMER-3390", contact="9866677889", email="rajesh.k@manipal.com")
    ]
    for d in doctors_data:
        db.merge(d)
    db.commit()

    # 3. Patients
    patients_data = [
        Patient(aadhaar_number="2345 6789 0123", full_name="Priya Sharma", date_of_birth=datetime.date(1990, 5, 14), gender="Female", blood_group="B+", mobile="+91 98765 43210", email="priya.sharma@gmail.com", address="B-14, Sector 62, Noida, Uttar Pradesh", allergies="Penicillin, Amoxicillin", chronic_conditions="Hypertension (Grade 1)", emergency_contact="Sunil Sharma (Husband): +91 98765 43219"),
        Patient(aadhaar_number="1111 2222 3333", full_name="Arjun Kapoor", date_of_birth=datetime.date(1985, 11, 30), gender="Male", blood_group="O+", mobile="+91 77777 88888", email="arjun.kapoor@outlook.com", address="Flat 402, Palm Heights, Gurugram, Haryana", allergies="Sulfa drugs, Septra", chronic_conditions="Type-2 Diabetes Mellitus", emergency_contact="Renu Kapoor (Wife): +91 77777 88889"),
        Patient(aadhaar_number="9999 8888 7777", full_name="Meera Iyer", date_of_birth=datetime.date(2001, 3, 22), gender="Female", blood_group="A+", mobile="+91 99001 12233", email="meera.iyer@gmail.com", address="12/4 Indiranagar, Bengaluru, Karnataka", allergies="None", chronic_conditions="None", emergency_contact="K. Iyer (Father): +91 99001 12244"),
        Patient(aadhaar_number="5555 6666 7777", full_name="Rajesh Verma", date_of_birth=datetime.date(1968, 8, 19), gender="Male", blood_group="AB+", mobile="+91 98123 45678", email="rajesh.verma@corp.in", address="77 Civil Lines, New Delhi", allergies="Aspirin, Ibuprofen (NSAIDs)", chronic_conditions="Coronary Artery Disease", emergency_contact="Anita Verma (Wife): +91 98123 45679"),
        Patient(aadhaar_number="4444 3333 2222", full_name="Ananya Patel", date_of_birth=datetime.date(1995, 12, 4), gender="Female", blood_group="O-", mobile="+91 97654 32100", email="ananya.p@design.io", address="201 Sunrise Apts, Chandigarh", allergies="Latex", chronic_conditions="Bronchial Asthma", emergency_contact="Deepak Patel (Brother): +91 97654 32101")
    ]
    for p in patients_data:
        db.merge(p)
    db.commit()

    # 4. Medical Records
    records_data = [
        MedicalRecord(record_id=1, aadhaar_number="2345 6789 0123", hospital_id=2, doctor_id=2, visit_date=datetime.date(2024, 1, 10), visit_type="OPD Consultation", department="Cardiology", chief_complaint="Persistent headaches, evening dizziness", diagnosis="Essential Hypertension (Grade 1)", icd10_code="I10", vitals_summary="BP: 145/95 mmHg, HR: 82 bpm, SpO2: 98%, Temp: 98.4°F", prescription="Tab Amlodipine 5mg OD morning x 30 days\nLow sodium diet (< 2g/day)\n30 min daily brisk aerobic walking", notes="Patient presented with tension headaches. Fundoscopy normal. Advised home BP monitoring.", follow_up_date=datetime.date(2024, 2, 10)),
        MedicalRecord(record_id=2, aadhaar_number="2345 6789 0123", hospital_id=1, doctor_id=1, visit_date=datetime.date(2023, 7, 22), visit_type="Routine Checkup", department="General Medicine", chief_complaint="Executive annual checkup", diagnosis="Vitamin D Deficiency", icd10_code="E55.9", vitals_summary="BP: 128/84 mmHg, HR: 74 bpm, SpO2: 99%, Temp: 98.6°F", prescription="Cap Vitamin D3 60,000 IU weekly x 8 weeks, then monthly", notes="Annual executive screening. Mild fatigue reported. Metabolic parameters normal.", follow_up_date=datetime.date(2024, 1, 20)),
        MedicalRecord(record_id=3, aadhaar_number="2345 6789 0123", hospital_id=3, doctor_id=3, visit_date=datetime.date(2022, 3, 5), visit_type="Lab Tests", department="Pathology", chief_complaint="Routine health screening panel", diagnosis="Borderline Dyslipidemia", icd10_code="E78.5", vitals_summary="BP: 130/85 mmHg, HR: 76 bpm, SpO2: 98%, Temp: 98.2°F", prescription="Dietary modifications, reduce saturated fats, retest lipid profile in 6 months", notes="Lipid panel demonstrated mild LDL elevation.", follow_up_date=datetime.date(2022, 9, 5)),
        MedicalRecord(record_id=4, aadhaar_number="1111 2222 3333", hospital_id=4, doctor_id=4, visit_date=datetime.date(2024, 3, 18), visit_type="Surgery", department="Orthopaedics", chief_complaint="Right knee lock and acute pain after sports injury", diagnosis="Meniscus Tear (Right Knee) - Post Arthroscopy", icd10_code="M23.22", vitals_summary="BP: 122/80 mmHg, HR: 78 bpm, SpO2: 99%, Temp: 98.6°F", prescription="Tab Paracetamol 650mg TDS PRN, Ice pack application, Physiotherapy 3x/week x 6 weeks", notes="Arthroscopic partial meniscectomy performed uneventfully.", follow_up_date=datetime.date(2024, 4, 15)),
        MedicalRecord(record_id=5, aadhaar_number="1111 2222 3333", hospital_id=6, doctor_id=6, visit_date=datetime.date(2023, 12, 1), visit_type="Emergency", department="Emergency Medicine", chief_complaint="Severe abdominal cramps, vomiting and dehydration", diagnosis="Acute Gastroenteritis with Moderate Dehydration", icd10_code="A09", vitals_summary="BP: 105/70 mmHg, HR: 102 bpm, SpO2: 98%, Temp: 99.1°F", prescription="IV Normal Saline 1000ml stat, Tab Ondansetron 4mg TDS, ORS sachet ad libitum", notes="Patient stabilized in emergency bay and discharged same evening.", follow_up_date=datetime.date(2023, 12, 7)),
        MedicalRecord(record_id=6, aadhaar_number="5555 6666 7777", hospital_id=1, doctor_id=1, visit_date=datetime.date(2024, 2, 14), visit_type="Emergency", department="Cardiology", chief_complaint="Substernal crushing chest pain radiating to left arm", diagnosis="Acute Coronary Syndrome (NSTEMI)", icd10_code="I21.4", vitals_summary="BP: 160/100 mmHg, HR: 110 bpm, SpO2: 94%, Temp: 98.4°F", prescription="Tab Clopidogrel 300mg stat, Tab Atorvastatin 80mg, Sublingual Nitroglycerin 0.5mg PRN", notes="Emergency angiogram revealed LAD 70% stenosis. Stent placed successfully.", follow_up_date=datetime.date(2024, 3, 1)),
        MedicalRecord(record_id=7, aadhaar_number="4444 3333 2222", hospital_id=5, doctor_id=5, visit_date=datetime.date(2024, 1, 28), visit_type="OPD Consultation", department="Pulmonology", chief_complaint="Exertional wheezing and nocturnal dry cough", diagnosis="Bronchial Asthma (Moderate Persistent)", icd10_code="J45.40", vitals_summary="BP: 118/76 mmHg, HR: 88 bpm, SpO2: 95%, Temp: 98.6°F", prescription="Budesonide + Formoterol Inhaler 200/6mcg 2 puffs BD, Tab Montelukast 10mg OD HS", notes="Asthma Action Plan reviewed. Advised to avoid dust and latex gloves.", follow_up_date=datetime.date(2024, 4, 28))
    ]
    for r in records_data:
        db.merge(r)
    db.commit()

    # 5. Lab Reports
    labs_data = [
        LabReport(report_id=1, record_id=1, aadhaar_number="2345 6789 0123", test_name="Serum Creatinine", result="0.9", normal_range="0.6 - 1.2", unit="mg/dL", is_abnormal=False, report_date=datetime.date(2024, 1, 11)),
        LabReport(report_id=2, record_id=1, aadhaar_number="2345 6789 0123", test_name="Serum Potassium", result="4.2", normal_range="3.5 - 5.0", unit="mEq/L", is_abnormal=False, report_date=datetime.date(2024, 1, 11)),
        LabReport(report_id=3, record_id=2, aadhaar_number="2345 6789 0123", test_name="Serum 25-OH Vitamin D", result="14.2", normal_range="30.0 - 100.0", unit="ng/mL", is_abnormal=True, report_date=datetime.date(2023, 7, 23)),
        LabReport(report_id=4, record_id=3, aadhaar_number="2345 6789 0123", test_name="HbA1c (Glycated Hb)", result="5.6", normal_range="< 5.7", unit="%", is_abnormal=False, report_date=datetime.date(2022, 3, 6)),
        LabReport(report_id=5, record_id=3, aadhaar_number="2345 6789 0123", test_name="Total Cholesterol", result="228", normal_range="< 200", unit="mg/dL", is_abnormal=True, report_date=datetime.date(2022, 3, 6)),
        LabReport(report_id=6, record_id=3, aadhaar_number="2345 6789 0123", test_name="LDL Cholesterol", result="148", normal_range="< 100", unit="mg/dL", is_abnormal=True, report_date=datetime.date(2022, 3, 6)),
        LabReport(report_id=7, record_id=4, aadhaar_number="1111 2222 3333", test_name="Knee MRI Scan (Right)", result="Complex tear posterior horn medial meniscus", normal_range="Intact meniscus", unit="Imaging", is_abnormal=True, report_date=datetime.date(2024, 3, 16)),
        LabReport(report_id=8, record_id=5, aadhaar_number="1111 2222 3333", test_name="Serum Electrolytes (Sodium)", result="132", normal_range="136 - 145", unit="mEq/L", is_abnormal=True, report_date=datetime.date(2023, 12, 1)),
        LabReport(report_id=9, record_id=6, aadhaar_number="5555 6666 7777", test_name="Cardiac Troponin-I", result="0.84", normal_range="< 0.04", unit="ng/mL", is_abnormal=True, report_date=datetime.date(2024, 2, 14)),
        LabReport(report_id=10, record_id=6, aadhaar_number="5555 6666 7777", test_name="12-Lead ECG", result="ST segment depression in V4-V6", normal_range="Normal Sinus Rhythm", unit="ECG", is_abnormal=True, report_date=datetime.date(2024, 2, 14)),
        LabReport(report_id=11, record_id=7, aadhaar_number="4444 3333 2222", test_name="Spirometry (FEV1/FVC)", result="68%", normal_range="> 75%", unit="%", is_abnormal=True, report_date=datetime.date(2024, 1, 29))
    ]
    for l in labs_data:
        db.merge(l)
    db.commit()

    # 6. Bed Allocations (Clean, strictly 1 bed per patient to fix the bug)
    beds_data = [
        BedAllocation(allocation_id=1, hospital_id=1, ward_name="Emergency Trauma Bay", bed_number="ER-101", aadhaar_number="5555 6666 7777", status="Occupied", admitted_at=datetime.datetime(2024, 2, 14, 2, 30), expected_discharge=datetime.date(2024, 2, 18)),
        BedAllocation(allocation_id=2, hospital_id=1, ward_name="Emergency Trauma Bay", bed_number="ER-102", aadhaar_number=None, status="Vacant"),
        BedAllocation(allocation_id=3, hospital_id=1, ward_name="Emergency Trauma Bay", bed_number="ER-103", aadhaar_number=None, status="Cleaning"),
        BedAllocation(allocation_id=4, hospital_id=1, ward_name="Emergency Trauma Bay", bed_number="ER-104", aadhaar_number=None, status="Vacant"),
        BedAllocation(allocation_id=5, hospital_id=1, ward_name="Intensive Care Unit", bed_number="ICU-201", aadhaar_number=None, status="Vacant"),
        BedAllocation(allocation_id=6, hospital_id=1, ward_name="Intensive Care Unit", bed_number="ICU-202", aadhaar_number=None, status="Vacant"),
        BedAllocation(allocation_id=7, hospital_id=2, ward_name="Cardiac HDU", bed_number="HDU-301", aadhaar_number="2345 6789 0123", status="Occupied", admitted_at=datetime.datetime(2024, 1, 10, 11, 0), expected_discharge=datetime.date(2024, 1, 12)),
        BedAllocation(allocation_id=8, hospital_id=2, ward_name="Cardiac HDU", bed_number="HDU-302", aadhaar_number=None, status="Vacant"),
        BedAllocation(allocation_id=9, hospital_id=4, ward_name="Surgical Post-Op Ward", bed_number="SPW-401", aadhaar_number="1111 2222 3333", status="Occupied", admitted_at=datetime.datetime(2024, 3, 18, 14, 0), expected_discharge=datetime.date(2024, 3, 21)),
        BedAllocation(allocation_id=10, hospital_id=4, ward_name="Surgical Post-Op Ward", bed_number="SPW-402", aadhaar_number=None, status="Vacant"),
        BedAllocation(allocation_id=11, hospital_id=4, ward_name="Surgical Post-Op Ward", bed_number="SPW-403", aadhaar_number=None, status="Vacant"),
        BedAllocation(allocation_id=12, hospital_id=6, ward_name="Acute Medical Care", bed_number="AMC-501", aadhaar_number=None, status="Vacant")
    ]
    for b in beds_data:
        db.merge(b)
    db.commit()

    # 7. OPD Queue
    today = datetime.date.today()
    queue_data = [
        OPDQueue(queue_id=1, token_number="A-101", aadhaar_number="2345 6789 0123", doctor_id=1, hospital_id=1, queue_date=today, status="Serving", time_issued="10:15 AM"),
        OPDQueue(queue_id=2, token_number="A-102", aadhaar_number="1111 2222 3333", doctor_id=4, hospital_id=4, queue_date=today, status="Waiting", time_issued="10:25 AM"),
        OPDQueue(queue_id=3, token_number="A-103", aadhaar_number="4444 3333 2222", doctor_id=5, hospital_id=5, queue_date=today, status="Waiting", time_issued="10:35 AM"),
        OPDQueue(queue_id=4, token_number="A-104", aadhaar_number="9999 8888 7777", doctor_id=2, hospital_id=2, queue_date=today, status="Waiting", time_issued="10:45 AM")
    ]
    for q in queue_data:
        db.merge(q)
    db.commit()

    # 8. Appointments
    appt_data = [
        Appointment(appointment_id=1, aadhaar_number="2345 6789 0123", doctor_id=1, hospital_id=1, department="Cardiology", appointment_date=today, time_slot="11:30 AM", reason="Hypertension Follow-up", status="Scheduled"),
        Appointment(appointment_id=2, aadhaar_number="1111 2222 3333", doctor_id=4, hospital_id=4, department="Orthopaedics", appointment_date=today, time_slot="02:00 PM", reason="Post-Knee Arthroscopy Evaluation", status="Scheduled"),
        Appointment(appointment_id=3, aadhaar_number="4444 3333 2222", doctor_id=5, hospital_id=5, department="Neurology", appointment_date=today + datetime.timedelta(days=1), time_slot="10:00 AM", reason="Asthma & Migraine Review", status="Scheduled"),
        Appointment(appointment_id=4, aadhaar_number="9999 8888 7777", doctor_id=2, hospital_id=2, department="General Medicine", appointment_date=today + datetime.timedelta(days=2), time_slot="03:30 PM", reason="Annual Wellness Check", status="Scheduled")
    ]
    for a in appt_data:
        db.merge(a)
    db.commit()

    # 9. Access Logs
    logs_data = [
        AccessLog(log_id=1, aadhaar_number="2345 6789 0123", hospital_id=2, accessed_by="Dr. Anita Verma (Apollo)", access_time=datetime.datetime(2024, 1, 10, 10, 14), purpose="OPD Cardiology Consultation", ip_address="127.0.0.1", status="Authorized"),
        AccessLog(log_id=2, aadhaar_number="2345 6789 0123", hospital_id=1, accessed_by="Dr. Ramesh Gupta (AIIMS)", access_time=datetime.datetime(2023, 7, 22, 9, 30), purpose="Routine Health Checkup", ip_address="127.0.0.1", status="Authorized"),
        AccessLog(log_id=3, aadhaar_number="1111 2222 3333", hospital_id=4, accessed_by="Dr. Vikram Singh (Max)", access_time=datetime.datetime(2024, 3, 18, 11, 0), purpose="Pre-Operative Ortho Review", ip_address="127.0.0.1", status="Authorized"),
        AccessLog(log_id=4, aadhaar_number="5555 6666 7777", hospital_id=1, accessed_by="Dr. Ramesh Gupta (AIIMS)", access_time=datetime.datetime(2024, 2, 14, 2, 45), purpose="Break-Glass Emergency Resuscitation", ip_address="127.0.0.1", status="Authorized")
    ]
    for l in logs_data:
        db.merge(l)
    db.commit()

    # 10. Initial Notifications
    notifs_data = [
        Notification(title="OPD Queue Active", message="Today's OPD queue is active with 4 scheduled patients.", notification_type="queue", is_read=False),
        Notification(title="Bed Availability", message="Emergency Bay ER-103 marked for sanitization.", notification_type="bed", is_read=False),
        Notification(title="System Ready", message="MediLink v3.0 Relational Healthcare System is online.", notification_type="info", is_read=False)
    ]
    for n in notifs_data:
        db.add(n)
    db.commit()

    ensure_demo_users(db)
    logger.info("Database seeding complete!")

def ensure_demo_users(db: Session):
    """Ensure standard demo accounts exist for testing all 4 roles."""
    roles = [
        ("admin", "admin123", "System Administrator", "Administrator", None, 1),
        ("doctor", "doctor123", "Dr. Ramesh Gupta", "Doctor", 1, 1),
        ("receptionist", "reception123", "Sunita Rao", "Receptionist", None, 1),
        ("emergency", "emergency123", "Trauma Unit Lead", "Emergency Staff", 6, 1),
    ]
    for username, pwd, name, role, doc_id, hosp_id in roles:
        existing = db.query(User).filter(User.username == username).first()
        if not existing:
            u = User(
                username=username,
                password_hash=hash_password(pwd),
                full_name=name,
                role=role,
                doctor_id=doc_id,
                hospital_id=hosp_id,
                is_active=True
            )
            db.add(u)
    db.commit()
