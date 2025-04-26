from fastapi.testclient import TestClient
from fastapi import FastAPI
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_read_user():
    response = client.get("/api/users", headers={"X-Token": "fake-token"})
