import os
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
algorithm = os.getenv("ALGORITHM")
db_url = os.getenv("DATABASE_URL")

print(access_token)
print(algorithm)
print(db_url)