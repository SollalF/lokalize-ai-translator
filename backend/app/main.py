import datetime
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import get_settings, validate_api_keys

# Load environment variables
_ = load_dotenv()

# Get settings
settings = get_settings()

# Validate API keys
if not validate_api_keys(settings):
    print("\n❌ Application startup failed due to missing API keys.")
    sys.exit(1)

app = FastAPI(
    title="Lokalize AI Translator API",
    description="Backend API for the Lokalise AI Translator application",
    version="0.1.0",
)

# Get CORS origins from environment variable
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:80,http://localhost"
).split(",")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to Lokalize AI Translator API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/test-connection")
async def test_connection():
    return {
        "message": "Connection successful!",
        "timestamp": datetime.datetime.now().isoformat(),
    }
