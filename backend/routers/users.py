from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from helper.db_helper import get_db
from engine.models import User
from engine.schemas import CreateUser, LoginUser, UpdateUser, ResponseUser
from auth.core import hash_password, verify_password, create_token, decode_token