import time
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.database import get_db

router = APIRouter(prefix="/sql", tags=["SQL Workbench"])

# Predefined Course Evaluation Queries (Q1 - Q5)
APPROVED_QUERIES = {
    "Q1": {
        "title": "Q1: Patient Lifelong History (JOIN patient, hospital, doctor)",
        "sql": """
SELECT 
    mr.record_id,
    mr.visit_date,
    mr.visit_type,
    mr.department,
    mr.diagnosis,
    mr.icd10_code,
    h.hospital_name,
    d.doctor_name
FROM medical_record mr
JOIN hospital h ON mr.hospital_id = h.hospital_id
LEFT JOIN doctor d ON mr.doctor_id = d.doctor_id
WHERE mr.aadhaar_number = :param
ORDER BY mr.visit_date DESC;
        """.strip(),
        "default_param": "2345 6789 0123",
        "param_label": "Patient Aadhaar UID"
    },
    "Q2": {
        "title": "Q2: Patient Profile & Visit Aggregations (GROUP BY & COUNT)",
        "sql": """
SELECT 
    p.aadhaar_number,
    p.full_name,
    p.blood_group,
    p.chronic_conditions,
    COUNT(mr.record_id) AS total_visits,
    MAX(mr.visit_date) AS latest_visit_date
FROM patient p
LEFT JOIN medical_record mr ON p.aadhaar_number = mr.aadhaar_number
WHERE p.aadhaar_number = :param
GROUP BY p.aadhaar_number;
        """.strip(),
        "default_param": "2345 6789 0123",
        "param_label": "Patient Aadhaar UID"
    },
    "Q3": {
        "title": "Q3: Abnormal Lab Investigation Findings (FILTER is_abnormal=1)",
        "sql": """
SELECT 
    lr.test_name,
    lr.result,
    lr.normal_range,
    lr.unit,
    lr.report_date,
    lr.aadhaar_number
FROM lab_report lr
WHERE lr.is_abnormal = 1
ORDER BY lr.report_date DESC;
        """.strip(),
        "default_param": "",
        "param_label": "None"
    },
    "Q4": {
        "title": "Q4: Hospital Network Performance KPI (GROUP BY hospital)",
        "sql": """
SELECT 
    h.hospital_id,
    h.hospital_name,
    h.hospital_type,
    h.city,
    COUNT(mr.record_id) AS total_consultations,
    COUNT(DISTINCT mr.aadhaar_number) AS unique_patients
FROM hospital h
LEFT JOIN medical_record mr ON h.hospital_id = mr.hospital_id
GROUP BY h.hospital_id, h.hospital_name, h.hospital_type, h.city
ORDER BY total_consultations DESC;
        """.strip(),
        "default_param": "",
        "param_label": "None"
    },
    "Q5": {
        "title": "Q5: Emergency Trauma Admissions & Critical Diagnoses",
        "sql": """
SELECT 
    p.full_name,
    p.mobile,
    p.blood_group,
    p.allergies,
    mr.visit_date,
    mr.diagnosis,
    h.hospital_name
FROM patient p
JOIN medical_record mr ON p.aadhaar_number = mr.aadhaar_number
JOIN hospital h ON mr.hospital_id = h.hospital_id
WHERE mr.visit_type = 'Emergency'
ORDER BY mr.visit_date DESC;
        """.strip(),
        "default_param": "",
        "param_label": "None"
    }
}

class QueryRunRequest(BaseModel):
    query_key: str
    param: str = ""

@router.get("/queries")
def get_approved_queries():
    """Return catalog of approved DBMS demonstration queries."""
    return [
        {
            "key": k,
            "title": v["title"],
            "sql": v["sql"],
            "default_param": v["default_param"],
            "param_label": v["param_label"]
        }
        for k, v in APPROVED_QUERIES.items()
    ]

@router.post("/execute")
def execute_approved_query(req: QueryRunRequest, db: Session = Depends(get_db)):
    """
    Executes an approved, read-only parameterized query against the real database.
    Prevents arbitrary SQL injection or destructive operations.
    """
    if req.query_key not in APPROVED_QUERIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Query key '{req.query_key}' is not an approved demonstration query."
        )

    query_meta = APPROVED_QUERIES[req.query_key]
    sql_text = query_meta["sql"]
    param_val = req.param.strip() if req.param.strip() else query_meta["default_param"]

    t0 = time.perf_counter()
    try:
        stmt = text(sql_text)
        result = db.execute(stmt, {"param": param_val})
        columns = list(result.keys())
        rows = []
        for r in result.fetchall():
            row_dict = {}
            for idx, col in enumerate(columns):
                val = r[idx]
                if hasattr(val, "isoformat"):
                    val = val.isoformat()
                row_dict[col] = val
            rows.append(row_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database query execution error: {str(e)}"
        )
    t1 = time.perf_counter()

    execution_ms = round((t1 - t0) * 1000, 2)
    return {
        "query_key": req.query_key,
        "title": query_meta["title"],
        "sql": sql_text,
        "param_used": param_val,
        "columns": columns,
        "rows": rows,
        "row_count": len(rows),
        "execution_time_ms": execution_ms
    }
