from app.models.user_model import User
from app.schemas.user import UserRegister, UserLogin
from app.core.security import hash_password, verify_password

def create_user(user_data: UserRegister):
    hashed_password = hash_password(user_data.password)
    user = User(username=user_data.username, email=user_data.email, password=hashed_password)
    # TODO: Add database add and commit logic
    return user

def authenticate_user(user_data: UserLogin):
    user = User.query.filter_by(username=user_data.username).first()
    if user and verify_password(user_data.password, user.password):
        return user
    return None
