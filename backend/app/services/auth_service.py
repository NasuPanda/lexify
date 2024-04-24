from typing import Optional
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user import UserRegister, UserLogin
from app.core.security import hash_password, verify_password

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Retrieve a single User by its name."""
    return db.query(User).filter_by(username=username).first()

def create_user(db: Session, user_data: UserRegister) -> Optional[User]:
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise ValueError("Username already exists")

    hashed_password = hash_password(user_data.password)
    user = User(username=user_data.username, password_hash=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user) # Refresh to retrieve and return the new user /w ID

    return user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)

    if user and verify_password(password, user.password_hash):
        return user

    return None
