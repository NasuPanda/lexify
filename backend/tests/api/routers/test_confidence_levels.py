import pytest

from httpx import AsyncClient

from app.main import app
from app.services.confidence_level_service import get_confidence_level_by_id, get_confidence_levels_by_user_id
from app.services.auth_service import get_user_by_username
from app.dependencies import get_db, get_current_user
from app.models.confidence_level_model import ConfidenceLevel
from tests.conftest import TestSessionContext

app.dependency_overrides[get_db] = lambda: TestSessionContext.session

def number_of_confidence_levels_belong_to_a_user(db, user_id: int) -> int:
    return db.query(ConfidenceLevel).filter(ConfidenceLevel.user_id == user_id).count()

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "password123"}

@pytest.fixture
def confidence_level_data():
    return {
        "description": "mid-confident",
        "interval_days": 3,
        "is_default": False,
    }

@pytest.fixture
def async_client():
    return AsyncClient(app=app, base_url="http://testserver")

@pytest.mark.asyncio
async def test_retrieve_confidence_level_endpoint(db, async_client, user_data, confidence_level_data):
    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user

        _res = await c.post("/confidence-levels", json=confidence_level_data)
        new_confidence_level = get_confidence_levels_by_user_id(db, new_user.id)[0]

        # Get the newly created c_level
        response = await c.get(f"/confidence-levels/{new_confidence_level.id}")

    response_data = response.json()
    assert response.status_code == 200
    assert response_data['id'] == new_confidence_level.id
    assert response_data['description'] == new_confidence_level.description
    assert response_data['interval_days'] == new_confidence_level.interval_days

@pytest.mark.asyncio
async def test_list_confidence_levels_endpoint(db, async_client, user_data, confidence_level_data):
    number_of_confidence_levels = 10

    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user

        # Create new confidence levels
        for _ in range(number_of_confidence_levels):
            _res = await c.post("/confidence-levels", json=confidence_level_data)

        response = await c.get("/confidence-levels")
        response_data = response.json()

    assert response.status_code == 200
    assert isinstance(response_data, list)
    assert len(response_data) == number_of_confidence_levels

@pytest.mark.asyncio
async def test_create_confidence_level_endpoint(db, async_client, user_data, confidence_level_data):
    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user

        # Store the number of c_levels at this point
        initial_confidence_level_count = number_of_confidence_levels_belong_to_a_user(db, new_user.id)

        # Create and retrieve a new one
        response = await c.post("/confidence-levels", json=confidence_level_data)

    assert response.status_code == 201
    assert number_of_confidence_levels_belong_to_a_user(db, new_user.id) == initial_confidence_level_count + 1

@pytest.mark.asyncio
async def test_update_confidence_level_endpoint(db, async_client, user_data, confidence_level_data):
    new_description_for_update = "Perfectly confident"
    new_interval_days_for_update = 10

    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user

        # Create and store a new one
        _res = await c.post("/confidence-levels", json=confidence_level_data)
        original_confidence_level = get_confidence_levels_by_user_id(db=db, user_id=new_user.id)[0]

        # Update the confidence level
        response = await c.put(
            f"/confidence-levels/{original_confidence_level.id}",
            json={
                "description": new_description_for_update,
                "interval_days": new_interval_days_for_update},
        )
        response_data = response.json()

    assert response.status_code == 200
    assert response_data["description"] == new_description_for_update
    assert response_data["description"] != confidence_level_data["description"]
    assert response_data["interval_days"] == new_interval_days_for_update
    assert response_data["interval_days"] != confidence_level_data["interval_days"]

@pytest.mark.asyncio
async def test_delete_confidence_level_endpoint(db, async_client, user_data, confidence_level_data):
    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user

        # Create a new confidence_level
        _res = await c.post("/confidence-levels", json=confidence_level_data)

        # Store the number of confidence_levels at this point
        confidence_level_count_before_deletion = number_of_confidence_levels_belong_to_a_user(db, new_user.id)
        created_confidence_level = get_confidence_levels_by_user_id(db=db, user_id=new_user.id)[0]

        response = await c.delete(f"/confidence-levels/{created_confidence_level.id}")

    assert response.status_code == 204
    assert response.json() == {"message": "Confidence level deleted successfully"}
    assert number_of_confidence_levels_belong_to_a_user(db, new_user.id) == confidence_level_count_before_deletion - 1

