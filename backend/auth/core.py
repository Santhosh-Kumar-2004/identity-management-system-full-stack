from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from fastapi import HTTPException, status, Header, Depends
from sqlalchemy.orm import Session
from helper.db_helper import get_db
from engine.models import User

load_dotenv()

SECURITY_KEY = os.getenv("JWT_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.getenv("ALGORTHIM")

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str: # passowrd hashing logic
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool: # Verifying the password logic
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict, expires_time: timedelta | None= None):
    data_copy = data.copy()
    print(f"The data which copied {data_copy}")

    expire = datetime.now(tz=datetime.timezone.utc) + (expires_time or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    data_copy.update({"exp": expire})
    # print(data_copy, SECURITY_KEY, algorithm=ALGORITHM)

    return jwt.encode(data_copy, SECURITY_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        print(f"Here is the payload {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORISED,
            detail = "Token Expired",
            headers = {"WWW-Authenticate: bearer"}
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token is not matching",
            headers={"WWW-Authenticate": "bearer"}
        )
        

def get_current_user(
        authorisation: str = Header(None),
        db: Session = Depends(get_db),
):
    if not authorisation or not authorisation.lower().startswith("bearer"):
        raise HTTPException(
            detail="Authorisation is not found",
            headers= {"WWW-Authenticate": "bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    token = authorisation.split(" ", 1)[1].strip()
    payload = decode_token(token=token)

    email_id = payload.get("sub")
    if not email_id:
        raise HTTPException(
            detail="User nt found",
            headers={"WWW-Authenticate": "bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    user = db.query(User).filter(User.email == email_id).first()

    if not user:
        raise HTTPException(
            detail="User not found. Log In again",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_logged:
        raise HTTPException(
            detail="Please log in Session Expired",
            status_code=status.HTTP_401_UNAUTHORIZED
        )



# passowrd1 = pwd_context.hash("mysecretpassword1234")
# verify = pwd_context.verify("mysecretpassword123", passowrd1)

# print(f"Here is the Hashed passowrd - {passowrd1}")
# print(verify)

# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# import datetime as dt

# import os
# from dotenv import load_dotenv

# from fastapi import HTTPException, status, Header, Depends
# from sqlalchemy.orm import Session

# from app.helper.db_helper import get_db
# from app.engine.models import User
