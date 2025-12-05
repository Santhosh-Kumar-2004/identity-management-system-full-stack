from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_env

load_env()

DATABASE_URL = os.getenv("DATABASE_URL")