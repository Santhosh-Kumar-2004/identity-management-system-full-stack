from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

SECURITY_KEY = os.getenv("JWT_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.getenv("ALGORTHIM")

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict, expires_time: timedelta | None= None):
    to_encode = data.copy()
    print(f"The data which copied {to_encode}")

    expire = datetime.now(tz=datetime.timezone.utc) + (expires_time or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    print(jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM))

    return jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM)











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
