from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import * # Import models to ensure SQLAlchemy is aware of them
from app.core.database import engine
from app.api.routers import cards, auth, reviews

app = FastAPI()
# Mount the routers
app.include_router(cards.router)
app.include_router(auth.router)
app.include_router(reviews.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9999"],  # Allows requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
