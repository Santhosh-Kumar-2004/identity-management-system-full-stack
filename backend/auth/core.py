from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# passowrd1 = pwd_context.hash("mysecretpassword1234")
# verify = pwd_context.verify("mysecretpassword123", passowrd1)

# print(f"Here is the Hashed passowrd - {passowrd1}")
# print(verify)

