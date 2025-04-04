import pytest  # Import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from database import user_collection

@pytest.fixture(scope="function")
async def mock_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    test_db = client["test_database"]
    test_user_collection = test_db["users"]

    original_user_collection = user_collection
    user_collection = test_user_collection

    yield test_user_collection

    # Cleanup after the test
    client.drop_database("test_database")
    user_collection = original_user_collection