import pytest
import datetime
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models.entities import Patient, MedicalRecord, BedAllocation, Appointment, OPDQueue

client = TestClient(app)

def test_full_e2e_20_workflows():
    # 1. Log in as authorized user
    res_login = client.post("/api/auth/login", json={"username": "doctor", "password": "doctor123"})
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Register a new patient
    new_aadhaar = "7777 8888 9999"
    # Clean up if prior run
    db = SessionLocal()
    db.query(OPDQueue).filter(OPDQueue.aadhaar_number == new_aadhaar).delete()
    db.query(Appointment).filter(Appointment.aadhaar_number == new_aadhaar).delete()
    db.query(MedicalRecord).filter(MedicalRecord.aadhaar_number == new_aadhaar).delete()
    p_exist = db.query(Patient).filter(Patient.aadhaar_number == new_aadhaar).first()
    if p_exist:
        db.delete(p_exist)
    db.commit()
    db.close()

    res_reg = client.post("/api/patients", json={
        "aadhaar_number": "777788889999",
        "full_name": "Rohan Malhotra",
        "date_of_birth": "1994-06-20",
        "gender": "Male",
        "blood_group": "B+",
        "mobile": "+91 98888 77777",
        "email": "rohan.m@example.com",
        "address": "88 Civil Lines, Jaipur",
        "allergies": "Penicillin",
        "chronic_conditions": "None",
        "emergency_contact": "Anita Malhotra: 9888877778"
    }, headers=headers)
    assert res_reg.status_code == 201
    assert res_reg.json()["aadhaar_number"] == new_aadhaar

    # 3. Find the registered patient
    res_find = client.get(f"/api/patients/{new_aadhaar}", headers=headers)
    assert res_find.status_code == 200
    assert res_find.json()["full_name"] == "Rohan Malhotra"

    # 4. Create a consultation
    consultation = {
        "aadhaar_number": new_aadhaar,
        "hospital_id": 1,
        "doctor_id": 1,
        "visit_date": datetime.date.today().isoformat(),
        "visit_type": "OPD Consultation",
        "department": "Cardiology",
        "chief_complaint": "Chest flutter during exertion",
        "diagnosis": "Sinus Tachycardia",
        "icd10_code": "R00.0",
        "vitals_summary": "BP: 132/86 mmHg, HR: 108 bpm, SpO2: 98%, Temp: 98.6°F",
        "prescription": "Tab Metoprolol 25mg OD morning x 14 days\nAdequate hydration",
        "notes": "Patient advised to reduce stress and monitor pulse.",
        "follow_up_date": (datetime.date.today() + datetime.timedelta(days=14)).isoformat()
    }
    res_enc = client.post("/api/records", json=consultation, headers=headers)
    assert res_enc.status_code == 201
    rec_id = res_enc.json()["record_id"]

    # 5 & 6. Verify encounter persists and still exists on retrieve
    res_rec = client.get(f"/api/records/{rec_id}", headers=headers)
    assert res_rec.status_code == 200
    assert res_rec.json()["diagnosis"] == "Sinus Tachycardia"

    # 7. Display actual saved vitals
    patient_fresh = client.get(f"/api/patients/{new_aadhaar}", headers=headers).json()
    assert len(patient_fresh["records"]) >= 1
    assert "BP: 132/86" in patient_fresh["records"][0]["vitals_summary"]

    # 8. Filtered timeline & prescription slip uses permanent record ID
    # Testing that record_id retrieved corresponds exactly to the consultation
    assert patient_fresh["records"][0]["record_id"] == rec_id

    # 9. Book and reschedule an appointment
    appt_date = (datetime.date.today() + datetime.timedelta(days=3)).isoformat()
    res_appt = client.post("/api/appointments", json={
        "aadhaar_number": new_aadhaar,
        "doctor_id": 1,
        "hospital_id": 1,
        "department": "Cardiology",
        "appointment_date": appt_date,
        "time_slot": "10:00 AM",
        "reason": "Cardiology Followup"
    }, headers=headers)
    assert res_appt.status_code == 201
    appt_id = res_appt.json()["appointment_id"]

    # 10. Prevent duplicate appointment slots
    res_dup_slot = client.post("/api/appointments", json={
        "aadhaar_number": "2345 6789 0123",
        "doctor_id": 1,
        "hospital_id": 1,
        "department": "Cardiology",
        "appointment_date": appt_date,
        "time_slot": "10:00 AM",
        "reason": "Conflict check"
    }, headers=headers)
    assert res_dup_slot.status_code == 409

    # Reschedule appointment
    res_resched = client.put(f"/api/appointments/{appt_id}/reschedule", json={
        "appointment_date": (datetime.date.today() + datetime.timedelta(days=4)).isoformat(),
        "time_slot": "11:00 AM",
        "reason": "Patient requested later date"
    }, headers=headers)
    assert res_resched.status_code == 200
    assert res_resched.json()["status"] == "Rescheduled"

    # 11. Admit patient to vacant bed
    res_admit = client.post("/api/beds/admit", json={
        "hospital_id": 1,
        "bed_number": "ER-104",
        "aadhaar_number": new_aadhaar,
        "expected_discharge": (datetime.date.today() + datetime.timedelta(days=2)).isoformat()
    }, headers=headers)
    assert res_admit.status_code == 200
    alloc_id = res_admit.json()["allocation_id"]

    # 12. Prevent duplicate bed assignment (patient already has active bed)
    res_dup_bed = client.post("/api/beds/admit", json={
        "hospital_id": 1,
        "bed_number": "ICU-202",
        "aadhaar_number": new_aadhaar
    }, headers=headers)
    assert res_dup_bed.status_code == 400

    # 13. Discharge patient -> Bed becomes Cleaning, then Mark Cleaned -> Bed becomes Vacant
    res_disch = client.post(f"/api/beds/{alloc_id}/discharge", headers=headers)
    assert res_disch.status_code == 200
    assert res_disch.json()["status"] == "Cleaning"

    res_clean = client.post(f"/api/beds/{alloc_id}/clean", headers=headers)
    assert res_clean.status_code == 200
    assert res_clean.json()["status"] == "Vacant"

    # 14. Issue unique OPD token
    res_token = client.post("/api/queue/issue", json={
        "aadhaar_number": new_aadhaar,
        "doctor_id": 1,
        "hospital_id": 1
    }, headers=headers)
    assert res_token.status_code == 201
    q_id = res_token.json()["queue_id"]
    assert res_token.json()["token_number"].startswith("A-")

    # 15. Complete and recall queue tokens
    res_serving = client.put(f"/api/queue/{q_id}/status", json={"status": "Serving"}, headers=headers)
    assert res_serving.status_code == 200
    res_done = client.put(f"/api/queue/{q_id}/status", json={"status": "Completed"}, headers=headers)
    assert res_done.status_code == 200
    assert res_done.json()["status"] == "Completed"

    # 16. Add and retrieve lab report
    res_lab = client.post("/api/labs", json={
        "record_id": rec_id,
        "aadhaar_number": new_aadhaar,
        "test_name": "Serum Magnesium",
        "result": "2.1",
        "normal_range": "1.7 - 2.2",
        "unit": "mg/dL",
        "is_abnormal": False,
        "report_date": datetime.date.today().isoformat()
    }, headers=headers)
    assert res_lab.status_code == 201

    # 17. Generate analytics from real records
    res_analytics = client.get("/api/analytics/dashboard", headers=headers)
    assert res_analytics.status_code == 200
    assert res_analytics.json()["total_patients"] >= 6

    # 18. Verify authorization and audit records
    res_audit = client.get(f"/api/audit?aadhaar={new_aadhaar}", headers=headers)
    assert res_audit.status_code == 200
    assert len(res_audit.json()) >= 1

    # 19. Execute approved read-only SQL demo queries
    res_q1 = client.post("/api/sql/execute", json={"query_key": "Q1", "param": new_aadhaar}, headers=headers)
    assert res_q1.status_code == 200
    assert res_q1.json()["row_count"] >= 1

    # 20. Check health endpoint
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"
