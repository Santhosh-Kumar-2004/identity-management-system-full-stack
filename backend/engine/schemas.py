from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from engine.models import UserRole

class CreateUser(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.user

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class ResponseUser(BaseModel):
    id: Optional[str] 
    name: str
    email: EmailStr
    role: Optional[UserRole] = UserRole.user
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class RoleChangeRequest(BaseModel):
    role: UserRole.admin