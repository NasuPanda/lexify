from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class CardResponse(BaseModel):
    """GET /cards/{card_id}"""
    id: int
    user_id: int
    term: str
    definition: str
    example_sentence: Optional[str]
    image_url: Optional[str]
    audio_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CardCreate(BaseModel):
    """POST /cards"""
    term: str = Field(..., example="Lexicon")
    definition: str = Field(..., example="The vocabulary of a person, language, or branch of knowledge")
    example_sentence: Optional[str] = Field(None, example="Her lexicon was vast and filled with unusual words.")
    image_url: Optional[str] = Field(None, example="http://example.com/image.png")
    audio_url: Optional[str] = Field(None, example="http://example.com/audio.mp3")

class CardUpdate(BaseModel):
    term: Optional[str] = Field(None, example="Updated term")
    definition: Optional[str] = Field(None, example="Updated definition")
    example_sentence: Optional[str] = Field(None, example="Pumpkin and penguins!")
    image_url: Optional[str] = Field(None, example="http://example.com/updated_image.png")
    audio_url: Optional[str] = Field(None, example="http://example.com/updated_audio.mp3")
