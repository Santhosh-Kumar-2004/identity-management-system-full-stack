from datetime import datetime, timedelta

def create_token(data: dict, expires_time: timedelta | None= None):
    data_copy = data.copy()

    expire = datetime.now(tz=datetime.timezone.utc) + (expires_time or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    data_copy.update({"exp": expire})