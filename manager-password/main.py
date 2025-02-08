from fastapi import FastAPI, HTTPException
from typing import List

import urllib.parse
from database import user_collection
from bson import ObjectId
import schemas
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from database import user_collection
import os

load_dotenv()
app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    user = urllib.parse.quote_plus(os.getenv("MONGO_USER"))
    password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
    host = os.getenv("MONGO_HOST")
    db_name = os.getenv("MONGO_DB")
    mongo_details = f"mongodb+srv://{user}:{password}@{host}/{db_name}?retryWrites=true&w=majority"

@app.get("/test-connection")
async def test_connection():
    users_cursor = user_collection.find()
    users = await users_cursor.to_list(5)

@app.get('/')
def welcome():
    return {'message': 'Welcome to my FastAPI application'}

@app.get("/users", response_model=List[schemas.User])
async def read_users():
    users = []
    async for user in user_collection.find():
        user["_id"] = str(user["_id"])  
        users.append(user)
    return users

@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    user_dict = user.dict()
    result = await user_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict

@app.put("/users/{id}", response_model=schemas.User)
async def update_user(id: str, user: schemas.UserCreate):
    user_dict = user.dict()
    result = await user_collection.update_one({"_id": ObjectId(id)}, {"$set": user_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict["_id"] = id
    return user_dict

@app.delete("/users/{id}")
async def delete_user(id: str):
    result = await user_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User successfully deleted"}