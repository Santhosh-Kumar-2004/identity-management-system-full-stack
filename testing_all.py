import os
from dotenv import load_dotenv

load_dotenv()

acces_token = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
algorithm = os.getenv("ALGORITHM")