import uuid
import bcrypt
from fastapi import FastAPI, HTTPException
from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

from pydantic_schemas.user_create import UserCreate
from database import db, engine

# create the FastAPI app
app = FastAPI()
    
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)

@app.post("/signup")
def signup_user(user: UserCreate):
    # TODO 1: Extract the data thats coming from request
    # print(user.email)
    # print(user.name)
    # print(user.password)
    
    # TODO 2: check if the user already exists in db
    user_db = db.query(User).filter(User.email == user.email).first()
    
    # jika ada user, kembalikan pesan bahwa user sudah ada
    if user_db is not None:
        raise HTTPException(400, detail="User with the same email already exists!")
    
    # hash the password
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    
    # Jika tidak ada, buat user baru
    user_db = User(
        id = str(uuid.uuid4()),  # uuid untuk id unik dari python
        name = user.name,
        email = user.email,
        password = hashed_pw
    )
    
    # TODO 3: add the user to db
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    
    return user_db
    

Base.metadata.create_all(engine)