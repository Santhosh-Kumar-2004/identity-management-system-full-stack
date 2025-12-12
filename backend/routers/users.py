from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from helper.db_helper import get_db
from engine.models import User
from engine.schemas import CreateUser, LoginUser, UpdateUser, ResponseUser
from auth.core import hash_password, verify_password, create_token, decode_token
from auth.core import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=ResponseUser, status_code=status.HTTP_201_CREATED)
def register(
    user: CreateUser,
    db: Session = Depends(get_db)
):
    """Resgiter Endpoint

    Args:
        user (CreateUser Schema Used): Register endpoint used to create the new users.

        1. Checking the db to check for the Existing user
    """

    existing_user = db.query(User).filter(User.email == user.email).lower().first()
    if existing_user:
        raise HTTPException(
            detail="User Already Registered - Login Now!",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    print(f"The input Data: {user}")

    hashed_password = hash_password(user.password)
    print(hashed_password)