from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from helper.db_helper import get_db
from engine.models import User
from engine.schemas import CreateUser, UpdateUser, LoginUser, ResponseUser, UserRole
from auth.core import get_current_user, validate_admin
from engine.schemas import RoleChangeRequest

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/all-users", response_model=list(ResponseUser))
def get_all_users(
    db: Session = Depends(get_db),
    admin = Depends(validate_admin)
):
    """This endpoint used to retrieve all the users by admins and returns as List frm typing

    Args:
        admin (Depends): va;ildate admin function which is imported from the core
        1. Checking whether the user is Admin or not using the validate admin function
        2. Creatign the try catch block which helps to handle the errors
        3. Queried the DB and trying to retrieve all the users from DB
        4. Raised one exception when any error occurred in the DB while retirveing
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
    
    
@router.get("/user/{user_id}", response_model=ResponseUser)
def get_user_by_id(
    user_id: str, 
    db: Session = Depends(get_db),
    admin = Depends(validate_admin)
):
    """This is the endpoint which helps retrieveing the particular user using their id

    Args:
        0. Created user_id input and assinged it to String
        1. Imported db depend on the get_db session Local
        2. validating the user, Admin or not
    """

    if not admin:
        raise HTTPException(
            detail="Unable to authorise you, Please contact admin.",
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        print(f"User Got with the ID is: {user}")

        if not user:
            raise HTTPException(
                detail="User is not Foundable, Please login to get new ID",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return ResponseUser.model_validate(user)

    except SQLAlchemyError as e:
        print(f"One error occurred at the get user by id: {e}")
        raise HTTPException(
            detail="Internal servie error: 500*",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@router.put("/user/{user_id}/role", response_model=ResponseUser)
def make_admins(
    user_id: str,
    db: Session = Depends(get_db),
    admin = Depends(validate_admin),
    schema = RoleChangeRequest
):
    """Thisnis the endpoint which is used to create and convert the normal user into Admins, but only it can be done by another admin not by any noremal users/

    Args:
        user_id (str): This is used to select the particular user with id
        db (Session, optional): This helps to query the db 
        admin (_type_, optional): validate admin func used to check for the admin authoriation
        schema (_type_, optional): This is the schema used to validate the request
    """

    if not user_id:
        raise HTTPException(
            detail="User id not found, Please log in first",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                detail="User not Found, Please register",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if user.role == UserRole.admin and schema.role != UserRole.admin:
            counting_admins = db.query(User).filter(User.role == UserRole.admin).count()
            if counting_admins <= 1:
                raise HTTPException(
                    detail="Cannot delete the last Admin",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
        user.role = schema.role
        db.add(user)
        db.commit()
        db.refresh(user)

    except SQLAlchemyError as e:
        print(f"The Db error occurred: {e}")

        raise HTTPException(
            detail="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR0
        )
    
    except Exception as a:
        print(f"The Pythons common error occurred: {e}")

        raise HTTPException(
            detail="Not a DB error, Instead internal",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/logout")
def admin_logout(
    admin = Depends(validate_admin), 
    db: Session = Depends(get_db),
    current_user: ResponseUser = Depends(get_current_user)
):
    """This is the endpoint where the admin have the rights to make the user logout, Just making the logged in as False, not a Hard delete. 

    1. Checking the admin is real ro not
    2. Created the try catch block to handle the errors
    3. Querying the db and getting the right user
    4. Handling the user not found error
    5. Making the is_logged into False once the user is fethced
    6. Adding and committing and refreshing the db
    7. Finally handling the errors in Except blocks
    """

    if not admin:
        raise HTTPException(
            detail="You are not authorised to use this endpoint, Please contact the admin",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = db.query(User).filter(User.id == current_user.id).first()

        if not user:
            raise HTTPException(
                detail="User not found, Please register.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        user.is_logged == False
        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"The user state now: {user.is_logged}")

        return ResponseUser.model_validate(user)

    except SQLAlchemyError as e:
        print(f"The Db error occurred: {e}")

        raise HTTPException(
            detail="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR0
        )
    
    except Exception as a:
        print(f"The Pythons common error occurred: {e}")

        raise HTTPException(
            detail="Not a DB error, Instead internal",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )