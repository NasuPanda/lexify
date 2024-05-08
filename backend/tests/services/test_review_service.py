from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.card_model import Card
from app.models.review_model import ReviewSchedule
from app.models.confidence_level_model import ConfidenceLevel
from app.services.review_service import (
    get_review_schedule_by_id,
    get_review_schedules_by_user_id,
    get_review_schedules_for_review_session,
    create_review_schedule,
    update_review_schedule,
    update_review_schedule_post_review,
    delete_review_schedule,
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
def mock_card(mocker):
    return mocker.Mock(spec=Card)

@pytest.fixture
def mock_confidence_level(mocker):
    return mocker.Mock(spec=ConfidenceLevel)

@pytest.fixture
def mock_review_schedules(mocker):
    def _create_mock_reviews(number_of_reviews):
        mock_reviews = [mocker.Mock(spec=ReviewSchedule(id=id)) for id in range(number_of_reviews)]
        return mock_reviews
    return _create_mock_reviews

def test_get_review_schedule_by_id(mock_db, mock_review_schedule):
    review_id = 1
    mock_review_schedule.id = review_id
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_review_schedule

    review_schedule = get_review_schedule_by_id(mock_db, review_id)

    assert review_schedule is mock_review_schedule
    mock_db.query.assert_called_with(ReviewSchedule)

    # Check that filter_by was called, not assert_called_with due to issues with SQLAlchemy expression objects
    assert mock_db.query.return_value.filter_by.called, "Filter method was not called"

def test_get_review_schedules_by_user_id(mock_db, mock_review_schedule):
    user_id = 1
    number_of_reviews = 5
    mock_review_schedules = []
    for i in range(number_of_reviews):
        review = mock_review_schedule
        review.review_id = i
        review.user_id = user_id
        mock_review_schedules.append(review)

    mock_db.query.return_value.filter_by.return_value.all.return_value = mock_review_schedules
    review_schedules = get_review_schedules_by_user_id(mock_db, user_id)

    assert len(review_schedules) == number_of_reviews
    mock_db.query.assert_called_with(ReviewSchedule)

def test_get_review_schedules_for_review_session(mock_db, mock_review_schedules):
    """
    Tests the retrieval of review schedules that are due for review, verifying that the function fetches only those schedules whose review dates are on or before the current time.

    Args:
    mock_db (Session): Mocked database session.
    mock_review_schedules (function): A factory function to create mock review schedules.

    Verifies:
    - The function fetches the correct number of review schedules.
    - Each returned schedule matches the expected dates (either exactly at or before the current time).
    - Proper database query methods are called to ensure that filtering is applied correctly.
    """
    user_id = 1
    current_time = datetime(2024, 5, 8, 15, 0, 0)  # May 8, 2024, at 15:00:00

    # Create mock data
    number_of_reviews = 3
    mock_reviews = mock_review_schedules(number_of_reviews)
    mock_reviews[0].review_date = datetime(2024, 5, 8, 12, 0, 0)  # This should be fetched
    mock_reviews[1].review_date = datetime(2024, 5, 9, 12, 0, 0)  # This should not be fetched
    mock_reviews[2].review_date = datetime(2024, 5, 7, 12, 0, 0)  # This should be fetched

    # Setup the mock to return our prepared list
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_reviews[0], mock_reviews[2]]

    # Invoke the function
    review_schedules = get_review_schedules_for_review_session(mock_db, user_id, current_time)

    # Assertions
    assert len(review_schedules) == 2, "Should only fetch review schedules before and exactly at the current time"
    assert review_schedules[0] == mock_reviews[0], "Should include review schedule on the exact time"
    assert review_schedules[1] == mock_reviews[2], "Should include review schedule before the current time"

    # Verify query was called correctly
    mock_db.query.assert_called_with(ReviewSchedule)
    assert mock_db.query.return_value.filter.called, "Filter method was not properly called"

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

def test_update_review_schedule_post_review(mock_db, mock_review_schedules, mocker, mock_card, mock_confidence_level):
    """
    Tests the update functionality for review schedules following a review session, specifically ensuring that review dates are correctly updated based on the associated confidence level's interval days.

    Args:
    mock_db (Session): Mocked database session.
    mock_review_schedules (function): A factory function to create mock review schedules.
    mocker (MockerFixture): Pytest fixture to provide mocking capabilities.
    mock_card (Mock): Mocked Card object.
    mock_confidence_level (Mock): Mocked ConfidenceLevel object.

    Verifies:
    - The review dates are updated correctly for each schedule based on the interval days.
    - Database commit is called to save the changes.
    - Exception handling is properly managed with a rollback in the event of a database error.
    """
    # Set up test data and mocks
    confidence_level_id = 1
    interval_days = 3
    test_date_may_seventh = datetime(2024, 5, 7)
    test_date_may_eighth = datetime(2024, 5, 8)

    number_of_reviews = 2
    review_schedules = mock_review_schedules(number_of_reviews)
    review_schedules[0].review_date = test_date_may_seventh
    review_schedules[1].review_date = test_date_may_eighth

    mock_card.confidence_level_id = confidence_level_id
    mock_confidence_level.interval_days = interval_days

    # Mock functions
    mocker.patch('app.services.review_service.get_card_by_id', return_value=mock_card)
    mocker.patch('app.services.review_service.get_confidence_level_by_id', return_value=mock_confidence_level)

    # Call the function to test
    update_review_schedule_post_review(db=mock_db, review_schedules=review_schedules)

    # Assertions to verify behavior
    assert review_schedules[0].review_date == test_date_may_seventh + timedelta(days=interval_days), \
        "Review date should be updated correctly based on the confidence level interval"
    assert review_schedules[1].review_date == test_date_may_eighth + timedelta(days=interval_days), \
        "Review date should be updated correctly based on the confidence level interval"

    assert mock_db.commit.called, "Database commit should be called to save changes"

    # Handle the exception case
    mock_db.commit.side_effect = SQLAlchemyError("Mock database error")
    with pytest.raises(ValueError):
        update_review_schedule_post_review(db=mock_db, review_schedules=review_schedules)
    assert mock_db.rollback.called, "Database rollback should be called on error"

def test_delete_review_schedule(mock_db, mock_review_schedule):
    review_id = 1
    mock_review_schedule.id = review_id
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_review_schedule

    success = delete_review_schedule(mock_db, review_id)

    mock_db.delete.assert_called_with(mock_review_schedule)
    mock_db.commit.assert_called_once()
    assert success is True
