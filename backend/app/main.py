from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    app.mongodb = app.mongodb_client.get_database("boardclimbingai")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
async def root():
    return {"message": "Welcome to BoardClimbingAI API"}

@app.get("/test_db")
async def test_db():
    try:
        # Attempt to fetch a document from a collection
        doc = await app.mongodb.users.find_one({})
        return {"message": "Database connection successful", "document": str(doc)}
    except Exception as e:
        return {"message": "Database connection failed", "error": str(e)}