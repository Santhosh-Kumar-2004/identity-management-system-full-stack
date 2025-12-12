from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

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
        db with the get_db sessionLocal

        1. Checking the db to check for the Existing user
        2. Hashing the password which entered by the user
        3. Trying to crete the user into the db
        4. adding to db and committing it
        5. Added 500 error handler using SQLAlchemyError
        6. finally returned the ResponseUser with the respective created user
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

    try: 
        creating_user = User(
            name = user.name.strip(),
            email = user.email,
            password =  hashed_password,
            is_logged = True
        )

        db.add(creating_user)
        db.commit()
        db.refresh(creating_user)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            detail=f"Unexpected error occurred, Do not worry This isn't Common",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
    return ResponseUser.model_validate(creating_user)

@router.post("/login")
def login(
    user: LoginUser,
    db: Session = Depends(get_db)
):
    """Login Endpoint


    """