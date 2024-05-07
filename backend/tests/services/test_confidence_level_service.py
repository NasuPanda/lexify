import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.main import app
from app.models.confidence_level_model import ConfidenceLevel
from app.schemas.confidence_level import ConfidenceLevelCreate, ConfidenceLevelUpdate
from app.services.confidence_level_service import (
    get_confidence_level_by_id,
    get_confidence_levels_by_user_id,
    create_confidence_level,
    update_confidence_level,
    delete_confidence_level,
)

client = TestClient(app)

@pytest.fixture
def mock_db(mocker) -> Session:
    """
    Provides a mocked session object for database operations.

    :param mocker: Fixture to provide mocking functionality.
    :return: A mocked session object.
    """
    session_mock = mocker.create_autospec(Session, instance=True)
    session_mock.add = mocker.Mock()
    session_mock.commit = mocker.Mock()
    session_mock.delete = mocker.Mock()
    session_mock.query.return_value.filter_by.return_value.first.return_value = None
    session_mock.query.return_value.filter_by.return_value.all.return_value = []
    return session_mock

@pytest.fixture
def mock_confidence_level(mocker) -> ConfidenceLevel:
    """
    Provides a mocked ConfidenceLevel object.

    :param mocker: Fixture to provide mocking functionality.
    :return: A mocked ConfidenceLevel object.
    """
    return mocker.Mock(spec=ConfidenceLevel)

@pytest.fixture
def confidence_level_data() -> ConfidenceLevelCreate:
    """
    Provides sample data for creating a ConfidenceLevel.

    :return: ConfidenceLevelCreate object filled with predefined data.
    """
    return ConfidenceLevelCreate(
        description="Fairly confident",
        interval_days=3,
        is_default=False,
    )

@pytest.fixture
def updated_confidence_level_data():
    """
    Provides sample data for updating a ConfidenceLevel.

    :return: ConfidenceLevelUpdate object filled with updated data.
    """
    return ConfidenceLevelUpdate(
        description="Updated description",
        interval_days=10,
        is_default=True,
    )

@pytest.fixture
def mock_confidence_levels(mocker):
    """
    Creates a list of mocked ConfidenceLevel objects.

    :param mocker: Fixture to provide mocking functionality.
    :return: Function that generates a list of mocked ConfidenceLevel objects.
    """
    # Default setup, can be overridden in each test
    def _create_confidence_levels(user_id, number_of_objects):
        confidence_levels = [mocker.Mock(spec=ConfidenceLevel, user_id=user_id) for _ in range(number_of_objects)]
        return confidence_levels
    return _create_confidence_levels

def test_get_confidence_level_by_id(mock_db: Session, mock_confidence_level: ConfidenceLevel):
    """
    Tests retrieving a confidence level by ID.

    :param mock_db: Mocked database session.
    :param mock_confidence_level: Mocked ConfidenceLevel object.
    """
    c_level_id = 1
    mock_confidence_level.id = c_level_id
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_confidence_level

    confidence_level = get_confidence_level_by_id(mock_db, c_level_id)

    assert confidence_level is mock_confidence_level
    mock_db.query.assert_called_with(ConfidenceLevel)
    mock_db.query.return_value.filter_by.return_value.first.assert_called_once()

def test_get_confidence_levels_by_user_id(mock_db: Session, mock_confidence_levels: callable):
    """
    Tests the retrieval of multiple confidence levels by a user's ID.

    :param mock_db: Mocked database session.
    :param mock_confidence_levels: A callable fixture that returns a list of mocked ConfidenceLevel objects.
    """
    number_of_c_levels = 10
    user_id = 1
    mock_confidence_levels = mock_confidence_levels(user_id, number_of_c_levels)
    mock_db.query.return_value.filter_by.return_value.all.return_value = mock_confidence_levels

    confidence_levels = get_confidence_levels_by_user_id(mock_db, user_id)

    assert len(confidence_levels) == number_of_c_levels
    mock_db.query.assert_called_with(ConfidenceLevel)
    mock_db.query.return_value.filter_by.assert_called_with(user_id=confidence_levels[0].user_id)

def test_create_confidence_level(mock_db: Session, confidence_level_data: ConfidenceLevelCreate):
    """
    Tests the creation of a confidence level using provided data.

    :param mock_db: Mocked database session.
    :param confidence_level_data: Data for creating a new confidence level.
    """
    user_id = 1
    confidence_level = create_confidence_level(mock_db, confidence_level_data, user_id)

    mock_db.add.assert_called_once_with(confidence_level)
    mock_db.commit.assert_called_once()
    assert confidence_level.description == confidence_level_data.description
    assert confidence_level.interval_days == confidence_level_data.interval_days
    assert confidence_level.is_default == confidence_level_data.is_default

def test_create_confidence_level_database_error(mock_db: Session, confidence_level_data: ConfidenceLevelCreate):
    """
    Tests the error handling in the creation of a confidence level when a database error occurs.

    :param mock_db: Mocked database session.
    :param confidence_level_data: Data for creating a new confidence level.
    """
    user_id = 1
    mock_db.add.side_effect = SQLAlchemyError("Simulated database error")
    with pytest.raises(ValueError) as excinfo:
        create_confidence_level(mock_db, confidence_level_data, user_id)
    assert "database" in str(excinfo.value)
    mock_db.rollback.assert_called_once()

def test_update_confidence_level(
    mock_db: Session, mock_confidence_level: ConfidenceLevel, updated_confidence_level_data: ConfidenceLevelUpdate
):
    """
    Tests updating an existing confidence level with new data.

    :param mock_db: Mocked database session.
    :param mock_confidence_level: A mocked existing confidence level.
    :param updated_confidence_level_data: Data for updating the confidence level.
    """
    confidence_level_id = 1
    user_id = 1
    mock_confidence_level.id = confidence_level_id
    mock_confidence_level.user_id = user_id
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_confidence_level

    updated_confidence_level = update_confidence_level(mock_db, confidence_level_id, updated_confidence_level_data)

    assert updated_confidence_level is mock_confidence_level
    mock_db.commit.assert_called_once()
    assert updated_confidence_level.description == updated_confidence_level_data.description

def test_update_non_existent_confidence_level(mock_db: Session, updated_confidence_level_data: ConfidenceLevelUpdate):
    """
    Tests updating a non existing confidence level.

    :param mock_db: Mocked database session.
    :param updated_confidence_level_data: Data for updating the confidence level.
    """
    confidence_id = 10

    with pytest.raises(ValueError) as e:
        _confidence_level = update_confidence_level(mock_db, confidence_id, updated_confidence_level_data)
    assert f"{confidence_id} not found" in str(e.value)

def test_delete_confidence_level(mock_db: Session, mock_confidence_level: ConfidenceLevel):
    """Tests deleting a user.

    :param mock_db (Session): Mocked database session.
    :param mock_confidence_level (ConfidenceLevel): A mocked existing confidence level.
    """
    confidence_level_id = 1
    user_id = 1
    mock_confidence_level.id = confidence_level_id
    mock_confidence_level.user_id = user_id
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_confidence_level

    is_deleted = delete_confidence_level(mock_db, confidence_level_id)

    assert is_deleted is True
    mock_db.delete.assert_called_with(mock_confidence_level)
    mock_db.commit.assert_called_once()
