from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from models import UserRole

class CreateUser(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.user

class LoginUser(BaseModel):
    email: EmailStr
    password: str