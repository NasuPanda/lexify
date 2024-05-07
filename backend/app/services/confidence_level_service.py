from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.confidence_level_model import ConfidenceLevel
from app.schemas.confidence_level import ConfidenceLevelCreate, ConfidenceLevelUpdate

def get_confidence_level_by_id(db: Session, confidence_id: int) -> Optional[ConfidenceLevel]:
    """Retrieve a single confidence level by its ID."""
    return db.query(ConfidenceLevel).filter_by(id=confidence_id).first()

def get_confidence_levels_by_user_id(db: Session, user_id: int) -> List[ConfidenceLevel]:
    """Retrieve all confidence levels belonging to a specific user."""
    return db.query(ConfidenceLevel).filter_by(user_id=user_id).all()

def get_default_confidence_level(db: Session) -> Optional[ConfidenceLevel]:
    """Retrieve the default confidence level."""
    return db.query(ConfidenceLevel).filter_by(is_default=True).first()

def create_confidence_level(db: Session, confidence_data: ConfidenceLevelCreate, user_id: int) -> Optional[ConfidenceLevel]:
    try:
        new_confidence_level = ConfidenceLevel(**confidence_data.dict(), user_id=user_id)
        db.add(new_confidence_level)
        db.commit()
        db.refresh(new_confidence_level)# Refresh to update instance state from DB
        return new_confidence_level
    except IntegrityError as e:
        db.rollback()
        print(f"Integrity error occurred: {e}")
        raise ValueError("Failed to create confidence level due to integrity constraints.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error occurred: {e}")
        raise

def update_confidence_level(db: Session, confidence_id: int, confidence_data: ConfidenceLevelUpdate) -> Optional[ConfidenceLevel]:
    try:
        confidence_level_to_update = get_confidence_level_by_id(db, confidence_id)
        if not confidence_level_to_update:
            raise ValueError(f"Confidence level with ID {confidence_id} not found")

        for attribute, value in confidence_data.dict(exclude_unset=True).items():
            setattr(confidence_level_to_update, attribute, value)
        db.commit()
        return confidence_level_to_update
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Failed to update confidence level: {e}")
        raise

def delete_confidence_level(db: Session, confidence_id: int) -> bool:
    try:
        confidence_level_to_delete = get_confidence_level_by_id(db, confidence_id)
        if not confidence_level_to_delete:
            raise ValueError(f"Confidence level with ID {confidence_id} not found")

        db.delete(confidence_level_to_delete)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Failed to delete confidence level: {e}")
        raise
