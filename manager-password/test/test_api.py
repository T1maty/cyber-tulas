def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Password Manager API!"}


def test_create_user(test_client, user_id):
    response = test_client.post("/api/register", json=user_id)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["message"] == "User registered successfully"

    # Get the created user
    response = test_client.get(f"/api/users/{response_data['id']}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == response_data["id"]
    assert response_json["first_name"] == "John"
    assert response_json["last_name"] == "Doe"


def test_create_delete_user(test_client, user_id):
    response = test_client.post("/api/register", json=user_id)
    assert response.status_code == 201
    response_data = response.json()

    # Delete the created user
    response = test_client.delete(f"/api/users/{response_data['id']}")
    assert response.status_code == 202
    response_json = response.json()
    assert response_json["message"] == "User deleted successfully"

    # Get the deleted user
    response = test_client.get(f"/api/users/{response_data['id']}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No User with this id: `{response_data['id']}` found"