from fastapi import FastAPI

from models.base import Base
from database import engine

from routes import auth_routes, song_routes

app = FastAPI()
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(song_routes.router, prefix="/songs")
Base.metadata.create_all(engine)
