from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

from app.models.user_model import User

class ReviewSchedule(Base):
    __tablename__ = "review_schedules"

    id = Column(Integer, primary_key=True, index=True)
    review_date = Column(DateTime, nullable=False)
    last_reviewed = Column(DateTime, nullable=True)

    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    card = relationship("Card", back_populates="reviews")
