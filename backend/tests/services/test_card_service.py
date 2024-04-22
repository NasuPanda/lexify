from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import Mock
import pytest
from app.services.card_service import create_card, delete_card, get_card_by_id, update_card
from app.schemas.card import CardCreate

client = TestClient(app)

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def card_data():
    return CardCreate(
        term="Example",
        definition="A thing characteristic of its kind or illustrating a general rule.",
        example_sentence="Don't forget to be an example!"
    )

def test_get_card_by_id(mock_db):
    user_id = 1
    # Call the service function
    card = create_card(mock_db, card_data, user_id)

    # Assume db and setup are mocked or a fixture is used
    assert get_card_by_id(mock_db, 1, 1).id == 1

def test_create_card(mock_db, card_data):
    user_id = 1  # Assuming a user ID is needed for card creation

    # Call the service function
    card = create_card(mock_db, card_data, user_id)

    # Assert that the database add was called correctly
    mock_db.add.assert_called_with(card)
    mock_db.commit.assert_called_once()

    # Check that the card object has the correct attributes
    assert card.term == card_data.term
    assert card.definition == card_data.definition
    assert card.user_id == user_id

def test_update_card(card_data):
    # Save the original term and update it
    original_term = card_data["term"]
    updated_term = "Updated term"
    card_data["term"] = updated_term
    updated_card = update_card(db=mock_db, card_id=1, user_id=1, card_data=card_data).term

    assert updated_card.term == updated_term
    assert updated_card.term != original_term

def test_delete_card(mock_db):
    user_id = 1
    card_id = 1
    # Call the service function
    card = create_card(mock_db, card_data, user_id)

    assert delete_card(mock_db, card_id, user_id) is True
