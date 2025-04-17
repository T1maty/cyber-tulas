from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field, validator
from passlib.context import CryptContext
import re


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
        username:str | None = None


class UserBaseRegister(BaseModel):
     username:str = Field(..., min_length=5, max_length=15)
     email: EmailStr
     password: str = Field(...,min_length=8, max_length=22)
     first_name: str = Field(..., min_length=1, max_length=15)
     last_name: str = Field(..., min_length=1, max_length=15)

     @validator("username")
     def validate_username(cls, value):
         if " " in value:
             raise ValueError("Username must not contain spaces")
         return value

     @validator("password")
     def validate_password(cls, value):
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d@#$%^&+=!]{8,22}$", value):
            raise ValueError(
               "Password must contain at least one uppercase letter, one lowercase letter, one number, and can include special characters"
            )
        return value
     
     
 
class UserBaseLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)


    @validator("password")
    def validate_password(cls, value):
        if " " in value:
            raise ValueError("Password must not contain spaces")
        return value


class UserCreate(UserBaseRegister):
    is_active: bool = Field(default=True)
    role: str = Field(default="user")


class UserResponse(UserBaseRegister):
   id: int


   class Config:
        orm_mode = True


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_sheme = OAuth2PasswordBearer(tokenUrl="token")