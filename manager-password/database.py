from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
import logging
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

Base = declarative_base()

MONGO_USER = urllib.parse.quote_plus(os.getenv("MONGO_USER"))
MONGO_PASSWORD = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")

if not all([MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_DB]):
    raise RuntimeError("Missing required MongoDB environment variables")


logger.info(f"MONGO_USER: {MONGO_USER}, MONGO_PASSWORD: {MONGO_PASSWORD}, MONGO_HOST: {MONGO_HOST}, MONGO_DB: {MONGO_DB}")

mongo_details = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DB}?retryWrites=true&w=majority"
client = AsyncIOMotorClient(mongo_details)
database = client[MONGO_DB]
user_collection = database.get_collection("users")
server_collection = database.get_collection("servers")
payment_collection = database.get_collection("payments")




'''
try:
    client = AsyncIOMotorClient(mongo_details)
    database = client[MONGO_DB]
    user_collection = database.get_collection("users")
    server_collection = database.get_collection("servers")
    payment_collection = database.get_collection("payments")
    # Test the connection
    logger.info("MongoDB connection established successfully.")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
'''




