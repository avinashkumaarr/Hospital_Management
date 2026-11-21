from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import Notification
from backend.app.schemas.all_schemas import NotificationOut

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=List[NotificationOut])
def get_notifications(db: Session = Depends(get_db)):
    notifs = db.query(Notification).order_by(Notification.created_at.desc()).limit(30).all()
    return notifs

@router.put("/{notification_id}/read")
def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found.")
    notif.is_read = True
    db.commit()
    return {"status": "success", "notification_id": notification_id}

@router.put("/mark-all-read")
def mark_all_notifications_read(db: Session = Depends(get_db)):
    db.query(Notification).filter(Notification.is_read == False).update({"is_read": True})
    db.commit()
    return {"status": "success", "message": "All notifications marked as read."}
