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

Base = declarative_base()

