from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import AccessLog, Hospital
from backend.app.schemas.all_schemas import AuditLogOut
from backend.app.services.report import mask_aadhaar

router = APIRouter(prefix="/audit", tags=["Audit Logs"])

@router.get("", response_model=List[AuditLogOut])
def list_audit_logs(
    aadhaar: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(AccessLog)
    if aadhaar:
        clean = aadhaar.strip()
        query = query.filter(AccessLog.aadhaar_number.like(f"%{clean}%"))
        
    logs = query.order_by(AccessLog.access_time.desc()).limit(limit).all()
    results = []
    for l in logs:
        hosp_name = "National Health Gateway"
        if l.hospital_id:
            h = db.query(Hospital).filter(Hospital.hospital_id == l.hospital_id).first()
            if h:
                hosp_name = h.hospital_name
                
        results.append(AuditLogOut(
            log_id=l.log_id,
            aadhaar_number=l.aadhaar_number,
            masked_aadhaar=mask_aadhaar(l.aadhaar_number),
            hospital_id=l.hospital_id,
            hospital_name=hosp_name,
            accessed_by=l.accessed_by,
            access_time=l.access_time,
            purpose=l.purpose,
            ip_address=l.ip_address,
            status=l.status
        ))
    return results
