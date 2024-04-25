from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ConfidenceLevel(BaseModel):
    id: Optional[int] = Field(None, description="The unique identifier for the confidence level")
    description: str = Field(..., description="Description of the confidence level")
    interval_days: int = Field(..., description="Number of days until the next review for this confidence level", ge=1, le=365)

class ConfidenceLevelCreate(BaseModel):
    description: str = Field(..., description="Description of the confidence level")
    interval_days: int = Field(..., description="Number of days until the next review for this confidence level", ge=1, le=365)

class ConfidenceLevelUpdate(BaseModel):
    description: Optional[str] = Field(None, description="Description of the confidence level")
    interval_days: Optional[int] = Field(None, description="Number of days until the next review for this confidence level", ge=1, le=365)

class ReviewSchedule(BaseModel):
    id: Optional[int] = Field(None, description="The unique identifier for the review schedule")
    card_id: int = Field(..., description="Identifier of the card being reviewed")
    confidence_level_id: int = Field(..., description="The confidence level associated with this review")
    review_date: datetime = Field(..., description="The date of the review")
    last_reviewed: Optional[datetime] = Field(None, description="The date when the card was last reviewed")

class ReviewScheduleCreate(BaseModel):
    card_id: int = Field(..., description="Identifier of the card being reviewed")
    confidence_level_id: int = Field(..., description="The confidence level associated with this review")
    review_date: datetime = Field(..., description="The date of the review")

class ReviewScheduleUpdate(BaseModel):
    confidence_level_id: Optional[int] = Field(None, description="The confidence level associated with this review")
    review_date: Optional[datetime] = Field(None, description="The date of the review")
    last_reviewed: Optional[datetime] = Field(None, description="The date when the card was last reviewed")
