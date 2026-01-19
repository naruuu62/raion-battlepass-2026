from pydantic import BaseModel


class SongUpdate(BaseModel):
    title: str
    artist: str
