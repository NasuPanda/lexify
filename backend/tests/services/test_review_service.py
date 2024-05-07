import pytest
from sqlalchemy.orm import Session
from app.models.review_model import ReviewSchedule
from app.services.review_service import (
    get_review_schedule_by_id,
    get_review_schedules_by_user_id,
    create_review_schedule,
    update_review_schedule,
    delete_review_schedule
)
from app.schemas.review import ReviewScheduleCreate, ReviewScheduleUpdate


@pytest.fixture
def mock_db(mocker):
    session_mock = mocker.create_autospec(Session, instance=True)
    session_mock.add = mocker.Mock()
    session_mock.commit = mocker.Mock()
    session_mock.delete = mocker.Mock()
    session_mock.query.return_value.filter.return_value.first.return_value = None
    session_mock.query.return_value.filter.return_value.all.return_value = []
    return session_mock

@pytest.fixture
def review_data():
    return ReviewScheduleCreate(
        card_id=1,
        user_id=1,
        review_date="2022-01-01T00:00:00"
    )

@pytest.fixture
def mock_review_schedule(mocker):
    return mocker.Mock(spec=ReviewSchedule)

@pytest.fixture
def mock_review_schedules(mocker):
    def _create_mock_reviews(number_of_reviews):
        mock_reviews = [mocker.Mock(spec=ReviewSchedule(id=id)) for id in range(number_of_reviews)]
        return mock_reviews
    return _create_mock_reviews

def test_get_review_schedule_by_id(mock_db, mock_review_schedule):
    review_id = 1
    mock_review_schedule.id = review_id
    mock_db.query.return_value.filter.return_value.first.return_value = mock_review_schedule

    review_schedule = get_review_schedule_by_id(mock_db, review_id)

    assert review_schedule is mock_review_schedule
    mock_db.query.assert_called_with(ReviewSchedule)

    # Check that filter was called, not assert_called_with due to issues with SQLAlchemy expression objects
    assert mock_db.query.return_value.filter.called, "Filter method was not called"

def test_get_review_schedules_by_user_id(mock_db, mock_review_schedule):
    user_id = 1
    number_of_reviews = 5
    mock_review_schedules = []
    for i in range(number_of_reviews):
        review = mock_review_schedule
        review.review_id = i
        review.user_id = user_id
        mock_review_schedules.append(review)

    mock_db.query.return_value.filter.return_value.all.return_value = mock_review_schedules
    review_schedules = get_review_schedules_by_user_id(mock_db, user_id)

    assert len(review_schedules) == number_of_reviews
    mock_db.query.assert_called_with(ReviewSchedule)

def test_create_review_schedule(mock_db, review_data):
    review_schedule = create_review_schedule(mock_db, review_data)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    assert review_schedule is not None

def test_update_review_schedule(mock_db, mock_review_schedule, review_data):
    review_id = 1
    mock_review_schedule.id = review_id
    mock_db.query.return_value.filter.return_value.first.return_value = mock_review_schedule

    updated_review_schedule = update_review_schedule(mock_db, review_id, review_data)

    mock_db.commit.assert_called_once()
    assert updated_review_schedule is not None

def test_delete_review_schedule(mock_db, mock_review_schedule):
    review_id = 1
    mock_review_schedule.id = review_id
    mock_db.query.return_value.filter.return_value.first.return_value = mock_review_schedule

    success = delete_review_schedule(mock_db, review_id)

    mock_db.delete.assert_called_with(mock_review_schedule)
    mock_db.commit.assert_called_once()
    assert success is True
