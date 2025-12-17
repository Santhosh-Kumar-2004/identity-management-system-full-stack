from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users as user_routes
from routers import admins as admin_routes

from helper.db_helper import engine
from engine.models import Base
