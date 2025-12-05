from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

passowrd1 = pwd_context.hash("mysecretpassword123")
verify = pwd_context.verify("mysecretpassword123", passowrd1)

print(passowrd1)
print(verify)