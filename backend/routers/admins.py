from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from helper.db_helper import get_db
from engine.models import User
from engine.schemas import CreateUser, UpdateUser, LoginUser, ResponseUser
from auth.core import get_current_user, validate_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/all-users", response_model=List(ResponseUser))
def get_all_users(
    db: Session = Depends(get_db),
    admin = Depends(validate_admin)
):
    """This endpoint used to retrieve all the users by admins and returns as List frm typing

    Args:
        admin (Depends): va;ildate admin function which is imported from the core
        1. 
    """
    if not admin:
        raise HTTPException(
            detail="You are not allowed to access this page, Please contact admin",
            status_code=status.HTTP_403_FORBIDDEN
        )

    try:
        users = db.query(User).all()

        return [ResponseUser.model_validate(user) for user in users]

    except SQLAlchemyError as e:
        print(f"The error occcurred in get all users: {e}")
        raise HTTPException(
            detail="Internal Server Error in DB",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )