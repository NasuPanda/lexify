from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.review_model import ReviewSchedule
from app.schemas.review import ReviewScheduleCreate, ReviewScheduleRead, ReviewScheduleUpdate
from app.services.review_service import (
    get_review_schedule_by_id,
    get_review_schedules_by_user_id,
    get_review_schedules_for_review_session,
    create_review_schedule,
    update_review_schedule,
    update_review_schedule_post_review,
    delete_review_schedule,
)
from app.dependencies import get_current_user, get_db

router = APIRouter()

@router.get("/review-schedules", response_model=List[ReviewScheduleRead], status_code=status.HTTP_200_OK)
async def list_all_review_schedules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    """
    Retrieves all review schedules associated with the current logged-in user.
    This endpoint ensures users can view all their scheduled reviews.

    Args:
    db (Session): The database session to facilitate database access.
    current_user (User): The user object of the currently authenticated user.

    Returns:
    List[ReviewScheduleRead]: A list of review schedules for the current user.

    Raises:
    HTTPException: 404 - If no review schedules are found for the current user.
    """
    review_schedules = get_review_schedules_by_user_id(db=db, user_id=current_user.id)
    if not review_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review Schedules not found")
    return review_schedules

@router.get("/review-schedules/session", response_model=List[ReviewScheduleRead], status_code=status.HTTP_200_OK)
async def get_due_review_schedules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    """
    Fetches review schedules that are due as of the current date for the logged-in user, intended to facilitate a review session.

    Args:
    db (Session): The database session used for database queries.
    current_user (User): The currently authenticated user whose due review schedules are to be retrieved.

    Returns:
    List[ReviewScheduleRead]: A list of due review schedules.

    Raises:
    HTTPException: 404 - If no due review schedules are found, indicating no reviews are pending or due.
    """
    review_schedules = get_review_schedules_for_review_session(db=db, user_id=current_user.id)
    if not review_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review Schedules not found")
    return review_schedules

@router.post("/review-schedules/complete", status_code=status.HTTP_204_NO_CONTENT)
async def complete_review_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    """
    Marks review sessions as completed for the current user by updating their review schedules based on the session's outcomes.
    This is typically called when a user finishes reviewing their scheduled items.

    Args:
    db (Session): The database session to perform data updates.
    current_user (User): The user who is completing the review session.

    Returns:
    dict: A message confirming that the review schedules have been successfully updated.

    Raises:
    HTTPException: 404 - If no review schedules eligible for updating are found, possibly indicating an error or miscommunication in schedule management.
    """
    review_schedules = get_review_schedules_for_review_session(db=db, user_id=current_user.id)
    if not review_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review Schedules not found")

    update_review_schedule_post_review(db, review_schedules)

    return {"message": "Review schedules updated successfully"}
