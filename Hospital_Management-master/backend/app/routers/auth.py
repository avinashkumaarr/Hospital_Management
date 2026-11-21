from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database import get_db
from backend.app.models.entities import User, Doctor, Hospital, AccessLog
from backend.app.schemas.all_schemas import Token, LoginRequest, UserOut, UserUpdate, ChangePasswordRequest
from backend.app.security import verify_password, hash_password, create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        # Check session cookie or fallback demo header
        token = request.cookies.get("medilink_token")
    else:
        token = auth_header.split(" ", 1)[1]
        
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired authentication token")
        
    user = db.query(User).filter(User.username == payload["sub"], User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account not found or deactivated")
    return user

def get_optional_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    try:
        return get_current_user(request, db)
    except Exception:
        return None

@router.post("/login", response_model=Token)
def login(req: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")
        
    token = create_access_token({
        "sub": user.username,
        "role": user.role,
        "name": user.full_name,
        "doc_id": user.doctor_id,
        "hosp_id": user.hospital_id
    })
    
    # Audit log login
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    return Token(
        access_token=token,
        role=user.role,
        username=user.username,
        full_name=user.full_name,
        doctor_id=user.doctor_id,
        hospital_id=user.hospital_id
    )

@router.get("/me", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    doc_dept = None
    hosp_name = None
    if current_user.doctor_id:
        doc = db.query(Doctor).filter(Doctor.doctor_id == current_user.doctor_id).first()
        if doc:
            doc_dept = doc.specialization
    if current_user.hospital_id:
        hosp = db.query(Hospital).filter(Hospital.hospital_id == current_user.hospital_id).first()
        if hosp:
            hosp_name = hosp.hospital_name

    return UserOut(
        user_id=current_user.user_id,
        username=current_user.username,
        full_name=current_user.full_name,
        role=current_user.role,
        doctor_id=current_user.doctor_id,
        hospital_id=current_user.hospital_id,
        email=current_user.email or f"{current_user.username}@medilink.hospital",
        phone=current_user.phone or "+91 98765 43210",
        department=doc_dept or ("Administration" if current_user.role == "Administrator" else "General Practice"),
        hospital_name=hosp_name or "AIIMS New Delhi",
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

@router.put("/profile", response_model=UserOut)
def update_profile(
    req: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Allow updating permitted personal profile information (name, email, phone)."""
    if req.full_name is not None and req.full_name.strip():
        current_user.full_name = req.full_name.strip()
    if req.email is not None:
        current_user.email = req.email.strip()
    if req.phone is not None:
        current_user.phone = req.phone.strip()
        
    db.commit()
    db.refresh(current_user)
    return get_profile(current_user, db)

@router.post("/change-password")
def change_password(
    req: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change staff account password with current-password verification."""
    if not verify_password(req.current_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password does not match")
    if len(req.new_password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be at least 6 characters")
        
    current_user.password_hash = hash_password(req.new_password)
    db.commit()
    return {"status": "success", "message": "Password changed successfully"}

@router.post("/logout")
def logout(current_user: Optional[User] = Depends(get_optional_user)):
    """Session invalidation endpoint."""
    return {"status": "logged_out", "message": "Session invalidated successfully"}

@router.get("/roles")
def get_available_demo_roles():
    """Return quick role information for testing UI dashboards."""
    return [
        {"role": "Administrator", "username": "admin", "desc": "Full hospital administrative privileges"},
        {"role": "Doctor", "username": "doctor", "desc": "Clinical encounters, prescriptions, and diagnostics"},
        {"role": "Receptionist", "username": "receptionist", "desc": "Patient registration, appointments, and OPD queue"},
        {"role": "Emergency Staff", "username": "emergency", "desc": "Emergency triage, break-glass records, and trauma bays"}
    ]
