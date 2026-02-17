# test_mongo.py
import os
import urllib.parse
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_USER = urllib.parse.quote_plus(os.getenv("MONGO_USER"))
MONGO_PASSWORD = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")

mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DB}?retryWrites=true&w=majority"

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    # Try to get server info
    client.server_info()
    print(" Connected successfully!")
except Exception as e:
    print(" Connection failed:", e)