from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

# Confidence Level
class ConfidenceLevelBase(BaseModel):
    description: str = Field(..., description="Description of the confidence level")
    interval_days: int = Field(..., description="Number of days until the next review for this confidence level", ge=1, le=365)
    is_default: bool = Field(False, description="Indicates if this is the default confidence level")

class ConfidenceLevelRead(ConfidenceLevelBase):
    id: Optional[int] = Field(None, description="The unique identifier for the confidence level")

class ConfidenceLevelCreate(ConfidenceLevelBase):
    pass

class ConfidenceLevelUpdate(ConfidenceLevelBase):
    pass
