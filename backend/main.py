from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users as user_routes
from routers import admins as admin_routes

from helper.db_helper import engine
from engine.models import Base

app = FastAPI(
    title="User Identity and Management System 2.0",
    description="The simple and the second version of the User Management system",
    version="2.1.0"
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_header=["*"]
)

app.include_router(user_routes)
app.include_router(admin_routes)

@app.get("/root-route")
def root_router():
    
    """This is the root, Just created to test the endpoint
    """
    return "The endpoint and app is running perfectly!"