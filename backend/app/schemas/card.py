from datetime import datetime
from pydantic import BaseModel, Field, AnyUrl, validator
from typing import Optional

class CardResponse(BaseModel):
    """GET /cards/{card_id}"""
    id: int
    user_id: int
    term: str
    definition: str
    example_sentence: Optional[str]
    image_url: Optional[AnyUrl]
    audio_url: Optional[AnyUrl]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CardCreate(BaseModel):
    term: str = Field(..., example="Lexicon")
    definition: str = Field(..., example="The vocabulary of a person, language, or branch of knowledge")
    example_sentence: Optional[str] = Field(None, example="Her lexicon was vast and filled with unusual words.")
    image_url: Optional[AnyUrl] = Field(None, example="http://example.com/image.png")
    audio_url: Optional[AnyUrl] = Field(None, example="http://example.com/audio.mp3")

    # Validators to ensure 'term' and 'definition' are not empty
    @validator('term', 'definition')
    def check_not_empty(cls, v):
        if not v.strip():  # This checks for empty strings or strings with only whitespace
            raise ValueError("This field cannot be empty or just whitespace.")
        return v

class CardUpdate(BaseModel):
    term: Optional[str] = Field(None, example="Updated term")
    definition: Optional[str] = Field(None, example="Updated definition")
    example_sentence: Optional[str] = Field(None, example="Pumpkin and penguins!")
    image_url: Optional[AnyUrl] = Field(None, example="http://example.com/updated_image.png")
    audio_url: Optional[AnyUrl] = Field(None, example="http://example.com/updated_audio.mp3")
