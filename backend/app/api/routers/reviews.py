from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.review_model import ReviewSchedule
from app.schemas.review import ReviewScheduleCreate, ReviewScheduleRead, ReviewScheduleUpdate
from app.services.review_service import (
    get_review_schedule_by_id,
    get_review_schedules_by_user_id,
    create_review_schedule,
    update_review_schedule,
    delete_review_schedule,
)
from app.dependencies import get_current_user, get_db

router = APIRouter()

@router.post("/review_schedules", response_model=ReviewScheduleRead, status_code=status.HTTP_201_CREATED)
async def create_review_schedule_endpoint(
        review_schedule_data: ReviewScheduleCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    pass
