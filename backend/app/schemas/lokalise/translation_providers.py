from pydantic import BaseModel, Field


class TranslationProviderPair(BaseModel):
    """Language pair and pricing information for a translation provider tier."""

    tier_id: int = Field(..., description="Translation tier")
    from_lang_iso: str = Field(..., description="Source language identifier")
    from_lang_name: str = Field(..., description="Source language name")
    to_lang_iso: str = Field(..., description="Target language identifier")
    to_lang_name: str = Field(..., description="Target language name")
    price_per_word: float = Field(..., description="Price per word in USD")


class TranslationProviderTier(BaseModel):
    """Available translation tier for a provider."""

    tier_id: int = Field(..., description="An identifier of the tier")
    name: str = Field(..., description="Name of the tier")
    pairs: dict[str, TranslationProviderPair] = Field(
        ..., description="List of language pairs and prices"
    )


class TranslationProvider(BaseModel):
    """Translation provider object schema for Lokalise API."""

    provider_id: int = Field(..., description="A unique identifier of the provider")
    name: str = Field(..., description="Name of the provider")
    slug: str = Field(..., description="Slug of the provider")
    price_pair_min: float = Field(
        ...,
        description="Minimum total price per language pair. It's '0.00' if there is no minimum requirement",
    )
    website_url: str = Field(..., description="Provider website")
    description: str = Field(..., description="Provider description")
    tiers: dict[str, TranslationProviderTier] = Field(
        ..., description="Available translation tiers"
    )


class TranslationProvidersResponse(BaseModel):
    """Response schema for listing translation providers."""

    providers: list[TranslationProvider] = Field(
        ..., description="List of translation providers"
    )


class TranslationProviderResponse(BaseModel):
    """Response schema for retrieving a single translation provider."""

    provider: TranslationProvider = Field(
        ..., description="The translation provider object"
    )
