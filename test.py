#!/usr/bin/env python3
"""
MediLink Enterprise v4.0 — Unified Test Runner
Runs backend unit tests, REST API tests, and end-to-end integration workflows.
"""

import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

def run_tests():
    print("=" * 70)
    print("  🏥  MEDILINK ENTERPRISE v4.0 — AUTOMATED TEST SUITE")
    print("=" * 70)
    
    cmd = [sys.executable, "-m", "pytest", "backend/tests/", "-v", "--tb=short"]
    print(f"Executing: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=str(BASE_DIR))
    
    print("\n" + "=" * 70)
    if result.returncode == 0:
        print("  ✅ ALL TEST SUITES PASSED SUCCESSFULLY!")
    else:
        print(f"  ❌ TEST FAILURES DETECTED (Exit code: {result.returncode})")
    print("=" * 70)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
