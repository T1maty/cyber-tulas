from fastapi import FastAPI, HTTPException
from typing import List
import schemas
from bson import ObjectId
from database import user_collection  # Import user_collection
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/test-connection")
async def test_connection():
    try:
        collections = await user_collection.database.list_collection_names()
        return {"status": "success", "collections": collections}
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        return {"status": "error", "message": str(e)}



@app.post("/register")
async def register_user(user: schemas.UserBaseRegister):
    existing_user = await user_collection.find_one({"email":user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await user_collection.find_one({"username":user.username})
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = pwd_context.hash(user.password)

    user_dict = user.dict()
    user_dict["password"] = hashed_password


    try:
       result = await user_collection.insert_one(user_dict)
       logger.info(f"User registered with ID: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return {"message": "User registered successfully"}    



@app.get("/users", response_model=List[schemas.UserBaseLogin])
async def read_users():
    users = []
    try:
        async for user in user_collection.find():
            user["_id"] = str(user["_id"])  # Convert ObjectId to string
            users.append(user)
    except Exception as e:
        logger.error(f"Error reading users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return users

@app.post("/users", response_model=schemas.UserBaseLogin)
async def create_user(user: schemas.UserCreate,):
    user_dict = user.dict()
    try:
        result = await user_collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id) 
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return user_dict

@app.put("/users/{id}", response_model=schemas.UserBaseLogin)
async def update_user(id: str, user: schemas.UserCreate):
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

@app.delete("/users/{id}")
async def delete_user(id: str):
    try:
        result = await user_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"message": "User successfully deleted"}