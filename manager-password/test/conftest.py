import pytest
from fastapi.testclient import TestClient
from main import app
from motor.motor_asyncio import AsyncIOMotorClient
from database import user_collection

# Use mongomock to mock MongoDB for testing
@pytest.fixture(scope="function")
async def mock_db():
    """Create a mock MongoDB database for testing."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    test_db = client["test_database"]
    test_user_collection = test_db["users"]

    # Replace the real user_collection with the mock collection
    original_user_collection = user_collection
    user_collection = test_user_collection

    yield test_user_collection

    # Cleanup after the test
    client.drop_database("test_database")
    user_collection = original_user_collection


@pytest.fixture(scope="function")
def test_client(mock_db):
    """Create a test client that uses the mock database."""
    with TestClient(app) as client:
        yield client