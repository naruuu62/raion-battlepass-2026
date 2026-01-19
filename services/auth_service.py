import uuid
import bcrypt
import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.user_db import UserDB
from pydantic_schemas.request.user_create import UserCreate
from pydantic_schemas.request.user_login import UserLogin
from pydantic_schemas.response.auth_response import AuthResponse
from config.settings import get_settings
from utils.const import MSG_USER_EXISTS, MSG_USER_NOT_FOUND, MSG_INCORRECT_PASSWORD

settings = get_settings()


class AuthService:

    @staticmethod
    def hash_password(password: str) -> bytes:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @staticmethod
    def verify_password(plain_password: str, hashed_password: bytes) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(plain_password.encode(), hashed_password)

    @staticmethod
    def create_token(user_id: str) -> str:
        """Create JWT token for user"""
        return jwt.encode(
            {"id": user_id}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def get_user_by_email(email: str, db: Session) -> UserDB | None:
        """Get user by email"""
        return db.query(UserDB).filter(UserDB.email == email).first()

    @staticmethod
    def get_user_by_id(user_id: str, db: Session) -> UserDB | None:
        """Get user by ID"""
        return db.query(UserDB).filter(UserDB.id == user_id).first()

    @staticmethod
    def create_user(user: UserCreate, db: Session) -> AuthResponse:
        """Create a new user"""

        existing_user = AuthService.get_user_by_email(user.email, db)
        if existing_user:
            raise HTTPException(400, detail=MSG_USER_EXISTS)

        # Hash password
        hashed_pw = AuthService.hash_password(user.password)

        user_db = UserDB(
            id=str(uuid.uuid4()),
            name=user.name,
            email=user.email,
            password=hashed_pw,
        )

        db.add(user_db)
        db.commit()
        db.refresh(user_db)

        return AuthResponse.model_validate(user_db)

    @staticmethod
    def login_user(user: UserLogin, db: Session) -> dict:
        """Authenticate user and return token"""
        # Find user
        user_db = AuthService.get_user_by_email(user.email, db)
        if not user_db:
            raise HTTPException(400, detail=MSG_USER_NOT_FOUND)

        # Verify password
        is_match = AuthService.verify_password(user.password, user_db.password)
        if not is_match:
            raise HTTPException(400, detail=MSG_INCORRECT_PASSWORD)

        # Create token
        token = AuthService.create_token(user_db.id)

        return {"token": token, "user": AuthResponse.model_validate(user_db)}
