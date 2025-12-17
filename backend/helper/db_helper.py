from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL, 
    echo=True,
    pool_size=30,
    max_overflow=20
)

seassionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = seassionLocal()

    try:
        yield db

    finally:
        db.close()

# Engine = manages DB connections
# sessionmaker = defines how sessions behave
# SessionLocal() = creates a new session
# yield = gives session to request, then cleans it up