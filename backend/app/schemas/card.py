from pydantic import BaseModel, Field, Optional

class CardCreate(BaseModel):
    term: str = Field(..., example="Lexicon")
    definition: str = Field(..., example="The vocabulary of a person, language, or branch of knowledge")
    example_sentence: Optional[str] = Field(None, example="Her lexicon was vast and filled with unusual words.")
    image_url: Optional[str] = Field(None, example="http://example.com/image.png")
    audio_url: Optional[str] = Field(None, example="http://example.com/audio.mp3")
