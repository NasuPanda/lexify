from sqlalchemy.orm import Session
from app.models.card_model import Card
from app.schemas.card import CardCreate, CardUpdate

def get_card_by_id(db: Session, card_id: int, user_id: int):
    return db.query(Card).filter(Card.id == card_id, Card.user_id == user_id).first()

def create_card(card_data: CardCreate, user_id: int):
    card = Card(**card_data.dict(), user_id=user_id)
    # TODO: Add database add and commit logic
    return card

def update_card(db: Session, card_id: int, user_id: int, card_data: CardUpdate):
    card = db.query(Card).filter(Card.id == card_id, Card.user_id == user_id).first()
    if card:
        for var, value in vars(card_data).items():
            if value is not None:
                setattr(card, var, value)
        db.commit()
        return card
    return None
