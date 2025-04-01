from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field, validator
from passlib.context import CryptContext


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
        username:str | None = None


class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)


    @validator("password")
    def validate_password(cls, value):
        if " " in value:
            raise ValueError("Password must not contain spaces")
        return value

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
   id: int


   class Config:
        orm_mode = True


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_sheme = OAuth2PasswordBearer(tokenUrl="token")