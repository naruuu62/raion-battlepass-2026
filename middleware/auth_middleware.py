from fastapi import HTTPException, Header
import jwt

from config.settings import get_settings

settings = get_settings()


def auth_middleware(x_auth_token: str = Header(None)) -> dict:
    """Verify JWT token and return user data"""
    try:
        # Check if token is provided
        if not x_auth_token:
            raise HTTPException(401, "No auth token provided, Access Unauthorized!")

        # Verify token
        verified_token = jwt.decode(
            x_auth_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        # Check if token is valid
        if not verified_token:
            raise HTTPException(401, "Token verification failed, Access Unauthorized!")

        # Extract user ID from the verified token
        uid = verified_token.get("id")

        return {"uid": uid, "token": x_auth_token}

    except jwt.PyJWTError:
        raise HTTPException(401, "Token not valid, Access Unauthorized!")
