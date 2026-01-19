from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from pydantic_schemas.request.user_create import UserCreate
from pydantic_schemas.request.user_login import UserLogin
from pydantic_schemas.response.auth_response import AuthResponse
from services.auth_service import AuthService
from dependencies import get_current_user
from models.user_db import UserDB

router = APIRouter()


@router.post("/signup", status_code=201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account"""
    return AuthService.create_user(user, db)


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    return AuthService.login_user(user, db)


@router.get("/")
def current_user_data(user: UserDB = Depends(get_current_user)):
    """Get current authenticated user data"""
    return AuthResponse.model_validate(user)
