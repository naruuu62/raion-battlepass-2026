import os
from dotenv import load_dotenv
from fastapi import HTTPException, Header
import jwt

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def auth_middleware(x_auth_token=Header()):
    try:
        # get the user token from the headers
        if not x_auth_token:
            raise HTTPException(401, "No auth token, Unauthorized!")

        # decode the token
        verified_token = jwt.decode(x_auth_token, JWT_SECRET_KEY, algorithms=["HS256"])

        if not verified_token:
            raise HTTPException(401, "Token verification failed, Unauthorized!")

        # get the id from the token
        uid = verified_token.get("id")
        return {"uid": uid, "token": x_auth_token}

        # postgres database get he user info8
    except jwt.PyJWTError:
        raise HTTPException(401, "Token not valid, Unauthorized!")
