import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.services.card_service import create_card, delete_card, get_card_by_id, update_card, get_cards_by_user_id
from app.schemas.card import CardCreate, CardUpdate
from app.models.card_model import Card

client = TestClient(app)

@pytest.fixture
def mock_db(mocker):
    session_mock = mocker.create_autospec(Session, instance=True)
    session_mock.add = mocker.Mock()
    session_mock.commit = mocker.Mock()
    session_mock.delete = mocker.Mock()
    session_mock.query.return_value.filter_by.return_value.first.return_value = None
    session_mock.query.return_value.filter_by.return_value.all.return_value = []
    return session_mock

@pytest.fixture
def mock_card(mocker):
    return mocker.Mock(spec=Card)

@pytest.fixture
def card_data():
    return CardCreate(
        term="Example",
        definition="A thing characteristic of its kind or illustrating a general rule.",
        example_sentence="Don't forget to be an example!",
        image_url="http://example.com/image.png",
        audio_url="http://example.com/audio.mp3",
    )

@pytest.fixture
def updated_card_data():
    return CardUpdate(
        term="Updated Example",
        definition="An updated thing characteristic of its kind or illustrating a general rule.",
        example_sentence="Always remember to update examples!"
    )

@pytest.fixture
def mock_cards(mocker):
    # Default setup, can be overridden in each test
    def _create_mock_cards(user_id, number_of_cards):
        mock_cards = [mocker.Mock(spec=Card, user_id=user_id) for _ in range(number_of_cards)]
        return mock_cards
    return _create_mock_cards

def test_get_card_by_id(mock_db, mock_card):
    user_id = 1
    card_id = 1
    mock_card.id = card_id
    mock_card.user_id = user_id
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_card

    card = get_card_by_id(mock_db, card_id, user_id)

    assert card is mock_card
    mock_db.query.assert_called_with(Card)
    mock_db.query.return_value.filter_by.return_value.first.assert_called_once()

def test_get_cards_by_user_id(mock_db, mock_cards):
    number_of_cards = 10
    user_id = 1
    mock_cards = mock_cards(user_id, number_of_cards)
    mock_db.query.return_value.filter_by.return_value.all.return_value = mock_cards

    cards = get_cards_by_user_id(mock_db, user_id)

    assert len(cards) == number_of_cards
    mock_db.query.assert_called_with(Card)
    mock_db.query.return_value.filter_by.assert_called_with(user_id=cards[0].user_id)

def test_create_card(mock_db, card_data):
    user_id = 1
    card = create_card(mock_db, card_data, user_id)

    mock_db.add.assert_called_once_with(card)
    mock_db.commit.assert_called_once()
    assert card.term == card_data.term
    assert card.definition == card_data.definition
    assert card.example_sentence == card_data.example_sentence

def test_create_card_with_required_fields_only(mock_db):
    """POST /cards: Card creation with minimal data"""
    user_id = 1
    minimum_card_data = CardCreate(
        term="Minimum",
        definition="Possible least amount.",
    )
    card_with_minimum_data = create_card(mock_db, minimum_card_data, user_id)
    mock_db.add.assert_called_once_with(card_with_minimum_data)
    mock_db.commit.assert_called_once()
    assert card_with_minimum_data.term == minimum_card_data.term
    assert not card_with_minimum_data.example_sentence

def test_update_card(mock_db, mock_card, updated_card_data):
    """PUT /cards/{id}: Card update"""
    card_id = 1
    user_id = 1
    mock_card.id = card_id
    mock_card.user_id = user_id
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_card

    card = update_card(mock_db, card_id, user_id, updated_card_data)

    assert card is mock_card
    mock_db.commit.assert_called_once()
    assert card.term == updated_card_data.term

def test_update_card_with_partial_data(mock_db, mock_card):
    """PUT /cards/{id}: update card with partial data"""
    unchanged_definition = mock_card.definition
    unchanged_example_sentence  = mock_card.example_sentence

    card_id = 1
    user_id = 1
    mock_card.id = card_id
    mock_card.user_id = user_id
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_card

    card_data_with_term_only = CardUpdate(term="Updated Example")
    updated_card = update_card(mock_db, card_id, user_id, card_data_with_term_only)

    assert updated_card is mock_card
    assert updated_card.term == card_data_with_term_only.term
    assert updated_card.definition == unchanged_definition
    assert updated_card.example_sentence == unchanged_example_sentence

def test_update_non_existent_card(mock_db, updated_card_data):
    card_id = 10
    user_id = 1

    card = update_card(mock_db, card_id, user_id, updated_card_data)
    assert card is None

def test_delete_card(mock_db, mock_card):
    """DELETE /cards/{id}: Delete card"""
    card_id = 1
    user_id = 1
    mock_card.id = card_id
    mock_card.user_id = user_id
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_card

    is_deleted = delete_card(mock_db, card_id, user_id)

    assert is_deleted is True
    mock_db.delete.assert_called_with(mock_card)
    mock_db.commit.assert_called_once()
