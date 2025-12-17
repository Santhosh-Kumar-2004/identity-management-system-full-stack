from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from helper.db_helper import get_db
from engine.models import User
from engine.schemas import CreateUser, UpdateUser, LoginUser, ResponseUser
from auth.core import get_current_user, validate_admi