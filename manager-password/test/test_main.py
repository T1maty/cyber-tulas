from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 404  

def test_test_connection():
    response = client.get("/test-connection")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] in ["success", "error"]

def test_user_register():
    response = client.post(
        "/api/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123@",
            "first_name": "John",
            "last_name": "Doe"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  

def test_user_login():
    client.post(
        "/api/register",
        json={
            "username": "Test",
            "email": "testexample@gmail.com",
            "password": "Password!1A3",
            "first_name": "John",
            "last_name": "Doe"
        }
    )

    
    response = client.post(
        "/api/login",
        json={
            "email": "test@example.com",
            "password": "Password123@"
        }
    )
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Login successful"