from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["brcypt"], deprecated="auto")

passowrd1 = pwd_context.hash("Santhosh12136")

print(passowrd1)