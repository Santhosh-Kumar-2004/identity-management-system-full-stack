import os
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
algorithm = os.getenv("ALGORITHM")

print(access_token)
print(algorithm)