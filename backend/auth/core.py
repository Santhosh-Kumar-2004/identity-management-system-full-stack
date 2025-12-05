from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

passowrd1 = pwd_context.hash("Santhosh12136")

print(passowrd1)