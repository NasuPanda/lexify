from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
from schemas.card import CardCreate
from services.card_service import create_card
from app.dependencies import get_current_user, get_db

router = APIRouter()

@router.post("/cards")
async def create_new_card(
        card_data: CardCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    card = create_card(card_data, current_user.id)
    if not card:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating card")
    return {"message": "Card created successfully", "card_id": card.id}
