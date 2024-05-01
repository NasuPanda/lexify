from typing import List, Optional

from app.models.card_model import Card
from app.models.review_model import ReviewSchedule
from app.schemas.card import CardCreate, CardUpdate
from app.schemas.review import ReviewScheduleCreate, ReviewScheduleUpdate
from app.services.confidence_level_service import get_default_confidence_level
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload


def get_card_by_id(db: Session, card_id: int, user_id: int) -> Optional[Card]:
    """Retrieve a single card by its ID and user ID."""
    try:
        card = db.query(Card).filter_by(id=card_id, user_id=user_id).first()
        if not card:
            raise ValueError(f"No card found with ID {card_id} for user {user_id}")
        return card
    except Exception as e:
        # Optionally log the error
        print(f"Failed to fetch card: {e}")
        raise

def get_card_details_by_id(db: Session, card_id: int, user_id: int) -> Optional[Card]:
    """Retrieve a single card by its ID along with its review schedule and confidence level."""
    return db.query(Card)\
            .filter_by(id=card_id, user_id=user_id)\
            .options(joinedload(Card.reviews), joinedload(Card.confidence_level))\
            .first()

def get_cards_by_user_id(db: Session, user_id: int) -> List[Card]:
    """Retrieve all cards belonging to a specific user."""
    return db.query(Card).filter_by(user_id=user_id).all()

def create_card(db: Session, card_data: CardCreate, user_id: int) -> Optional[Card]:
    """Create a new card with the provided card data and associate it with a user and default confidence level."""
    try:
        default_confidence_level = get_default_confidence_level(db)
        if not default_confidence_level:
            raise ValueError("Default confidence level not found. Please ensure a default is set.")

        card_data.confidence_level_id = default_confidence_level.id
        new_card = Card(**card_data.dict(),user_id=user_id)
        db.add(new_card)
        db.commit()
        return new_card
    except Exception as e:
        db.rollback()
        print(f"Failed to create card due to a database error: {str(e)}")
        raise ValueError("Failed to create card due to a database error.")


def create_review_schedule_for_card(db: Session, card_id: int, review_data: ReviewScheduleCreate) -> Optional[ReviewSchedule]:
    """Create a new review schedule for a card."""
    review_schedule = ReviewSchedule(**review_data.dict(), card_id=card_id)
    db.add(review_schedule)
    db.commit()
    return review_schedule

def update_card(db: Session, card_id: int, user_id: int, card_data: CardUpdate) -> Optional[Card]:
    """Update an existing card with new data."""
    try:
        card_to_update = get_card_by_id(db, card_id, user_id)
        if not card_to_update:
            raise ValueError(f"No card found with ID {card_id} for user {user_id}")

        for attribute, value in card_data.dict(exclude_unset=True).items():
            setattr(card_to_update, attribute, value)
        db.commit()
        return card_to_update
    except Exception as e:
        db.rollback()
        print(f"Failed to update card: {e}")
        raise

def update_review_schedule_for_card(db: Session, review_id: int, review_data: ReviewScheduleUpdate) -> Optional[ReviewSchedule]:
    """Update an existing review schedule."""
    review_schedule = db.query(ReviewSchedule).filter_by(id=review_id).first()
    if review_schedule:
        for key, value in review_data.dict(exclude_unset=True).items():
            setattr(review_schedule, key, value)
        db.commit()
    return review_schedule

def update_card_confidence_level(db: Session, card_id: int, confidence_level_id: int) -> Optional[Card]:
    """Update a card's associated confidence level."""
    card = db.query(Card).filter_by(id=card_id).first()
    if card:
        card.confidence_level_id = confidence_level_id
        db.commit()
    return card

def delete_card(db: Session, card_id: int, user_id: int) -> bool:
    """Delete a card by its ID and user ID."""
    try:
        card_to_delete = get_card_by_id(db, card_id, user_id)
        if not card_to_delete:
            raise ValueError(f"No card found with ID {card_id} for user {user_id}")

        db.delete(card_to_delete)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Failed to delete card: {e}")
        raise
