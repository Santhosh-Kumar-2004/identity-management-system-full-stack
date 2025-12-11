import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Enum, 
    TIMESTAMP,
    func
)
from sqlalchemy.orm import declarative_base
from typing import Optional
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum

Base = declarative_base()

class UserRole(PyEnum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default= lambda: str(uuid.uuid4())),
    name = Column(String(255), nullable=False),
    email = Column(String(255), nullable=False, unique=True),
    password = Column(String(255), nullable=False),
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.user),
    is_logged = Column(Boolean, nullable=False, default=False),

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True))