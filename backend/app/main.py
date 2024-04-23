from sqlalchemy import text
from fastapi import FastAPI, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

from app.core.database import engine
from app.api.routers import cards, auth

app = FastAPI()
# Mount the routers
app.include_router(cards.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9999"],  # Allows requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConfidenceLevel(Enum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

class Review(BaseModel):
    card_id: int
    user_id: int
    review_date: datetime
    confidence_level: ConfidenceLevel
    last_reviewed: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Check the connection to the database by executing a simple SQL query (for testing)
# TODO Remove this function
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

@app.post("/reviews/")
async def create_review(review: Review):
    reviews_db = []
    reviews_db.append(review.dict())
    return review

@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    return {"filename": file.filename, "url": f"http://example.com/{file.filename}"}

@app.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    return {"filename": file.filename, "url": f"http://example.com/{file.filename}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
