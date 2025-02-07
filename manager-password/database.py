import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Завантажуємо змінні з .env
load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")

MONGO_URL = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DB}?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGO_URL)
database = client[MONGO_DB]
user_collection = database.get_collection("users")
