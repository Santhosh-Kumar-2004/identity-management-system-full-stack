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

    Args: 
        User with the LoginUser schmea to validate the inputs
        db with the new sessionLocal in it which got injected by fast.

        1. Checking the Existing User or not logic
        2. Checking whether the entered and db password is matching or not
        3. Create dtry catch block to handle the errors. 
        4. Creating access token using the create_token function from hte core
        5. Except block is handling any DB related SQLAlchemy errors.
        6. Finally returning the Access tokenw itht ehtype of the token
    """

    existing_user = db.query(User).filter(User.email == user.email).lower().first()

    if not existing_user:
        raise HTTPException(
            detail=".Invalid Credentials. Please Register...!",
            status_code=status.HTTP_401_UNAUTHORIZED
       )
    
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            detail="Invalid Credentials. Please Register...!",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        existing_user.is_logged = True
        db.commit(existing_user)

        access_token = create_token(data={"sub": user.email})

    except SQLAlchemyError as e:    
        db.rollback()
        print(f"The error {e}")
        raise HTTPException(
            detail="Unexpected error Occured, This isn't common.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user", response_model=ResponseUser)
def current_user(
    user: ResponseUser = Depends(get_current_user)
):
    """This is the endpoint which extracts the Current users INformation including the Admins one I think so

    Args:
        1. Checking the user existence of the user with an If condition
        2. Created the try block and returning the exact user from the get_current_user
        3. Created the Except block to handle the DB related upcoming errors. 
    """

    if not user:
        raise HTTPException(
            detail="Invalid User, Please Login first!",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    try:
        print(f"Here is the Current User Details: {user}")
        return user
    
    except SQLAlchemyError as e:
        raise HTTPException(
            detail="Error occurred unexpectedly, Please try again after Sometime.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.put("/update-user", response_model=ResponseUser)
def update_user(
    validate_user: UpdateUser,
    db: Session = Depends(get_db),
    current_user: ResponseUser = Depends(get_current_user)
):
    """This is the endpoint which helps updating the user who needs to update their Credentials

    Args:
        1. Checking for the current user existence
    """

    if not current_user:
        raise HTTPException(
            detail="The user not found, Please try to login to get the Fresh Token",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    user = db.query(User).filter(User.email == current_user.email).lower().first()

    if not user:
        raise HTTPException(
            detail="User not found",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        if validate_user.name is not None:
            user.name = validate_user.name

        if validate_user.email is not None:
            user.email = validate_user.email

        if validate_user.password is not None:
            user.password = validate_user.password

        print(
            "Update went successfully!"
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Unexpected error the Update Endpoint: {e}")
        
        raise HTTPException(
            detail="The error code is 500, Found it Unexpectedly",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )