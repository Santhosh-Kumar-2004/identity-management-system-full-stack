from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()


def create_token(data: dict, expires_time: timedelta | None= None):
    data_copy = data.copy()

    expire = datetime.now(tz=datetime.timezone.utc) + (expires_time or timedelta(minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))

    data_copy.update({"exp": expire})

    jwt.encode(data_copy, os.getenv("SECURITY_KEY"), algorithm=os.getenv("ALGORITHM"))