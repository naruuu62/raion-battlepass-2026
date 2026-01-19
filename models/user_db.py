from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary
from sqlalchemy.orm import relationship

from models.base import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)

    # Relationship: one user can have many songs
    songs = relationship(
        "SongDB", back_populates="uploader", cascade="all, delete-orphan"
    )
