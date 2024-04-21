from app.models.card_model import Card
from app.schemas.card import CardCreate

def create_card(card_data: CardCreate, user_id: int):
    card = Card(**card_data.dict(), user_id=user_id)
    # TODO: Add database add and commit logic
    return card
