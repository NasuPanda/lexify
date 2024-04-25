from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class ConfidenceLevel(Base):
    __tablename__ = "confidence_levels"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    interval_days = Column(Integer, nullable=False)

    user = relationship("User", back_populates="confidence_levels")

class ReviewSchedule(Base):
    __tablename__ = "review_schedules"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    confidence_level_id = Column(Integer, ForeignKey("confidence_levels.id"), nullable=False)
    review_date = Column(DateTime, nullable=False)
    last_reviewed = Column(DateTime, nullable=True)

    card = relationship("Card", back_populates="reviews")
    confidence_level = relationship("ConfidenceLevel", back_populates="reviews")
