from pydantic import BaseModel


class AuthResponse(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        from_attributes = True
