from app.models.user_model import User

def get_current_user(id: int) -> User:
    # TODO: Implement
    return User(
        id=1,
        username="John Green",
        password="pumpkin_and_penguins",
        email="johngreen@example.com",
    )

def get_db(db_name: str):
    # TODO: Implement
    return
