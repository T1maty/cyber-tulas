from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    users: str
    password: str
    email: str

class User(BaseModel):
    id: int
    users: str
    password: str
    email: str

    class Config:
        orm_mode = True