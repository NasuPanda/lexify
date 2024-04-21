from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ConfidenceLevel(Enum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

class Review(BaseModel):
    card_id: int
    user_id: int
    review_date: datetime
    confidence_level: ConfidenceLevel
    last_reviewed: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
