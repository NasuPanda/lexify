import os
from sqlalchemy import create_engine, text
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime
from enum import Enum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9999"],  # Allows requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect db using DATABASE_URL from the environment variable
database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)

# Mock database for demonstration purposes
users_db = {"user@example.com": {"username": "user@example.com", "password": "secret"}}
cards_db = []
reviews_db = []

# Check the connection to the database by executing a simple SQL query
@app.get("/test-db")
async def test_db():
    try:
        # Execute a simple SQL query to fetch the current date
        with engine.connect() as connection:
            result = connection.execute(text("SELECT NOW()"))
            current_time = result.fetchone()
        return {"message": "Database connection successful", "current_time": str(current_time)}
    except Exception as e:
        return {"error": str(e)}

# Pydantic models for data validation
class ConfidenceLevel(Enum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

class User(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None

class Card(BaseModel):
    id: int
    user_id: int
    front_text: str
    back_text: str
    example_sentence: Optional[str] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Review(BaseModel):
    card_id: int
    user_id: int
    review_date: datetime
    confidence_level: ConfidenceLevel
    last_reviewed: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication routes
@app.post("/auth/register")
async def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    users_db[user.username] = user.dict()
    return {"message": "User registered successfully"}

@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = users_db.get(form_data.username)
    if not user_dict or user_dict['password'] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": user_dict["username"], "token_type": "bearer"}

# Card management routes
@app.post("/cards/")
async def create_card(card: Card):
    card.id = len(cards_db) + 1  # Simple ID assignment
    cards_db.append(card.dict())
    return card

@app.get("/cards/{card_id}", response_model=Card)
async def get_card(card_id: int):
    card = next((c for c in cards_db if c['id'] == card_id), None)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@app.put("/cards/{card_id}")
async def update_card(card_id: int, card: Card):
    index = next((i for i, c in enumerate(cards_db) if c['id'] == card_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Card not found")
    cards_db[index] = card.dict()
    return card

@app.delete("/cards/{card_id}")
async def delete_card(card_id: int):
    index = next((i for i, c in enumerate(cards_db) if c['id'] == card_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Card not found")
    del cards_db[index]
    return {"message": "Card deleted"}

# Review scheduling routes
@app.post("/reviews/")
async def create_review(review: Review):
    reviews_db.append(review.dict())
    return review

# File upload routes
@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    return {"filename": file.filename, "url": f"http://example.com/{file.filename}"}

@app.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    return {"filename": file.filename, "url": f"http://example.com/{file.filename}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
