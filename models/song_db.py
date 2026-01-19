from sqlalchemy import TEXT, VARCHAR, Column
from models.base import Base


class SongDB(Base):
    __tablename__ = "songs"

    id = Column(TEXT, primary_key=True)
    song_url = Column(TEXT)
    thumbnail_url = Column(TEXT)
    artist = Column(TEXT)
    song_title = Column(VARCHAR(100))
