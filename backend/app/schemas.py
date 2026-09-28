from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    student_id: str | None = None
    department: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    student_id: str | None
    department: str | None
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class ComplaintCreate(BaseModel):
    title: str = Field(min_length=3, max_length=180)
    description: str = Field(min_length=5)
    category: str
    department: str
    priority: str = "medium"

class ComplaintUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    assigned_to: int | None = None
    resolution: str | None = None

class ComplaintOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    category: str
    department: str
    priority: str
    status: str
    attachment_url: str | None
    resolution: str | None
    student_id: int
    assigned_to: int | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None
