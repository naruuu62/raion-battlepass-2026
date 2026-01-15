import uuid
import bcrypt
from fastapi import Depends, HTTPException
from models.user_db_model import UserDB
from pydantic_schemas.user_create import UserCreate
from fastapi import APIRouter
from sqlalchemy.orm import Session

from database import get_db
from pydantic_schemas.user_login import UserLogin

router = APIRouter()


@router.post("/signup", status_code=201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    # TODO 1: Extract the data thats coming from request
    # print(user.email)
    # print(user.name)
    # print(user.password)

    # TODO 2: check if the user already exists in db
    user_db = db.query(UserDB).filter(UserDB.email == user.email).first()

    # jika ada user, kembalikan pesan bahwa user sudah ada
    if user_db is not None:
        raise HTTPException(400, detail="User with the same email already exists!")

    # hash the password
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    # Jika tidak ada, buat user baru
    user_db = UserDB(
        id=str(uuid.uuid4()),  # uuid untuk id unik dari python
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

    # TODO 1: check if a user with same email already exist
    user_db = db.query(UserDB).filter(UserDB.email == user.email).first()

    if not user_db:
        raise HTTPException(400, detail="User with this email does not exist!")

    # TODO 2: if user exist, password matching or not
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)

    if not is_match:
        raise HTTPException(400, detail="Incorrect password!")

    return user_db
