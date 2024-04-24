import pytest
from app.services.auth_service import create_user, authenticate_user
from app.core.security import hash_password
from app.models.user_model import User
from app.schemas.user import UserRegister, UserLogin
from sqlalchemy.orm import Session

@pytest.fixture
def mock_db_session(mocker):
    # Create a mock session to use in the tests
    session = mocker.MagicMock(spec=Session)
    return session

@pytest.fixture
def user_data():
    return UserRegister(username="testuser", password="securepassword")

@pytest.fixture
def user_login_data():
    return UserLogin(username="testuser", password="securepassword")

@pytest.fixture
def existing_user():
    """Simulate an existing user in the database"""
    return User(username="testuser", password_hash="hashed_securepassword")

def test_create_new_user(mock_db_session, mocker, user_data):
    mock_hashed_password = f"hashed_{user_data.password}"

    # Mock get_user_by_username to return None indicating no existing user
    mocker.patch('app.services.auth_service.get_user_by_username', return_value=None)

    # Mock the hash_password function to simulate hashing behavior
    mocker.patch('app.services.auth_service.hash_password', return_value=mock_hashed_password)

    mock_db_session.add = mocker.MagicMock()
    mock_db_session.commit = mocker.MagicMock()
    mock_db_session.refresh = mocker.MagicMock()

    user = create_user(mock_db_session, user_data)

    assert user.username == user_data.username
    assert user.password_hash == mock_hashed_password
    mock_db_session.add.assert_called_once_with(user)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(user)

def test_create_user_existing_username(mock_db_session, mocker, user_data, existing_user):
    # Mock get_user_by_username to return an existing user object
    mocker.patch('app.services.auth_service.get_user_by_username', return_value=existing_user)

    # Attempt to create a user with a username that already exists
    with pytest.raises(ValueError) as excinfo:
        create_user(mock_db_session, user_data)
    assert str(excinfo.value) == "Username already exists"

    # Ensure that the database add function was never called since username is duplicate
    mock_db_session.add.assert_not_called()

def test_authenticate_user(user_login_data, mock_db_session, mocker):
    hashed_password = hash_password(user_login_data.password)
    mock_user = User(username=user_login_data.username, password_hash=hashed_password)

    # Mock the get_user_by_username to return a user with a hashed password
    mocker.patch('app.services.auth_service.get_user_by_username', return_value=mock_user)

    user = authenticate_user(mock_db_session, username=user_login_data.username, password=user_login_data.password)
    assert user is not None
    assert user.username == user_login_data.username
