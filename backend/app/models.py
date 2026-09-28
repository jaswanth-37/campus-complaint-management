from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class UserRole(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"

class ComplaintStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    student_id: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    department: Mapped[str | None] = mapped_column(String(120), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default=UserRole.STUDENT.value)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    complaints: Mapped[list["Complaint"]] = relationship(
        back_populates="student", foreign_keys="Complaint.student_id"
    )

class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(80))
    department: Mapped[str] = mapped_column(String(120))
    priority: Mapped[str] = mapped_column(String(20), default=Priority.MEDIUM.value)
    status: Mapped[str] = mapped_column(String(30), default=ComplaintStatus.PENDING.value)
    attachment_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resolution: Mapped[str | None] = mapped_column(Text, nullable=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    student: Mapped["User"] = relationship(back_populates="complaints", foreign_keys=[student_id])
