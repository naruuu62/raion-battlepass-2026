import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.song_db import SongDB
from pydantic_schemas.request.song_update import SongUpdate
from utils.const import MSG_SONG_NOT_FOUND, MSG_FORBIDDEN_UPDATE, MSG_FORBIDDEN_DELETE


class SongService:

    @staticmethod
    def get_all_songs(db: Session) -> list[SongDB]:
        """Get all songs"""
        return db.query(SongDB).all()

    @staticmethod
    def get_song_by_id(song_id: str, db: Session) -> SongDB | None:
        """Get song by ID"""
        return db.query(SongDB).filter(SongDB.id == song_id).first()

    @staticmethod
    def get_user_songs(user_id: str, db: Session) -> list[SongDB]:
        """Get all songs uploaded by a user"""
        return db.query(SongDB).filter(SongDB.user_id == user_id).all()

    @staticmethod
    def create_song(
        song_url: str,
        thumbnail_url: str,
        artist: str,
        title: str,
        user_id: str,
        db: Session,
    ) -> SongDB:
        """Create a new song"""
        song_id = str(uuid.uuid4())

        new_song = SongDB(
            id=song_id,
            song_url=song_url,
            thumbnail_url=thumbnail_url,
            artist=artist,
            title=title,
            user_id=user_id,
        )

        db.add(new_song)
        db.commit()
        db.refresh(new_song)

        return new_song

    @staticmethod
    def update_song(
        song_id: str, song_data: SongUpdate, user_id: str, db: Session
    ) -> SongDB:
        """Update a song"""
        song = SongService.get_song_by_id(song_id, db)

        if not song:
            raise HTTPException(404, detail=MSG_SONG_NOT_FOUND)

        if song.user_id != user_id:
            raise HTTPException(403, detail=MSG_FORBIDDEN_UPDATE)

        song.title = song_data.title
        song.artist = song_data.artist

        db.commit()
        db.refresh(song)

        return song

    @staticmethod
    def delete_song(song_id: str, user_id: str, db: Session) -> dict:
        """Delete a song"""
        song = SongService.get_song_by_id(song_id, db)

        if not song:
            raise HTTPException(404, detail=MSG_SONG_NOT_FOUND)

        if song.user_id != user_id:
            raise HTTPException(403, detail=MSG_FORBIDDEN_DELETE)

        db.delete(song)
        db.commit()

        return {"message": "Song deleted successfully!", "song_id": song_id}
