from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")

print(f"MONGO_USER: {MONGO_USER}, MONGO_PASSWORD: {MONGO_PASSWORD}, MONGO_HOST: {MONGO_HOST}, MONGO_DB: {MONGO_DB}")

mongo_details = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/{MONGO_DB}?authSource=admin"

client = AsyncIOMotorClient(mongo_details)
database = client[MONGO_DB]
user_collection = database.get_collection("users")