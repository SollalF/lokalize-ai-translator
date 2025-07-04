from pydantic import BaseModel, Field


class ServiceTokenCreateRequest(BaseModel):
    """Request schema for creating a service JWT token."""

    service: str = Field(..., description="Service to create the token for")


class ServiceTokenResponse(BaseModel):
    """Response schema for service token creation."""

    jwt: str = Field(..., description="JWT token for the specified service")
