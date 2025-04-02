import time

def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Password Manager API!"}


def test_create_user(test_client, user_id):
    response = test_client.post("/api/register", json=user_id)
    response_data = response.json()
    assert response.status_code == 201


    response = test_client.get(f"/api/users/{response_data['id']}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert response_json["User"]["id"] == user_id["id"]
    assert response_json["User"]["address"] == "123 Farmville"
    assert response_json["User"]["first_name"] == "John"
    assert response_json["User"]["last_name"] == "Doe"



def test_create_delete_user(test_client, user_id):
    response = test_client.post("/api/users/", json=user_id)
    response_json = response.json()
    assert response.status_code == 201

    # Delete the created user
    response = test_client.delete(f"/api/users/{user_id['id']}")
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["Status"] == "Success"
    assert response_json["Message"] == "User deleted successfully"

    # Get the deleted user
    response = test_client.get(f"/api/users/{user_id['id']}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No User with this id: `{user_id['id']}` found"
