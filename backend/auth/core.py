from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    url=DATABASE_URL,
    echo=True,
    pool_size=30,
    max_overflow=20,
)

sessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = sessionLocal()

    try:
        yield db

    finally:
        db.close()