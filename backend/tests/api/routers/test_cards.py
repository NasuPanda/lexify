from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.main import app
from app.models.card_model import Card

client = TestClient(app)

def create_mock_card(db, user_id):
    # This function simulates the insertion of a card into the database
    # TODO: In a real testing environment, you would use a database session to add and commit this data
    mock_card = Card(
        id=1,
        term="Example",
        definition="A thing characteristic of its kind or illustrating a general rule.",
        example_sentence="Pumpkin and penguins!",
        user_id=user_id
    )
    db.add(mock_card)
    db.commit()
    return mock_card


def test_retrieve_card():
    user_id = 1  # Mocked user ID for authentication

    # Setup: Mock the dependencies
    with patch('app.api.routers.cards.get_db') as mock_db, \
        patch('app.api.routers.cards.get_current_user', return_value={'id': user_id}):

        # Assuming get_db is properly mocked to provide a Session object that would work with our mock
        mock_session = Mock(spec=Session)
        mock_db.return_value = mock_session

        # Create a mock card using our helper function
        create_mock_card(mock_session, user_id)

        # Attempt to retrieve the mock card
        response = client.get("/cards/1")

    # Assertions to ensure the correct function was called and the response is as expected
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['term'] == "Example"

def test_list_cards():
    user_id = 1  # Mocked user ID for authentication
    number_of_cards = 10

    # Setup: Mock the dependencies
    with patch('app.api.routers.cards.get_db') as mock_db, \
        patch('app.api.routers.cards.get_current_user', return_value={'id': user_id}):

        # Assuming get_db is properly mocked to provide a Session object that would work with our mock
        mock_session = Mock(spec=Session)
        mock_db.return_value = mock_session

        # Create mock cards
        [create_mock_card(mock_session, user_id) for __ in range(number_of_cards)]

        # Attempt to retrieve the mock card
        response = client.get("/cards")

    assert response.status_code == 200
    assert isinstance(response.json(), list) # Verify that a list is returned
    assert len(response.json()) == number_of_cards

def test_create_new_card():
    card_data = {
        "term": "Example",
        "definition": "A thing characteristic of its kind or illustrating a general rule.",
        "example_sentence": "Pumpkin and penguins!"
    }
    user_id = 1  # Mocked user ID for authentication

    # Mock the dependency that provides the user
    with patch('app.api.routers.cards.get_current_user', return_value={'id': user_id}):
        response = client.post("/cards", json=card_data)

    # Check the response from API
    assert response.status_code == 201
    assert response.json() == {"message": "Card created successfully", "card_id": 1}

def test_update_card_details():
    user_id = 1  # Mocked user ID for authentication

    # Setup: Mock the dependencies
    with patch('app.api.routers.cards.get_db') as mock_db, \
        patch('app.api.routers.cards.get_current_user', return_value={'id': user_id}):

        # Assuming get_db is properly mocked to provide a Session object that would work with our mock
        mock_session = Mock(spec=Session)
        mock_db.return_value = mock_session

        # Create a mock card using our helper function
        create_mock_card(mock_session, user_id)

    response = client.put("/cards/1", json={"term": "Updated term"})
    assert response.status_code == 200
    assert response.json()['term'] == "Updated term"

def test_delete_card_endpoint(mock_db):
    user_id = 1  # Mocked user ID for authentication
    card_id = 1

    # Setup: Mock the dependencies
    with patch('app.api.routers.cards.get_db') as mock_db, \
        patch('app.api.routers.cards.get_current_user', return_value={'id': user_id}):

        # Assuming get_db is properly mocked to provide a Session object that would work with our mock
        mock_session = Mock(spec=Session)
        mock_db.return_value = mock_session

        # Create a mock card using our helper function
        create_mock_card(mock_session, user_id)

        # Get the response from /DELETE
        response = client.delete(f"/cards/{card_id}")

    assert response.status_code == 204
    assert response.json() == {"message": "Card deleted successfully"}
