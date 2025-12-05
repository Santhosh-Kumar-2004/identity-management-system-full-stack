from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_pwd(password: str) -> str:
    pwd_context.hash(password)

def verify_pwd(plain_pwd: str, hashed_pwd: str) -> bool:
    pwd_context.verify(plain_pwd, hashed_pwd)