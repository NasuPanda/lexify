from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.card import CardCreate, CardResponse, CardUpdate
from app.services.card_service import create_card, delete_card, get_card_by_id, get_cards_by_user_id, update_card
from app.dependencies import get_current_user, get_db

router = APIRouter()

@router.get("/cards/{card_id}", response_model=CardResponse)
async def retrieve_card(card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    card = get_card_by_id(db, card_id, current_user.id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return card

@router.get("/cards", response_model=CardResponse)
async def list_cards(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_cards_by_user_id(db=db, user_id=current_user.user_id)

@router.post("/cards")
async def create_new_card(
        card_data: CardCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    card = create_card(db, card_data, current_user.id)
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

@router.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card_endpoint(
        card_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    is_success = delete_card(db=db, card_id=card_id, user_id=current_user.id)
    if not is_success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found or not accessible")
    return {"message": "Card deleted successfully"}
