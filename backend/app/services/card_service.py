from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.card_model import Card
from app.schemas.card import CardCreate, CardUpdate

def get_card_by_id(db: Session, card_id: int, user_id: int) -> Optional[Card]:
    """Retrieve a single card by its ID and user ID."""
    return db.query(Card).filter_by(id=card_id, user_id=user_id).first()

def get_cards_by_user_id(db: Session, user_id: int) -> List[Card]:
    """Retrieve all cards belonging to a specific user."""
    return db.query(Card).filter_by(user_id=user_id).all()

def create_card(db: Session, card_data: CardCreate, user_id: int) -> Optional[Card]:
    """Create a new card with the provided card data and associate it with a user."""
    new_card = Card(**card_data.dict(), user_id=user_id)
    db.add(new_card)
    db.commit()
    return new_card

def update_card(db: Session, card_id: int, user_id: int, card_data: CardUpdate) -> Optional[Card]:
    """Update an existing card with new data."""
    card_to_update = get_card_by_id(db, card_id, user_id)
    if not card_to_update:
        return None

    # exclude_unset: used to only include fields that were explicitly set in the update
    for attribute, value in card_data.dict(exclude_unset=True).items():
        setattr(card_to_update, attribute, value)
    db.commit()
    return card_to_update

def delete_card(db: Session, card_id: int, user_id: int) -> bool:
    """Delete a card by its ID and user ID."""
    card_to_delete = get_card_by_id(db, card_id, user_id)
    if not card_to_delete:
        return False

    db.delete(card_to_delete)
    db.commit()
    return True
