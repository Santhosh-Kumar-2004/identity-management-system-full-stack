from passlib.context import CryptContext
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_pwd(plain_pwd: str) -> str:
    return pwd_context.hash(plain_pwd)

def decode_pwd(hashed_pwd: str, plain_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)