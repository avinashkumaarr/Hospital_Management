import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time
print("Importing app...")
t0 = time.time()
from backend.app.main import app
print(f"App imported in {time.time()-t0:.2f}s")

from fastapi.testclient import TestClient
print("Creating TestClient...")
t1 = time.time()
client = TestClient(app)
print(f"TestClient created in {time.time()-t1:.2f}s")

print("Calling /api/health...")
t2 = time.time()
res = client.get("/api/health")
print(f"Called in {time.time()-t2:.2f}s: status={res.status_code}")
print(res.json())
