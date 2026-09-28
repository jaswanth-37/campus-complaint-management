from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .auth import create_access_token, get_current_user, hash_password, verify_password
from .database import get_db
from .models import User, UserRole
from .schemas import Token, UserCreate, UserLogin, UserOut

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    if data.student_id and db.query(User).filter(User.student_id == data.student_id).first():
        raise HTTPException(status_code=409, detail="Student ID already registered")
    user = User(
        name=data.name,
        email=data.email,
        student_id=data.student_id,
        department=data.department,
        password_hash=hash_password(data.password),
        role=UserRole.STUDENT.value,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return Token(access_token=create_access_token(user.id), user=user)

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return Token(access_token=create_access_token(user.id), user=user)

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
