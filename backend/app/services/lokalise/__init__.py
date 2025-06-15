from .glossary import LokaliseGlossaryService
from .keys import LokaliseKeysService
from .languages import LokaliseLanguagesService
from .projects import LokaliseProjectsService
from .system import LokaliseSystemService
from .translations import LokaliseTranslationsService

# Create singleton instances
lokalise_glossary_service = LokaliseGlossaryService()
lokalise_keys_service = LokaliseKeysService()
lokalise_languages_service = LokaliseLanguagesService()
lokalise_translations_service = LokaliseTranslationsService()
lokalise_projects_service = LokaliseProjectsService()
lokalise_system_service = LokaliseSystemService()


# For backward compatibility, create a combined service interface
class LokaliseService:
    """Combined service interface for all Lokalise operations."""

    def __init__(self):
        self.glossary = lokalise_glossary_service
        self.keys = lokalise_keys_service
        self.languages = lokalise_languages_service
        self.translations = lokalise_translations_service
        self.projects = lokalise_projects_service
        self.system = lokalise_system_service

    # Delegate methods for backward compatibility
    async def get_keys(self, *args, **kwargs):
        return await self.keys.get_keys(*args, **kwargs)

    async def create_keys(self, *args, **kwargs):
        return await self.keys.create_keys(*args, **kwargs)

    async def get_translations(self, *args, **kwargs):
        return await self.translations.get_translations(*args, **kwargs)

    async def get_translation(self, *args, **kwargs):
        return await self.translations.get_translation(*args, **kwargs)

    async def update_translation(self, *args, **kwargs):
        return await self.translations.update_translation(*args, **kwargs)

    # Glossary delegate methods
    async def get_glossary_terms(self, *args, **kwargs):
        return await self.glossary.get_glossary_terms(*args, **kwargs)

    async def get_glossary_term(self, *args, **kwargs):
        return await self.glossary.get_glossary_term(*args, **kwargs)

    async def create_glossary_terms(self, *args, **kwargs):
        return await self.glossary.create_glossary_terms(*args, **kwargs)

    async def update_glossary_terms(self, *args, **kwargs):
        return await self.glossary.update_glossary_terms(*args, **kwargs)

    async def delete_glossary_terms(self, *args, **kwargs):
        return await self.glossary.delete_glossary_terms(*args, **kwargs)


# Main service instance for backward compatibility
lokalise_service = LokaliseService()

__all__ = [
    "LokaliseGlossaryService",
    "LokaliseKeysService",
    "LokaliseLanguagesService",
    "LokaliseProjectsService",
    "LokaliseService",
    "LokaliseSystemService",
    "LokaliseTranslationsService",
    "lokalise_glossary_service",
    "lokalise_keys_service",
    "lokalise_languages_service",
    "lokalise_projects_service",
    "lokalise_service",
    "lokalise_system_service",
    "lokalise_translations_service",
]
