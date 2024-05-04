from datetime import datetime
from pydantic import BaseModel, Field, AnyUrl, validator
from typing import Optional

from app.schemas.review import ReviewScheduleRead
from app.schemas.confidence_level import ConfidenceLevelRead

class CardResponse(BaseModel):
    """GET /cards/{card_id}"""
    id: int
    term: str
    definition: str
    example_sentence: Optional[str]
    image_url: Optional[AnyUrl]
    audio_url: Optional[AnyUrl]
    created_at: datetime
    updated_at: datetime

    user_id: int
    confidence_level_id: int

    # Ensure that attributes exactly match with card_model
    # review_schedule: Optional[ReviewScheduleRead] = None
    # confidence_level: Optional[ConfidenceLevelRead] = None

    class Config:
        orm_mode = True

class CardCreate(BaseModel):
    term: str = Field(..., example="Lexicon")
    definition: str = Field(..., example="The vocabulary of a person, language, or branch of knowledge")
    example_sentence: Optional[str] = Field(None, example="Her lexicon was vast and filled with unusual words.")
    image_url: Optional[AnyUrl] = Field(None, example="http://example.com/image.png")
    audio_url: Optional[AnyUrl] = Field(None, example="http://example.com/audio.mp3")
    confidence_level_id: Optional[int] = Field(None, description="The ID of the confidence level associated with this card")  # New field to link confidence level

    @validator('term', 'definition')
    def check_not_empty(cls, v):
        if not v.strip():
            raise ValueError("This field cannot be empty or just whitespace.")
        return v

class CardUpdate(BaseModel):
    term: Optional[str] = Field(None, example="Updated term")
    definition: Optional[str] = Field(None, example="Updated definition")
    example_sentence: Optional[str] = Field(None, example="Pumpkin and penguins!")
    image_url: Optional[AnyUrl] = Field(None, example="http://example.com/updated_image.png")
    audio_url: Optional[AnyUrl] = Field(None, example="http://example.com/updated_audio.mp3")
    confidence_level_id: Optional[int] = Field(None, description="Update the confidence level associated with the card")  # New field for updating confidence level
