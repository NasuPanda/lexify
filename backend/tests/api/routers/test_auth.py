from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={"username": "testuser", "password": "securepassword", "email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully", "user_id": 1}

def test_login_user():
    response = client.post("/auth/login", json={"username": "testuser", "password": "securepassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful", "user_id": 1}
