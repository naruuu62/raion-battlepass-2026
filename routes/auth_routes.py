from datetime import datetime, timedelta
import os
import uuid
import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Header
import jwt
from fastapi import APIRouter
from sqlalchemy.orm import Session

from response.auth_response import AuthResponse
from models.user_db import UserDB
from pydantic_schemas.user_create import UserCreate
from middleware.auth_middleware import auth_middleware
from database import get_db
from pydantic_schemas.user_login import UserLogin

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

router = APIRouter()


# SIGNUP ENDPOINT
@router.post("/signup", status_code=201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):

    user_db = db.query(UserDB).filter(UserDB.email == user.email).first()

    if user_db is not None:
        raise HTTPException(400, detail="User with the same email already exists!")

    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

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


# LOGIN ENDPOINT
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    user_db = db.query(UserDB).filter(UserDB.email == user.email).first()

    if not user_db:
        raise HTTPException(400, detail="User with this email does not exist!")

    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)

    if not is_match:
        raise HTTPException(400, detail="Incorrect password!")

    token = jwt.encode(
        {
            "id": user_db.id,
        },
        JWT_SECRET_KEY,
        algorithm="HS256",
    )

    return {"token": token, "user": AuthResponse.model_validate(user_db)}


# CURRENT USER DATA ENDPOINT
@router.get("/")
def current_user_data(
    db: Session = Depends(get_db), user_dict=Depends(auth_middleware)
):
    user_db = db.query(UserDB).filter(UserDB.id == user_dict["uid"]).first()

    if not user_db:
        raise HTTPException(404, detail="User not found")

    return AuthResponse.model_validate(user_db)
