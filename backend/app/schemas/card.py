from datetime import datetime
from pydantic import BaseModel, Field, Optional

"""
NOTE:
- Don't forget to modify: examples -> example_sentence
- Be attentive to potential lacks of attributes/module imports

PUT /cards/{card_id}: Updates a specific card by its ID.
DELETE /cards/{card_id}: Deletes a specific card by its ID.
GET /cards: Lists all cards for the logged-in user.
"""

class CardResponse(BaseModel):
    """GET /cards/{card_id}"""
    id: int
    user_id: int
    term: str
    definition: str
    example_sentence: Optional[str]
    image_url: Optional[str]
    audio_url: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

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
    term: str = Field(None, example="Updated term")
    definition: str = Field(None, example="Updated definition")
    example_sentence: Optional[str] = Field(None, example="Pumpkin and penguins!")
    image_url: Optional[str] = Field(None, example="http://example.com/updated_image.png")
    audio_url: Optional[str] = Field(None, example="http://example.com/updated_audio.mp3")
