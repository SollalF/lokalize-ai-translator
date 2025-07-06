from fastapi import APIRouter

from app.api.v1.endpoints.glossary_processor import router as glossary_processor_router
from app.api.v1.endpoints.lokalise import router as lokalise_router
from app.api.v1.endpoints.translation import router as translation_router

api_router = APIRouter()

# Include Lokalise endpoints (mirroring Lokalise API structure)
api_router.include_router(lokalise_router, prefix="/lokalise", tags=["lokalise"])

# Include Translation endpoints
api_router.include_router(
    translation_router, prefix="/translation", tags=["translation"]
)

# Include Glossary Processor endpoints
api_router.include_router(
    glossary_processor_router, prefix="/glossary", tags=["glossary-processor"]
)
