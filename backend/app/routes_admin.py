from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from .auth import require_admin
from .database import get_db
from .models import Complaint, User

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/stats")
def stats(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    total = db.query(func.count(Complaint.id)).scalar() or 0
    pending = db.query(func.count(Complaint.id)).filter(Complaint.status == "pending").scalar() or 0
    in_progress = db.query(func.count(Complaint.id)).filter(Complaint.status == "in_progress").scalar() or 0
    resolved = db.query(func.count(Complaint.id)).filter(Complaint.status == "resolved").scalar() or 0
    return {"total": total, "pending": pending, "in_progress": in_progress, "resolved": resolved}

@router.get("/users")
def users(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User.id, User.name, User.email, User.student_id, User.department, User.role).order_by(User.name).all()
