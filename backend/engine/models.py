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
from pydantic import BaseModel