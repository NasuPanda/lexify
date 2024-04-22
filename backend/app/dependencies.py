from typing import Generator

from app.core.database import SessionLocal
from app.models.user_model import User
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session


# TODO This function is problematic. When it's commented out, it raises the error: NameError: name 'Any' is not defined.
# def get_current_user(db: Session = Depends(SessionLocal)) -> User:
#     # TODO # This should be dynamically determined, e.g., from a token
#     user_id = 1
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

def get_current_user() -> User:
    return

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
