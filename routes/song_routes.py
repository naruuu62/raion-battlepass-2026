import os
import uuid
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, Form, UploadFile, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from middleware.auth_middleware import auth_middleware
from models.song_db import SongDB

load_dotenv()

router = APIRouter()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


@router.post("/upload")
def upload_song(
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist: str = Form(...),
    song_title: str = Form(...),
    db: Session = Depends(get_db),
    auth_details=Depends(auth_middleware),  # verifikasi token saat request
):
    song_id = str(uuid.uuid4())

    song_res = cloudinary.uploader.upload(
        song.file, resource_type="auto", folder=f"songs/{song_id}"
    )
    thumbnail_res = cloudinary.uploader.upload(
        thumbnail.file, resource_type="image", folder=f"songs/{song_id}"
    )

    new_song = SongDB(
        id=song_id,
        song_url=song_res["url"],
        thumbnail_url=thumbnail_res["url"],
        artist=artist,
        song_title=song_title,
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song
