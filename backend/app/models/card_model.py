from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    term = Column(String, index=True)
    definition = Column(String)
    example = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
