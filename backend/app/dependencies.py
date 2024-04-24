from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user_model import User


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db)) -> User:
    # TODO This should be dynamically determined, e.g., from a token
    user_id = 1
    return db.query(User).filter(User.id == user_id).first()
