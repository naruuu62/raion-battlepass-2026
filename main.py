from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from database import engine
from models.base import Base
from routes import auth_routes, song_routes

settings = get_settings()

app = FastAPI(
    title="Music App API",
    description="API for Music Application",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(song_routes.router, prefix="/songs")

# Create database tables
Base.metadata.create_all(bind=engine)
