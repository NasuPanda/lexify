import pytest
from pydantic import ValidationError
from app.schemas.card import CardCreate

def test_create_card_with_empty_term():
    """Card creation with empty term"""
    with pytest.raises(ValueError) as e:
        _card_data = CardCreate(
            term="",
            definition="Definition",
            example_sentence="Don't forget to be an example!",
            image_url="http://example.com/image.png",
            audio_url="http://example.com/audio.mp3",
        )
    assert "This field cannot be empty or just whitespace." in str(e.value)

def test_create_card_with_empty_definition():
    """Card creation with empty definition"""
    with pytest.raises(ValueError) as e:
        _card_data = CardCreate(
            term="Lexicon",
            definition="",
            example_sentence="Don't forget to be an example!",
            image_url="http://example.com/image.png",
            audio_url="http://example.com/audio.mp3",
        )
    assert "This field cannot be empty or just whitespace." in str(e.value)

def test_create_card_with_invalid_url():
    """Card creation with invalid url"""
    with pytest.raises(ValidationError) as e:
        _card_data = CardCreate(
            term="Example",
            definition="A thing characteristic of its kind or illustrating a general rule.",
            example_sentence="Don't forget to be an example!",
            image_url="invalid_url",
            audio_url="invalid_url",
        )
    assert "invalid or missing url scheme" in str(e.value).lower()
