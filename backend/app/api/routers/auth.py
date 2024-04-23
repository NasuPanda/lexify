from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user import UserRegister, UserLogin
from app.services.auth_service import create_user, authenticate_user
from app.dependencies import get_db

router = APIRouter()

@router.post("/auth/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)) -> User:
    user = create_user(db=db, user_data=user_data)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error registering user")

@router.post("/auth/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)) -> dict:
    user = authenticate_user(db=db, username=user_data.username, password=user_data.password)
    if user:
        return {"message": "Login successful", "user_id": user.id}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
