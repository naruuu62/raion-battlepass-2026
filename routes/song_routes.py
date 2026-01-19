import os
import uuid
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from middleware.auth_middleware import auth_middleware
from models.song_db import SongDB
from pydantic_schemas.song_update import SongUpdate

load_dotenv()

router = APIRouter()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


# CREATE SONG ENDPOINT
@router.post("/upload", status_code=201)
def upload_song(
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist: str = Form(...),
    title: str = Form(...),
    db: Session = Depends(get_db),
    auth_details=Depends(auth_middleware),  # token verification when request comes in
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
        title=title,
        user_id=auth_details["uid"],
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song


# READ ALL SONGS ENDPOINT
@router.get("/getall")
def get_all_songs(db: Session = Depends(get_db)):
    songs = db.query(SongDB).all()
    return songs


# READ SONGS BY CURRENT USER
@router.get("/me")
def get_user_songs(
    db: Session = Depends(get_db), auth_details=Depends(auth_middleware)
):
    user_id = auth_details["uid"]
    songs = db.query(SongDB).filter(SongDB.user_id == user_id).all()
    return songs


# UPDATE SONG ENDPOINT
@router.put("/update/{song_id}", status_code=200)
def update_song(
    song_id: str,
    song_data: SongUpdate,
    db: Session = Depends(get_db),
    auth_details=Depends(auth_middleware),
):
    user_id = auth_details["uid"]

    song = db.query(SongDB).filter(SongDB.id == song_id).first()

    if not song:
        raise HTTPException(404, detail="Song not found!")

    if song.user_id != user_id:
        raise HTTPException(
            403, detail="Forbidden! You can only update songs that you uploaded."
        )

    song.title = song_data.title
    song.artist = song_data.artist

    db.commit()
    db.refresh(song)
    return song


# DELETE SONG ENDPOINT
@router.delete("/delete/{song_id}", status_code=200)
def delete_song(
    song_id: str, db: Session = Depends(get_db), auth_details=Depends(auth_middleware)
):
    user_id = auth_details["uid"]

    song = db.query(SongDB).filter(SongDB.id == song_id).first()

    if not song:
        raise HTTPException(404, detail="Song not found!")

    if song.user_id != user_id:
        raise HTTPException(
            403, detail="Forbidden! You can only delete songs that you uploaded."
        )

    db.delete(song)
    db.commit()

    return {"message": "Song deleted successfully!", "song_id": song_id}
