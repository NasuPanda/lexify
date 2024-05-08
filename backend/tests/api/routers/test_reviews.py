from datetime import datetime, timedelta
import pytest

from httpx import AsyncClient

from app.main import app
from app.services.auth_service import get_user_by_username
from app.dependencies import get_db, get_current_user
from app.services.auth_service import get_user_by_username
from app.services.review_service import create_review_schedule, get_review_schedules_by_user_id
from app.services.card_service import create_card
from app.schemas.review import ReviewScheduleCreate
from app.schemas.card import CardCreate
from tests.conftest import TestSessionContext

app.dependency_overrides[get_db] = lambda: TestSessionContext.session

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "password123"}

@pytest.fixture
def card_data():
    return CardCreate(
        term="Example",
        definition="A thing characteristic of its kind or illustrating a general rule.",
        example_sentence="Pumpkin and penguins!",
    )

@pytest.fixture
def review_schedule_data():
    return ReviewScheduleCreate(
        review_date=datetime(2024, 5, 7),
        user_id=1,
        card_id=1,
    )

@pytest.fixture
def default_confidence_level_data():
    return {
        "description": "default confidence level", "interval_days": 3, "is_default": True,
    }

@pytest.fixture
def async_client():
    return AsyncClient(app=app, base_url="http://testserver")

@pytest.mark.asyncio
async def test_get_due_review_schedules(
    db, async_client, user_data, card_data, default_confidence_level_data, review_schedule_data
):
    """
    Tests the API endpoint to retrieve all due review schedules for the current user.
    This endpoint should return only the review schedules that are due based on the current date,
    ensuring that only relevant review tasks are presented to the user.

    Args:
    - db (Session): The database session to access the database.
    - async_client (AsyncClient): The test client used for making asynchronous API calls.
    - user_data, card_data, default_confidence_level_data, review_schedule_data: Dictionaries providing the necessary data to set up the test conditions, including user and card details, confidence levels, and review schedules.

    Ensures:
    - The API returns a 200 status code for a successful retrieval.
    - The number of returned review schedules matches the number expected to be due.
    """
    number_of_review_schedules = 3

    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user
        # Register the default confidence level
        _res = await c.post("/confidence-levels", json=default_confidence_level_data)

        user_id = new_user.id
        for _ in range(number_of_review_schedules):
            card = create_card(db, card_data, user_id)
            review_schedule_data.user_id = user_id
            review_schedule_data.card_id = card.id
            create_review_schedule(db, review_schedule_data)

        response = await c.get("/review-schedules")
        response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == number_of_review_schedules

@pytest.mark.asyncio
async def test_list_review_schedules_for_review_session_endpoint(
    db, async_client, user_data, card_data, default_confidence_level_data, review_schedule_data
):
    """
    Tests the API endpoint for listing review schedules that should be included in a review session.
    It checks if the endpoint correctly filters out review schedules based on the current time,
    including only those schedules whose review dates are on or before the current time.

    Args:
    - db (Session): The database session to access the database.
    - async_client (AsyncClient): The test client used for making asynchronous API calls.
    - user_data, card_data, default_confidence_level_data, review_schedule_data: Dictionaries providing the necessary data to set up the test conditions, including user and card details, confidence levels, and review schedules.

    Ensures:
    - The API returns a 200 status code indicating successful data retrieval.
    - The returned data set excludes any review schedules set for dates after the current time, thus confirming correct filtering logic.
    """
    # Setup
    number_of_review_schedules = 3
    number_of_reviews_should_be_in_review_session = 2

    current_time = datetime(2024, 5, 8, 15, 0, 0)
    date_before_the_current = datetime(2024, 5, 9, 12, 0, 0) # This should not be fetched
    date_equals_current = current_time                       # This should be fetched
    date_pass_the_current = datetime(2024, 5, 8, 12, 0, 0)   # This should be fetched
    mock_date_times = [date_pass_the_current, date_before_the_current, date_equals_current]

    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user
        # Register the default confidence level
        _res = await c.post("/confidence-levels", json=default_confidence_level_data)

        # Create review schedules for testing
        user_id = new_user.id
        for dt in mock_date_times:
            card = create_card(db, card_data, user_id)
            review_schedule_data.review_date = dt
            review_schedule_data.user_id = user_id
            review_schedule_data.card_id = card.id
            create_review_schedule(db, review_schedule_data)

        response = await c.get("/review-schedules/session")
        response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) != number_of_review_schedules
    assert len(response_data) == number_of_reviews_should_be_in_review_session

@pytest.mark.asyncio
async def test_complete_review_session_endpoint(
    db, async_client, user_data, card_data, default_confidence_level_data, review_schedule_data
):
    """
    Tests the functionality of the API endpoint designed to handle the completion of a review session.
    This includes ensuring that the review schedules are updated correctly based on the defined interval days
    after completing a review, as dictated by the associated confidence levels.

    Args:
    - db (Session): The database session, for database interactions.
    - async_client (AsyncClient): The client used to make asynchronous API requests.
    - user_data, card_data, default_confidence_level_data, review_schedule_data: Dictionaries providing the necessary data to set up the test conditions, including user and card details, confidence levels, and review schedules.

    Ensures:
    - The API responds with a 204 status code, indicating that the review schedules were successfully updated.
    - The response contains a confirmation message stating that the update was successful.
    - The review dates of the schedules are updated correctly to reflect the new intervals as expected post-review.
    """
    interval_days = default_confidence_level_data["interval_days"]
    test_date_may_seventh = datetime(2024, 5, 7)
    test_date_may_eighth = datetime(2024, 5, 8)
    mock_date_times = [test_date_may_seventh, test_date_may_eighth]

    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user
        # Register the default confidence level
        _res = await c.post("/confidence-levels", json=default_confidence_level_data)

        user_id = new_user.id
        for dt in mock_date_times:
            card = create_card(db, card_data, user_id)
            review_schedule_data.user_id = user_id
            review_schedule_data.card_id = card.id
            review_schedule_data.review_date = dt
            create_review_schedule(db, review_schedule_data)

        response = await c.post("/review-schedules/complete")
        review_schedules = get_review_schedules_by_user_id(db, user_id)
        review_schedules.sort(key=lambda x: x.review_date)

    assert response.status_code == 204
    assert response.json() == {"message": "Review schedules updated successfully"}
    assert review_schedules[0].review_date == test_date_may_seventh + timedelta(days=interval_days), \
        "Review date should be updated correctly based on the confidence level interval"
    assert review_schedules[1].review_date == test_date_may_eighth + timedelta(days=interval_days), \
        "Review date should be updated correctly based on the confidence level interval"
