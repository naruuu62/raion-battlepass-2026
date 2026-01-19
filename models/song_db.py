from sqlalchemy import TEXT, VARCHAR, Column, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class SongDB(Base):
    __tablename__ = "songs"

    id = Column(TEXT, primary_key=True)
    song_url = Column(TEXT)
    thumbnail_url = Column(TEXT)
    artist = Column(VARCHAR(100))
    title = Column(VARCHAR(100))
    user_id = Column(TEXT, ForeignKey("users.id"))

    # Relationship: one song belongs to one user
    uploader = relationship("UserDB", back_populates="songs")
