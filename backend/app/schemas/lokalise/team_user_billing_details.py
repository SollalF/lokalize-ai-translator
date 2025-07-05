from pydantic import BaseModel, Field


class TeamUserBillingDetails(BaseModel):
    """Team user billing details object schema for Lokalise API."""

    billing_email: str = Field(
        ..., description="Email for invoices and translation orders"
    )
    country_code: str = Field(
        ..., description="Country code as described in ISO 3166 (alpha-2 code)"
    )
    zip: str = Field(..., description="Valid postal code for specified country")
    state_code: str | None = Field(None, description="Required if country code is US")
    address1: str = Field(..., description="Address line 1")
    address2: str | None = Field(None, description="Address line 2")
    city: str = Field(..., description="City")
    phone: str = Field(..., description="Phone")
    company: str = Field(..., description="Company name")
    vatnumber: str = Field(..., description="VAT number")


class TeamUserBillingDetailsCreateRequest(BaseModel):
    """Request schema for creating team user billing details."""

    billing_email: str = Field(
        ..., description="Email for invoices and translation orders"
    )
    country_code: str = Field(
        ..., description="Country code as described in ISO 3166 (alpha-2 code)"
    )
    zip: str = Field(..., description="Valid postal code for specified country")
    state_code: str | None = Field(None, description="Required if country code is US")
    address1: str = Field(..., description="Address line 1")
    address2: str | None = Field(None, description="Address line 2")
    city: str = Field(..., description="City")
    phone: str = Field(..., description="Phone")
    company: str = Field(..., description="Company name")
    vatnumber: str = Field(..., description="VAT number")


class TeamUserBillingDetailsResponse(BaseModel):
    """Response schema for team user billing details operations."""

    billing_details: TeamUserBillingDetails
