import asyncio
import sqlite3
import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.core.security import hash_password
from app.models.user_model import User
from app.main import app


@pytest.fixture(scope="module")
def client():
    # Create an instance of AsyncClient
    test_client = AsyncClient(app=app, base_url="http://testserver")
    yield test_client
    # Ensure the client is closed after the test completes
    asyncio.run(test_client.aclose())

@pytest.fixture(scope="module")
def test_db():
    # TODO Prepare test db
    # TODO Modify the URL here
    engine = create_engine("postgresql://username:password@localhost/testdb")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.mark.asyncio
async def test_user_registration(client, test_db, mocker):
    # Mock the get_db dependency to return our test database
    mocker.patch('app.dependencies.get_db', return_value=test_db)

    # Define user registration data
    user_data = {"username": "testuser", "password": "password123"}
    response = await client.post("/auth/register", json=user_data)

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_user_login(client, test_db, mocker):
    # Insert user directly into the database
    hashed_password = hash_password("password123")
    user = User(username="testuser", password_hash=hashed_password)
    test_db.add(user)
    test_db.commit()

    # Mock the get_db dependency to return our test database
    mocker.patch('app.dependencies.get_db', return_value=test_db)

    # Test login
    login_data = {"username": "testuser", "password": "password123"}
    response = await client.post("/auth/login", json=login_data)

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
