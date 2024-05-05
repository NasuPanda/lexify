from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.review_model import ReviewSchedule
from app.models.card_model import Card
from app.schemas.review import ReviewScheduleCreate, ReviewScheduleUpdate


def get_review_schedule_by_id(db: Session, review_id: int) -> Optional[ReviewSchedule]:
    """Retrieve a single review schedule by its ID."""
    return db.query(ReviewSchedule).filter(ReviewSchedule.id == review_id).first()

def get_review_schedules_by_user_id(db: Session, user_id: int) -> List[ReviewSchedule]:
    """Retrieve all review schedules belonging to a specific user through their cards."""
    return db.query(ReviewSchedule).filter(ReviewSchedule.user_id == user_id).all()

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
