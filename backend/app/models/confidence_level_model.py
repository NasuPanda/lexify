from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class ConfidenceLevel(Base):
    __tablename__ = "confidence_levels"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    interval_days = Column(Integer, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="confidence_levels")
