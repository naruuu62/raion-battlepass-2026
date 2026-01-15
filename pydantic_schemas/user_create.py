# define the Pydantic model for user creation
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
