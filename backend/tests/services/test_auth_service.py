import pytest
from sqlalchemy.orm import Session
from unittest.mock import patch
from app.services.auth_service import create_user, authenticate_user
from app.models.user_model import User
from app.schemas.user import UserRegister, UserLogin

@pytest.fixture
def user_data():
    return UserRegister(username="testuser", password="securepassword", email="test@example.com")

@pytest.fixture
def user_login_data():
    return UserLogin(username="testuser", password="securepassword")

def test_create_user(user_data):
    with patch('services.auth_service.SessionLocal') as mock_session:
        mock_session.return_value = Session()
        user = create_user(user_data)
        assert user.username == user_data.username
        assert user.email == user_data.email

def test_authenticate_user(user_login_data):
    with patch('services.auth_service.SessionLocal') as mock_session, \
        patch('services.auth_service.User.query') as mock_query:
        mock_user = User(username="testuser", password="securepassword")
        mock_query.filter_by.return_value.first.return_value = mock_user
        user = authenticate_user(user_login_data)
        assert user is not None
        assert user.username == user_login_data.username
