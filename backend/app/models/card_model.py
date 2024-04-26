from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, index=True)
    definition = Column(String)
    example_sentence = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    confidence_level_id = Column(Integer, ForeignKey("confidence_levels.id"), nullable=False)  # Added line

    user = relationship("User", back_populates="cards")
    reviews = relationship("ReviewSchedule", back_populates="card")
    confidence_level = relationship("ConfidenceLevel")
