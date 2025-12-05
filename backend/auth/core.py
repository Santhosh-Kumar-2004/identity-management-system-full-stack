from passlib.context import CryptContext
from jose import JWTError, jwt

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)














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
