from sqlalchemy import text
from fastapi import FastAPI, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

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


@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    return {"filename": file.filename, "url": f"http://example.com/{file.filename}"}

@app.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    return {"filename": file.filename, "url": f"http://example.com/{file.filename}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
