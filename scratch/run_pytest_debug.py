import sys
import subprocess

cmd = [sys.executable, "-m", "pytest", "backend/tests/test_api.py::test_health_endpoint", "-vv", "-s"]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
print("STDOUT:\n", res.stdout)
print("STDERR:\n", res.stderr)
print("RETURNCODE:", res.returncode)
