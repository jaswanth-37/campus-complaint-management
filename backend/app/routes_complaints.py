from datetime import datetime
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .auth import get_current_user, require_admin
from .database import get_db
from .models import Complaint, ComplaintStatus, User
from .schemas import ComplaintCreate, ComplaintOut, ComplaintUpdate

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])

@router.post("", response_model=ComplaintOut, status_code=201)
def create_complaint(data: ComplaintCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    complaint = Complaint(**data.model_dump(), student_id=user.id)
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint

@router.get("", response_model=list[ComplaintOut])
def list_complaints(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Complaint)
    if user.role != "admin":
        query = query.filter(Complaint.student_id == user.id)
    return query.order_by(Complaint.created_at.desc()).all()

@router.get("/{complaint_id}", response_model=ComplaintOut)
def get_complaint(complaint_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    complaint = db.get(Complaint, complaint_id)
    if not complaint or (user.role != "admin" and complaint.student_id != user.id):
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@router.patch("/{complaint_id}", response_model=ComplaintOut)
def update_complaint(
    complaint_id: int,
    data: ComplaintUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    complaint = db.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(complaint, key, value)
    if data.status == ComplaintStatus.RESOLVED.value:
        complaint.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(complaint)
    return complaint

@router.post("/{complaint_id}/attachment", response_model=ComplaintOut)
async def upload_attachment(
    complaint_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    complaint = db.get(Complaint, complaint_id)
    if not complaint or (user.role != "admin" and complaint.student_id != user.id):
        raise HTTPException(status_code=404, detail="Complaint not found")
    allowed = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, WEBP, and PDF files are allowed")
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Maximum file size is 5 MB")
    import os
    os.makedirs("uploads", exist_ok=True)
    safe_name = f"complaint_{complaint_id}_{os.path.basename(file.filename or 'attachment')}"
    path = os.path.join("uploads", safe_name)
    with open(path, "wb") as target:
        target.write(content)
    complaint.attachment_url = f"/uploads/{safe_name}"
    db.commit()
    db.refresh(complaint)
    return complaint
