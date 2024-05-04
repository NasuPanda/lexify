import pytest

from httpx import AsyncClient

from app.main import app
from app.services.auth_service import get_user_by_username
from app.dependencies import get_db
from tests.conftest import TestSessionContext

app.dependency_overrides[get_db] = lambda: TestSessionContext.session

@pytest.mark.asyncio
async def test_user_registration(db):
    user_data = {"username": "testuser", "password": "password123"}
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/auth/register", json=user_data)

    user = get_user_by_username(db, username="testuser")

    # Assertions to check if the user was created and the response is correct
    assert user is not None
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_user_registration_and_login(db):
    user_data = {"username": "testuser", "password": "password123"}
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        _res = await client.post("/auth/register", json=user_data)

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/auth/login", json=user_data)

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
