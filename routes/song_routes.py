import uuid
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user_id
from models.song_db import SongDB
from pydantic_schemas.request.song_update import SongUpdate
from services.song_service import SongService
from services.upload_service import UploadService


router = APIRouter()


@router.post("/upload", status_code=201)
def upload_song(
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist: str = Form(...),
    title: str = Form(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """Upload a new song with thumbnail"""
    # Validate files
    UploadService.validate_files(song, thumbnail)

    # Generate song ID for folder structure

    song_id = str(uuid.uuid4())

    # Upload files to Cloudinary
    song_url, thumbnail_url = UploadService.upload_song_files(song, thumbnail, song_id)

    # Create song in database
    return SongService.create_song(
        song_url=song_url,
        thumbnail_url=thumbnail_url,
        artist=artist,
        title=title,
        user_id=user_id,
        db=db,
    )


@router.get("/getall")
def get_all_songs(db: Session = Depends(get_db)):
    """Get all songs"""
    return SongService.get_all_songs(db)


@router.get("/me")
def get_user_songs(
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)
):
    """Get all songs uploaded by current user"""
    return SongService.get_user_songs(user_id, db)


@router.put("/update/{song_id}")
def update_song(
    song_id: str,
    song_data: SongUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """Update song information"""
    return SongService.update_song(song_id, song_data, user_id, db)


@router.delete("/delete/{song_id}")
def delete_song(
    song_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """Delete a song"""
    return SongService.delete_song(song_id, user_id, db)
