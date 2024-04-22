from fastapi import APIRouter, HTTPException, status
from app.models.user_model import User
from app.schemas.user import UserRegister, UserLogin
from app.services.auth_service import create_user, authenticate_user

router = APIRouter()

@router.post("/auth/register")
async def register(user_data: UserRegister):
    user = create_user(user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error registering user")
    return {"message": "User created successfully", "user_id": user.id}

@router.post("/auth/login")
async def login(user_data: UserLogin):
    user = authenticate_user(user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}
