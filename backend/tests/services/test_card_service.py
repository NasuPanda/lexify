from unittest.mock import Mock
import pytest
from app.services.card_service import create_card
from app.schemas.card import CardCreate

@pytest.fixture
def card_data():
    return CardCreate(
        term="Example",
        definition="A thing characteristic of its kind or illustrating a general rule.",
        example_sentence="Don't forget to be an example!"
    )

def test_create_card(card_data):
    mock_db = Mock()
    user_id = 1  # Assuming a user ID is needed for card creation

    # Call the service function
    card = create_card(card_data, user_id)

    # Assert that the database add was called correctly
    mock_db.add.assert_called_with(card)
    mock_db.commit.assert_called_once()

    # Check that the card object has the correct attributes
    assert card.term == card_data.term
    assert card.definition == card_data.definition
    assert card.user_id == user_id
