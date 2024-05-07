from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.confidence_level_model import ConfidenceLevel
from app.schemas.confidence_level import ConfidenceLevelCreate, ConfidenceLevelUpdate, ConfidenceLevelRead
from app.services.confidence_level_service import create_confidence_level, get_confidence_level_by_id, get_confidence_levels_by_user_id, update_confidence_level, delete_confidence_level
from app.dependencies import get_current_user, get_db

router = APIRouter()

@router.post("/confidence-levels", response_model=ConfidenceLevelRead, status_code=status.HTTP_201_CREATED)
async def create_confidence_level_endpoint(
        confidence_data: ConfidenceLevelCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    new_confidence_level = create_confidence_level(db, confidence_data, current_user.id)
    if not new_confidence_level:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating confidence level")
    return new_confidence_level

@router.get("/confidence-levels/{confidence_id}", response_model=ConfidenceLevelRead)
async def get_confidence_level_endpoint(
        confidence_id: int,
        db: Session = Depends(get_db),
    ):
    confidence_level = get_confidence_level_by_id(db, confidence_id)
    if not confidence_level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Confidence level not found")
    return confidence_level

@router.get("/confidence-levels", response_model=List[ConfidenceLevelRead])
async def get_confidence_levels_endpoint(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    confidence_levels = get_confidence_levels_by_user_id(db, current_user.id)
    if not confidence_levels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Confidence levels not found")
    return confidence_levels

@router.put("/confidence-levels/{confidence_id}", response_model=ConfidenceLevelRead)
async def update_confidence_level_endpoint(
        confidence_id: int,
        confidence_data: ConfidenceLevelUpdate,
        db: Session = Depends(get_db),
    ):
    updated_confidence_level = update_confidence_level(db, confidence_id, confidence_data)
    if not updated_confidence_level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Confidence level not found")
    return updated_confidence_level

@router.delete("/confidence-levels/{confidence_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_confidence_level_endpoint(
        confidence_id: int,
        db: Session = Depends(get_db),
    ):
    is_success = delete_confidence_level(db, confidence_id)
    if not is_success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Confidence level not found or not accessible")
    return {"message": "Confidence level deleted successfully"}
