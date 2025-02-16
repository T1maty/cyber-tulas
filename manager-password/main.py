from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import urllib.parse
from typing import List
import schemas
from bson import ObjectId
from database import user_collection  # Import user_collection

load_dotenv()
app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    user = urllib.parse.quote_plus(os.getenv("MONGO_USER", ""))
    password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD", ""))
    host = os.getenv("MONGO_HOST", "localhost")
    db_name = os.getenv("MONGO_DB", "test")
    port = os.getenv("MONGO_PORT", "27017")

    mongo_details = f"mongodb://{user}:{password}@{host}:{port}/{db_name}?authSource=admin"
    
    print(f" MongoDB connection string: {mongo_details}")

    app.mongodb_client = AsyncIOMotorClient(mongo_details)
    app.mongodb = app.mongodb_client.get_database(db_name)
    print(" MongoDB connected.")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    print(" MongoDB disconnected.")

@app.get("/test-connection")
async def test_connection():
    try:
        collections = await app.mongodb.list_collection_names()
        return {"status": "success", "collections": collections}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get('/')
def welcome():
    return {'message': 'Welcome to my FastAPI application'}

@app.get("/users", response_model=List[schemas.User])
async def read_users():
    users = []
    async for user in user_collection.find():
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        users.append(user)
    return users

@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    user_dict = user.dict()
    result = await user_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)  # Convert ObjectId to string
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
