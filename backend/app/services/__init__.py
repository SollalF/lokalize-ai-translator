from app.services.gemini_service import gemini_service
from app.services.glossary_aware_translation import glossary_aware_translation_service
from app.services.glossary_processor import glossary_processor
from app.services.translation_evaluation_service import translation_evaluation_service

# Export the singleton instances
__all__ = [
    "gemini_service",
    "glossary_aware_translation_service",
    "glossary_processor",
    "translation_evaluation_service",
]
