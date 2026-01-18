import uuid
import bcrypt
from fastapi import Depends, HTTPException, Header
import jwt
from middleware.auth_middleware import auth_middleware
from models.user_db_model import UserDB
from pydantic_schemas.user_create import UserCreate
from fastapi import APIRouter
from sqlalchemy.orm import Session

from database import get_db
from pydantic_schemas.user_login import UserLogin

router = APIRouter()


@router.post("/signup", status_code=201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    # TODO 1: Ekstrak data yang berasal dari request
    # print(user.email)
    # print(user.name)
    # print(user.password)

    # TODO 2: Cek apakah user sudah ada di database
    user_db = db.query(UserDB).filter(UserDB.email == user.email).first()

    # Jika ada user, kembalikan pesan bahwa user sudah ada
    if user_db is not None:
        raise HTTPException(400, detail="User with the same email already exists!")

    # Hash password
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    # Jika tidak ada, buat user baru
    user_db = UserDB(
        id=str(uuid.uuid4()),  # UUID untuk ID unik dari Python
        name=user.name,
        email=user.email,
        password=hashed_pw,
    )

    # TODO 3: add the user to db
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    # check if a user with same email already exist
    user_db = db.query(UserDB).filter(UserDB.email == user.email).first()

    if not user_db:
        raise HTTPException(400, detail="User with this email does not exist!")

    # if user exist, password matching or not
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)

    if not is_match:
        raise HTTPException(400, detail="Incorrect password!")

    token = jwt.encode(
        {
            "id": user_db.id,
        },
        "password_key",
    )

    return {"token": token, "user": user_db}


@router.get("/")
def current_user_data(
    db: Session = Depends(get_db), user_dict=Depends(auth_middleware)
):
    user = db.query(UserDB).filter(UserDB.id == user_dict["uid"]).first()

    if not user:
        raise HTTPException(404, detail="User not found")

    return user
