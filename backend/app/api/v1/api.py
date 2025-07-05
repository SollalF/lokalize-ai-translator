from fastapi import APIRouter

from app.api.v1.endpoints import lokalise

api_router = APIRouter()

# Import and include other routers here
# Example:
# from .endpoints import items, users
# api_router.include_router(items.router, prefix="/items", tags=["items"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])

# Include Lokalise endpoints (mirroring Lokalise API structure)
api_router.include_router(lokalise.router)

# # Include Translation endpoints
# api_router.include_router(
#     translation.router, prefix="/translation", tags=["translation"]
# )

# # Include Glossary Processor endpoints
# api_router.include_router(
#     glossary_processor.router, prefix="/glossary", tags=["glossary-processor"]
# )
