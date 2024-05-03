from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ReviewScheduleBase(BaseModel):
    review_date: datetime = Field(..., description="The scheduled date for the review")
    last_reviewed: Optional[datetime] = Field(None, description="The date when the card was last reviewed")

class ReviewScheduleCreate(ReviewScheduleBase):
    card_id: int = Field(..., description="Identifier of the card being reviewed")

class ReviewScheduleRead(ReviewScheduleBase):
    id: int = Field(..., description="The unique identifier for the review schedule")
    card_id: int = Field(..., description="Identifier of the card being reviewed")

class ReviewScheduleUpdate(ReviewScheduleBase):
    pass
