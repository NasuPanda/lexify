from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.review_model import ReviewSchedule
from app.models.card_model import Card
from app.services.card_service import get_card_by_id
from app.services.confidence_level_service import get_confidence_level_by_id
from app.schemas.review import ReviewScheduleCreate, ReviewScheduleUpdate

def __get_confidence_level_from_review_schedule(db: Session, review: ReviewSchedule):
    # Get card from review
    card = get_card_by_id(db=db, card_id=review.card_id, user_id=review.user_id)
    if not card:
        raise ValueError(f"Card with ID {review.card_id} not found")
    # Get confidence level from the card
    confidence_level = get_confidence_level_by_id(db=db, confidence_id=card.confidence_level_id)
    if not confidence_level:
        raise ValueError(f"Confidence level with ID {card.confidence_level_id} not found")
    return confidence_level

def get_review_schedule_by_id(db: Session, review_id: int) -> Optional[ReviewSchedule]:
    """Retrieve a single review schedule by its ID."""
    return db.query(ReviewSchedule).filter_by(id=review_id).first()

def get_review_schedules_by_user_id(db: Session, user_id: int) -> List[ReviewSchedule]:
    """Retrieve all review schedules belonging to a specific user through their cards."""
    return db.query(ReviewSchedule).filter_by(user_id=user_id).all()

def get_review_schedules_for_review_session(db: Session, user_id: int, current_time: datetime = None) -> List[ReviewSchedule]:
    """
    Retrieves review schedules for a user that are due for review, meaning their review_date is past the current date and time.

    Args:
    db (Session): The database session.
    user_id (int): The ID of the user whose review schedules are to be retrieved.
    current_time (datetime, optional): The current datetime to compare against the review dates. Defaults to None, which means it uses the current system time.

    Returns:
    List[ReviewSchedule]: A list of ReviewSchedule instances that are due for review.
    """
    if current_time is None:
        current_time = datetime.now()

    print(f"Current datetime is: {current_time}")

    return db.query(ReviewSchedule) \
            .filter(ReviewSchedule.user_id == user_id,
                    # review_date is past the current datetime
                    ReviewSchedule.review_date <= current_time) \
            .all()

def create_review_schedule(db: Session, review_data: ReviewScheduleCreate) -> Optional[ReviewSchedule]:
    try:
        new_review_schedule = ReviewSchedule(**review_data.dict())
        db.add(new_review_schedule)
        db.commit()
        return new_review_schedule
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Failed to create review schedule: {e}")
        raise ValueError("Database transaction failed, unable to create review schedule.")

def update_review_schedule(db: Session, review_id: int, review_data: ReviewScheduleUpdate) -> Optional[ReviewSchedule]:
    try:
        review_schedule_to_update = get_review_schedule_by_id(db, review_id)
        if not review_schedule_to_update:
            raise ValueError(f"Review schedule with ID {review_id} not found")

        for attribute, value in review_data.dict(exclude_unset=True).items():
            setattr(review_schedule_to_update, attribute, value)
        db.commit()
        return review_schedule_to_update
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Failed to update review schedule: {e}")
        raise ValueError("Database transaction failed, unable to update review schedule.")

def update_review_schedule_post_review(db: Session, review_schedules: List[ReviewSchedule]):
    """
    Update review schedules and associated card data after a review session.

    Args:
    db (Session): The database session.
    review_schedules (List[ReviewSchedule]): A list of ReviewSchedules to be updated based on the review results.

    Returns:
    None: Updates the database in-place.
    """
    for review in review_schedules:
        confidence_level = __get_confidence_level_from_review_schedule(db=db, review=review)

        try:
            current_review_date = review.review_date
            review.review_date = current_review_date + timedelta(days=confidence_level.interval_days)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Failed to update review schedule: {e}")
            raise ValueError("Database transaction failed, unable to update review schedule.")

def delete_review_schedule(db: Session, review_id: int) -> bool:
    try:
        review_schedule_to_delete = get_review_schedule_by_id(db, review_id)
        if not review_schedule_to_delete:
            raise ValueError(f"Review schedule with ID {review_id} not found")

        db.delete(review_schedule_to_delete)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Failed to delete review schedule: {e}")
        raise ValueError("Database transaction failed, unable to delete review schedule.")
