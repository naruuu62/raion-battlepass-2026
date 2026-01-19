import os
from dotenv import load_dotenv
from fastapi import HTTPException, Header
import jwt

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def auth_middleware(x_auth_token=Header(None)):
    try:
        # Check if token is provided
        if not x_auth_token:
            raise HTTPException(401, "No auth token in header, Access Unauthorized!")

        verified_token = jwt.decode(x_auth_token, JWT_SECRET_KEY, algorithms=["HS256"])

        # Check if token is valid
        if not verified_token:
            raise HTTPException(401, "Token verification failed, Access Unauthorized!")

        # Extract user ID from the verified token
        uid = verified_token.get("id")

        return {"uid": uid, "token": x_auth_token}

    except jwt.PyJWTError:
        raise HTTPException(401, "Token not valid, Access Unauthorized!")
