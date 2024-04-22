from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.card import CardCreate, CardResponse, CardUpdate
from app.services.card_service import create_card, get_card_by_id, update_card
from app.dependencies import get_current_user, get_db

router = APIRouter()

@router.get("/cards/{card_id}", response_model=CardResponse)
async def retrieve_card(card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    card = get_card_by_id(db, card_id, current_user.id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return card

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

@router.put("/cards/{card_id}", response_model=CardResponse)
async def update_card_details(
        card_id: int,
        card_data: CardUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    card = update_card(db, card_id, current_user.id, card_data)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return card
