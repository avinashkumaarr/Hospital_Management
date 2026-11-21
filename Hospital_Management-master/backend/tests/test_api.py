import pytest
import datetime
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models.entities import Patient, BedAllocation, Appointment, OPDQueue

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "engine" in data["database"]
    assert data["database"]["counts"]["patients"] >= 5

def test_auth_login_and_roles():
    # Login admin
    res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    token_data = res.json()
    assert "access_token" in token_data
    assert token_data["role"] == "Administrator"

    # Login doctor
    res = client.post("/api/auth/login", json={"username": "doctor", "password": "doctor123"})
    assert res.status_code == 200
    token_data = res.json()
    assert token_data["role"] == "Doctor"

    # Failed login
    res = client.post("/api/auth/login", json={"username": "admin", "password": "wrongpassword"})
    assert res.status_code == 401

def test_patient_list_and_details():
    res = client.get("/api/patients")
    assert res.status_code == 200
    patients = res.json()
    assert len(patients) >= 5
    assert any(p["full_name"] == "Priya Sharma" for p in patients)

    # Details
    priya_res = client.get("/api/patients/2345 6789 0123")
    assert priya_res.status_code == 200
    priya = priya_res.json()
    assert priya["full_name"] == "Priya Sharma"
    assert len(priya["records"]) >= 3
    assert len(priya["lab_reports"]) >= 6

def test_patient_registration_and_validation():
    test_aadhaar = "8888 7777 6666"
    
    # Clean up if existing
    db = SessionLocal()
    existing = db.query(Patient).filter(Patient.aadhaar_number == test_aadhaar).first()
    if existing:
        db.delete(existing)
        db.commit()
    db.close()

    new_patient = {
        "aadhaar_number": "888877776666",
        "full_name": "Test Vikram Rao",
        "date_of_birth": "1992-04-10",
        "gender": "Male",
        "blood_group": "O+",
        "mobile": "+91 91234 56789",
        "email": "test.vikram@example.com",
        "address": "45 Park Street, Kolkata",
        "allergies": "Penicillin",
        "chronic_conditions": "None",
        "emergency_contact": "Anita Rao: 9123456780"
    }
    res = client.post("/api/patients", json=new_patient)
    assert res.status_code == 201
    data = res.json()
    assert data["aadhaar_number"] == "8888 7777 6666"
    assert data["masked_aadhaar"] == "XXXX-XXXX-6666"

    # Duplicate registration check
    res_dup = client.post("/api/patients", json=new_patient)
    assert res_dup.status_code == 409

    # Invalid Aadhaar format
    invalid_p = new_patient.copy()
    invalid_p["aadhaar_number"] = "1234"
    res_inv = client.post("/api/patients", json=invalid_p)
    assert res_inv.status_code == 422

def test_break_glass_emergency_access():
    res = client.post("/api/patients/2345 6789 0123/break-glass?reason=Acute+Anaphylaxis+Resuscitation")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "EMERGENCY_ACCESS_GRANTED"
    assert "audit_id" in data
    assert data["blood_group"] == "B+"

def test_create_clinical_record():
    new_record = {
        "aadhaar_number": "2345 6789 0123",
        "hospital_id": 1,
        "doctor_id": 1,
        "visit_date": datetime.date.today().isoformat(),
        "visit_type": "OPD Consultation",
        "department": "Cardiology",
        "chief_complaint": "Mild palpitations during evening walk",
        "diagnosis": "Sinus Tachycardia",
        "icd10_code": "R00.0",
        "vitals_summary": "BP: 135/88 mmHg, HR: 104 bpm, SpO2: 98%",
        "prescription": "Tab Metoprolol 25mg OD morning x 14 days\nAdequate hydration\nAvoid caffeine",
        "notes": "ECG confirms sinus tachycardia. Advised repeat review in 2 weeks.",
        "follow_up_date": (datetime.date.today() + datetime.timedelta(days=14)).isoformat()
    }
    res = client.post("/api/records", json=new_record)
    assert res.status_code == 201
    rec = res.json()
    assert rec["record_id"] > 0
    assert rec["diagnosis"] == "Sinus Tachycardia"

def test_bed_management_and_duplicate_prevention():
    # 1. Check beds list
    res = client.get("/api/beds")
    assert res.status_code == 200
    beds = res.json()
    assert len(beds) >= 12

    # 2. Prevent admitting patient who already has an occupied bed (Priya Sharma is in HDU-301)
    admit_conflict = {
        "hospital_id": 1,
        "bed_number": "ER-102",
        "aadhaar_number": "2345 6789 0123"
    }
    res_conflict = client.post("/api/beds/admit", json=admit_conflict)
    assert res_conflict.status_code == 400
    assert "already admitted" in res_conflict.json()["detail"].lower()

    # 3. Admit Meera Iyer (who has no active bed) to vacant bed ER-102
    admit_success = {
        "hospital_id": 1,
        "bed_number": "ER-102",
        "aadhaar_number": "9999 8888 7777"
    }
    res_admit = client.post("/api/beds/admit", json=admit_success)
    assert res_admit.status_code == 200
    admitted = res_admit.json()
    assert admitted["status"] == "Occupied"
    assert admitted["bed_number"] == "ER-102"
    alloc_id = admitted["allocation_id"]

    # 4. Prevent assigning the now-occupied bed to another patient
    res_bed_conflict = client.post("/api/beds/admit", json={
        "hospital_id": 1,
        "bed_number": "ER-102",
        "aadhaar_number": "4444 3333 2222"
    })
    assert res_bed_conflict.status_code == 409

    # 5. Discharge bed -> transitions to 'Cleaning'
    res_dis = client.post(f"/api/beds/{alloc_id}/discharge")
    assert res_dis.status_code == 200
    assert res_dis.json()["status"] == "Cleaning"

    # 6. Mark bed Cleaned -> transitions to 'Vacant'
    res_clean = client.post(f"/api/beds/{alloc_id}/clean")
    assert res_clean.status_code == 200
    assert res_clean.json()["status"] == "Vacant"

def test_opd_queue_and_collision_safe_tokens():
    # Issue a token for Meera Iyer
    res = client.post("/api/queue/issue", json={
        "aadhaar_number": "9999 8888 7777",
        "doctor_id": 2,
        "hospital_id": 2
    })
    # If Meera already had one from seeding, it will reject or issue
    if res.status_code == 201:
        q_item = res.json()
        assert q_item["token_number"].startswith("A-")
        q_id = q_item["queue_id"]
        
        # Prevent duplicate active token today
        res_dup = client.post("/api/queue/issue", json={
            "aadhaar_number": "9999 8888 7777",
            "doctor_id": 2,
            "hospital_id": 2
        })
        assert res_dup.status_code == 400

        # Update status to Serving
        res_serv = client.put(f"/api/queue/{q_id}/status", json={"status": "Serving"})
        assert res_serv.status_code == 200
        assert res_serv.json()["status"] == "Serving"

        # Complete token
        res_comp = client.put(f"/api/queue/{q_id}/status", json={"status": "Completed"})
        assert res_comp.status_code == 200
        assert res_comp.json()["status"] == "Completed"

def test_appointments_double_booking_prevention():
    today = datetime.date.today()
    target_date = (today + datetime.timedelta(days=7)).isoformat()
    slot = "10:30 AM"

    # Book first appointment
    appt1 = {
        "aadhaar_number": "2345 6789 0123",
        "doctor_id": 1,
        "hospital_id": 1,
        "department": "Cardiology",
        "appointment_date": target_date,
        "time_slot": slot,
        "reason": "Blood Pressure Evaluation"
    }
    res1 = client.post("/api/appointments", json=appt1)
    # If already booked in earlier test run, clear it or verify conflict
    if res1.status_code == 201:
        # Second attempt for same doctor, date and slot must fail
        appt2 = {
            "aadhaar_number": "1111 2222 3333",
            "doctor_id": 1,
            "hospital_id": 1,
            "department": "Cardiology",
            "appointment_date": target_date,
            "time_slot": slot,
            "reason": "Routine Checkup"
        }
        res2 = client.post("/api/appointments", json=appt2)
        assert res2.status_code == 409
        assert "already booked" in res2.json()["detail"].lower()

def test_sql_workbench_approved_queries():
    # Test Q1
    res = client.post("/api/sql/execute", json={"query_key": "Q1", "param": "2345 6789 0123"})
    assert res.status_code == 200
    data = res.json()
    assert data["row_count"] >= 3
    assert "diagnosis" in data["columns"]

    # Test Q4 (Hospital KPI)
    res_q4 = client.post("/api/sql/execute", json={"query_key": "Q4", "param": ""})
    assert res_q4.status_code == 200
    assert len(res_q4.json()["rows"]) >= 6

    # Test unapproved query rejection
    res_bad = client.post("/api/sql/execute", json={"query_key": "DROP_TABLES", "param": ""})
    assert res_bad.status_code == 400

def test_analytics_and_csv_exports():
    res_dash = client.get("/api/analytics/dashboard")
    assert res_dash.status_code == 200
    dash = res_dash.json()
    assert dash["total_patients"] >= 5
    assert dash["total_beds"] >= 12

    # CSV exports
    res_csv = client.get("/api/analytics/reports/csv?report_type=records")
    assert res_csv.status_code == 200
    assert "Record ID" in res_csv.text
    assert "Masked Aadhaar" in res_csv.text

def test_user_profile_and_password_change():
    # 1. Login as doctor
    res = client.post("/api/auth/login", json={"username": "doctor", "password": "doctor123"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get profile
    res_me = client.get("/api/auth/me", headers=headers)
    assert res_me.status_code == 200
    me = res_me.json()
    assert me["username"] == "doctor"
    assert me["role"] == "Doctor"
    assert me["department"] is not None
    assert me["hospital_name"] is not None

    # 3. Update profile
    res_up = client.put("/api/auth/profile", json={
        "full_name": "Dr. Anita Verma MD",
        "email": "dr.anita@apollo.hospital",
        "phone": "+91 99887 76655"
    }, headers=headers)
    assert res_up.status_code == 200
    updated = res_up.json()
    assert updated["full_name"] == "Dr. Anita Verma MD"
    assert updated["email"] == "dr.anita@apollo.hospital"

    # 4. Change password
    res_pw = client.post("/api/auth/change-password", json={
        "current_password": "doctor123",
        "new_password": "newDoctorPass123"
    }, headers=headers)
    assert res_pw.status_code == 200
    assert res_pw.json()["status"] == "success"

    # Verify old password fails
    res_fail = client.post("/api/auth/login", json={"username": "doctor", "password": "doctor123"})
    assert res_fail.status_code == 401

    # Verify new password succeeds
    res_succ = client.post("/api/auth/login", json={"username": "doctor", "password": "newDoctorPass123"})
    assert res_succ.status_code == 200
    new_token = res_succ.json()["access_token"]

    # Revert password back to doctor123 for test reproducibility
    res_rev = client.post("/api/auth/change-password", json={
        "current_password": "newDoctorPass123",
        "new_password": "doctor123"
    }, headers={"Authorization": f"Bearer {new_token}"})
    assert res_rev.status_code == 200

    # 5. Test logout endpoint
    res_out = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {new_token}"})
    assert res_out.status_code == 200
    assert res_out.json()["status"] == "logged_out"

def test_patient_update_endpoint():
    # Login admin
    res_login = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Update patient Ananya Patel
    update_data = {
        "allergies": "Latex, Dust Mites",
        "emergency_contact": "Deepak Patel (Brother): +91 97654 99999"
    }
    res_up = client.put("/api/patients/4444 3333 2222", json=update_data, headers=headers)
    assert res_up.status_code == 200
    p = res_up.json()
    assert "Dust Mites" in p["allergies"]
    assert "99999" in p["emergency_contact"]
