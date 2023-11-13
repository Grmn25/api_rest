import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_create_user_success():
    user_data = {
        "name": "usuarioprueba",
        "user": "usuarioprueba",
        "email": "test@example.com",
        "password": "testpassword",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 200

    user = response.json()

    assert "usuario_id" in user
    assert user["nombre"] == user_data["name"]
    assert user["usuario"] == user_data["user"]
    assert user["email"] == user_data["email"]


def test_create_user_failure():
    user_data = {
        "name": "Usuario de Prueba",
        "user": "testuser",
        "password": "testpassword"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 422

def test_login_success():
    login_data = {
        "user": "usuarioprueba",
        "password": "testpassword",
    }

    response = client.post("/users/login/", json=login_data)

    assert response.status_code == 200

    result = response.json()

    assert "check" in result

def test_login_failure():
    login_data = {
        "user": "test@example.com",
        "password": "failurepassword",
    }

    response = client.post("/users/", json=login_data)

    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main()