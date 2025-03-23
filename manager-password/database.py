from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")

logger.info(f"MONGO_USER: {MONGO_USER}, MONGO_PASSWORD: {MONGO_PASSWORD}, MONGO_HOST: {MONGO_HOST}, MONGO_DB: {MONGO_DB}")

# Use the MongoDB Atlas connection string format
mongo_details = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DB}?retryWrites=true&w=majority"

try:
    client = AsyncIOMotorClient(mongo_details)
    database = client[MONGO_DB]
    user_collection = database.get_collection("users")
    logger.info("MongoDB connection established successfully.")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")



#test commit