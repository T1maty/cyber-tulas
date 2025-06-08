from pydantic import BaseModel, EmailStr

class User(BaseModel):
    __tablename__ = "users"
    username: str 
    password: str
    email: EmailStr