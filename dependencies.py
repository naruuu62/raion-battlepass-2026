from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from middleware.auth_middleware import auth_middleware
from models.user_db import UserDB


def get_current_user(
    db: Session = Depends(get_db), auth_details: dict = Depends(auth_middleware)
) -> UserDB:
    """Get current authenticated user"""
    user = db.query(UserDB).filter(UserDB.id == auth_details["uid"]).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    return user


def get_current_user_id(auth_details: dict = Depends(auth_middleware)) -> str:
    """Get current authenticated user ID"""
    return auth_details["uid"]
