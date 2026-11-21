import sys
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

payload = {
    "mobile": "9876543210",
    "email": "",
    "address": "B-14, Sector 62, Noida, Uttar Pradesh",
    "allergies": "Penicillin, Aspirin",
    "chronic_conditions": "None",
    "emergency_contact_name": "",
    "emergency_contact_phone": ""
}

res = client.put("/api/patients/2345 6789 0123", json=payload)
print("Status code:", res.status_code)
print("Response text:", res.text)
