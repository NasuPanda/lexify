import pytest

from httpx import AsyncClient

from app.main import app
from app.services.auth_service import get_user_by_username
from app.dependencies import get_db, get_current_user
from app.services.auth_service import get_user_by_username
from app.services.card_service import get_cards_by_user_id
from app.models.card_model import Card
from tests.conftest import TestSessionContext

app.dependency_overrides[get_db] = lambda: TestSessionContext.session

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "password123"}

@pytest.fixture
def default_confidence_level_data():
    return {
        "description": "default confidence level", "interval_days": 3, "is_default": True,
    }

@pytest.fixture
def card_data():
    return {
        "term": "Example",
        "definition": "A thing characteristic of its kind or illustrating a general rule.",
        "example_sentence": "Pumpkin and penguins!"
    }

@pytest.fixture
def async_client():
    return AsyncClient(app=app, base_url="http://testserver")

@pytest.mark.asyncio
async def test_create_new_card(db, async_client, user_data, default_confidence_level_data, card_data):
    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user
        # Register the default confidence level
        _res = await c.post("/confidence-levels", json=default_confidence_level_data)

        # Store the number of cards at this point (should be 0)
        initial_card_count = db.query(Card).filter(Card.user_id == new_user.id).count()

        response = await c.post("/cards", json=card_data)

    assert response.status_code == 201
    assert db.query(Card).filter(Card.user_id == new_user.id).count() == initial_card_count + 1

@pytest.mark.asyncio
async def test_retrieve_card(db, async_client, user_data, default_confidence_level_data, card_data):
    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user
        # Register the default confidence level
        _res = await c.post("/confidence-levels", json=default_confidence_level_data)

        # Create a new card
        _res = await c.post("/cards", json=card_data)
        new_card = get_cards_by_user_id(db, new_user.id)[0]

        # Get the newly created card
        response = await c.get(f"cards/{new_card.id}")

    response_data = response.json()
    assert response.status_code == 200
    assert response_data['id'] == new_card.id
    assert response_data['term'] == new_card.term
    assert response_data['definition'] == new_card.definition

@pytest.mark.asyncio
async def test_list_cards(db, async_client, user_data, default_confidence_level_data, card_data):
    number_of_cards = 10

    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user
        # Register the default confidence level
        _res = await c.post("/confidence-levels", json=default_confidence_level_data)

        # Create new cards
        for _ in range(number_of_cards):
            _res = await c.post("/cards", json=card_data)

        response = await c.get("/cards")
        response_data = response.json()

    assert response.status_code == 200
    assert isinstance(response_data, list)
    assert len(response_data) == number_of_cards

@pytest.mark.asyncio
async def test_update_card_details(db, async_client, user_data, default_confidence_level_data, card_data):
    new_term_for_update = "Dawn"

    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user
        # Register the default confidence level
        _res = await c.post("/confidence-levels", json=default_confidence_level_data)

        # Create a new card
        _res = await c.post("/cards", json=card_data)

        original_card = get_cards_by_user_id(db=db, user_id=new_user.id)[0]

        # Update the card
        response = await c.put(f"/cards/{original_card.id}", json={"term": new_term_for_update})
        response_data = response.json()

    assert response.status_code == 200
    assert response_data['term'] == new_term_for_update

@pytest.mark.asyncio
async def test_delete_card_endpoint(db, async_client, user_data, default_confidence_level_data, card_data):
    async with async_client as c:
        # Register a new user and override the current user dependency
        _res = await c.post("/auth/register", json=user_data)
        new_user = get_user_by_username(db, user_data["username"])
        app.dependency_overrides[get_current_user] = lambda: new_user
        # Register the default confidence level
        _res = await c.post("/confidence-levels", json=default_confidence_level_data)

        # Create a new card
        _res = await c.post("/cards", json=card_data)

        # Store the number of cards at this point
        card_count_before_deletion = db.query(Card).filter(Card.user_id == new_user.id).count()

        response = await c.delete(f"/cards/{get_cards_by_user_id(db, new_user.id)[0].id}")

    assert response.status_code == 204
    assert response.json() == {"message": "Card deleted successfully"}
    assert db.query(Card).filter(Card.user_id == new_user.id).count() == card_count_before_deletion - 1
