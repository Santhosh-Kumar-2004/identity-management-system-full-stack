from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

passowrd1 = pwd_context.hash("Santhosh1")

print(passowrd1)