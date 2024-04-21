from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

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
    assert response.status_code == 200
    assert response.json() == {"message": "Card created successfully", "card_id": 1}
