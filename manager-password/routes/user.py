from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from bson import ObjectId
from database import user_collection
import schemas
from schemas import pwd_context
from pymongo.errors import DuplicateKeyError
import logging
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext



SECRET_KEY = "915ecbac79029b3ae20e60e424dc06919beaff15f45dcc865444579867d83125"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

logger = logging.getLogger(__name__)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter()


router.post("/token-auth")
async def token_login(form_data: Annotated[str, Depends(oauth2_scheme)]):
    user = await user_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"access_token": user.username, "token_type": "bearer"}



@router.post("/register")
async def register_user(user: schemas.UserBaseRegister, token: Annotated[str, Depends(oauth2_scheme)]):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username = await user_collection.find_one({"username": user.username})
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password

    try:
        result = await user_collection.insert_one(user_dict)
        logger.info(f"User registered with ID: {result.inserted_id}")
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"message": "User registered successfully"}


@router.post("/api/login")
async def login_user(user: schemas.UserBaseLogin, token: Annotated[str, Depends(oauth2_scheme)]):
    existing_user = await user_collection.find_one({"email": user.email})
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not pwd_context.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful"}

@router.get("/users", response_model=List[schemas.UserBaseLogin])
async def read_users():
    users = []
    try:
        async for user in user_collection.find():
            user["_id"] = str(user["_id"])  
            users.append(user)
    except Exception as e:
        logger.error(f"Error reading users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return users


@router.put("/users/{id}", response_model=schemas.UserBaseLogin)
async def update_user(id: str, user: schemas.UserResponse):
    user_dict = user.dict()
    try:
        result = await user_collection.update_one({"_id": ObjectId(id)}, {"$set": user_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    user_dict["_id"] = id
    return user_dict


@router.delete("/users/{id}")
async def delete_user(id: str):
    try:
        result = await user_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"message": "User successfully deleted"}