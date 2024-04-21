from sqlalchemy.orm import Session
from app.models.card_model import Card
from app.schemas.card import CardCreate

def create_card(card_data: CardCreate, user_id: int):
    card = Card(**card_data.dict(), user_id=user_id)
    # TODO: Add database add and commit logic
    return card

def get_card_by_id(db: Session, card_id: int, user_id: int):
    return db.query(Card).filter(Card.id == card_id, Card.user_id == user_id).first()
