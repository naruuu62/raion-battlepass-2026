from fastapi import FastAPI

from models.base_model import Base
from database import engine

from routes import auth_routes

app = FastAPI()
app.include_router(auth_routes.router, prefix="/auth")

Base.metadata.create_all(engine)
