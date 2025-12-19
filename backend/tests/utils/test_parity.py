"""
Test suite to verify API parity between our service and Lokalise API.
This ensures our endpoints return exactly the same data as Lokalise.
"""

import asyncio
import json
import os
from typing import Any
from urllib.parse import urlencode

import httpx

# Try to load .env file if not already loaded
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Try to import the app, but handle missing environment gracefully
try:
    from fastapi.testclient import TestClient

    from app.core.config import get_settings
    from app.main import app

    # Test client for our FastAPI app
    client = TestClient(app)

    # Get settings for Lokalise API access
    settings = get_settings()

    # Check if we have the required token
    if not settings.LOKALISE_API_TOKEN:
        # Check if it's in environment directly
        env_token = os.getenv("LOKALISE_API_TOKEN")
        if env_token:
            # Environment variable exists but settings didn't pick it up
            raise ValueError(
                f"LOKALISE_API_TOKEN found in environment ({env_token[:10]}...) but not in settings. Check your config loading."
            )
        else:
            raise ValueError(
                "LOKALISE_API_TOKEN is not configured in environment or settings"
            )

except (ImportError, ValueError) as e:
    # If the app can't be imported due to missing environment variables,
    # we'll set up for error reporting
    client = None
    settings = None
    configuration_error = str(e)


class APIParityTester:
    """Test framework for comparing our API responses with Lokalise API responses."""

    def __init__(self):
        self.lokalise_base_url = "https://api.lokalise.com/api2"
        self.our_base_url = "http://testserver/api/v1"

        # Ensure API token is available
        if not settings or not settings.LOKALISE_API_TOKEN:
            raise ValueError("LOKALISE_API_TOKEN is required for API parity testing")

        self.headers = {
            "accept": "application/json",
            "X-Api-Token": settings.LOKALISE_API_TOKEN,
        }

    async def call_lokalise_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a direct call to Lokalise API."""
        url = f"{self.lokalise_base_url}/{endpoint.lstrip('/')}"

        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(
                url, headers=self.headers, params=params or {}, timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    def call_our_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a call to our FastAPI service."""
        if not client:
            raise ValueError("API client is not available - check configuration")

        url = f"/{endpoint.lstrip('/')}"
        query_string = f"?{urlencode(params)}" if params else ""

        response = client.get(f"{url}{query_string}")
        assert response.status_code == 200, (
            f"Our API returned {response.status_code}: {response.text}"
        )
        return response.json()

    def normalize_data(self, data: Any) -> Any:
        """Normalize data for comparison (sort lists, handle floats, etc.)."""
        if isinstance(data, dict):
            # Sort dictionary keys and recursively normalize values
            return {k: self.normalize_data(v) for k, v in sorted(data.items())}
        elif isinstance(data, list):
            # Sort lists if they contain dictionaries with 'id' fields, otherwise preserve order
            if data and isinstance(data[0], dict):
                # Try to sort by common ID fields
                for id_field in ["project_id", "language_id", "id", "key_id"]:
                    if id_field in data[0]:
                        return sorted(
                            [self.normalize_data(item) for item in data],
                            key=lambda x: x.get(id_field, ""),
                        )
            return [self.normalize_data(item) for item in data]
        elif isinstance(data, float):
            # Round floats to avoid minor precision differences
            return round(data, 2)
        else:
            return data

    def compare_responses(
        self, lokalise_data: dict[str, Any], our_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Compare two API responses and return detailed differences."""
        normalized_lokalise = self.normalize_data(lokalise_data)
        normalized_ours = self.normalize_data(our_data)

        differences = {}

        def find_differences(path: str, lok_val: Any, our_val: Any):
            if lok_val != our_val:
                if isinstance(lok_val, dict) and isinstance(our_val, dict):
                    # Compare dict keys
                    lok_keys = set(lok_val.keys())
                    our_keys = set(our_val.keys())

                    if lok_keys != our_keys:
                        differences[f"{path}._keys"] = {
                            "lokalise_only": list(lok_keys - our_keys),
                            "ours_only": list(our_keys - lok_keys),
                        }

                    # Compare common keys
                    for key in lok_keys & our_keys:
                        find_differences(f"{path}.{key}", lok_val[key], our_val[key])

                elif isinstance(lok_val, list) and isinstance(our_val, list):
                    if len(lok_val) != len(our_val):
                        differences[f"{path}._length"] = {
                            "lokalise": len(lok_val),
                            "ours": len(our_val),
                        }

                    # Compare elements
                    for i, (lok_item, our_item) in enumerate(
                        zip(lok_val, our_val, strict=False)
                    ):
                        find_differences(f"{path}[{i}]", lok_item, our_item)

                else:
                    differences[path] = {"lokalise": lok_val, "ours": our_val}

        find_differences("", normalized_lokalise, normalized_ours)
        return differences

    async def test_endpoint_parity(
        self,
        lokalise_endpoint: str,
        our_endpoint: str,
        params: dict[str, Any] | None = None,
        ignore_fields: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Test that our endpoint returns the same data as Lokalise endpoint.

        Args:
            lokalise_endpoint: Lokalise API endpoint (e.g., "projects")
            our_endpoint: Our API endpoint (e.g., "lokalise/")
            params: Query parameters to send to both endpoints
            ignore_fields: List of field paths to ignore in comparison (e.g., ["projects[0].uuid"])

        Returns:
            Dictionary with test results and any differences found
        """
        params = params or {}
        ignore_fields = ignore_fields or []

        # Get data from both APIs
        lokalise_data = await self.call_lokalise_api(lokalise_endpoint, params)
        our_data = self.call_our_api(our_endpoint, params)

        # Remove ignored fields
        def remove_ignored_fields(data: Any, path: str = "") -> Any:
            if isinstance(data, dict):
                return {
                    k: remove_ignored_fields(v, f"{path}.{k}" if path else k)
                    for k, v in data.items()
                    if f"{path}.{k}" not in ignore_fields and path != k
                }
            elif isinstance(data, list):
                return [
                    remove_ignored_fields(item, f"{path}[{i}]")
                    for i, item in enumerate(data)
                    if f"{path}[{i}]" not in ignore_fields
                ]
            return data

        if ignore_fields:
            lokalise_data = remove_ignored_fields(lokalise_data)
            our_data = remove_ignored_fields(our_data)

        # Compare responses
        differences = self.compare_responses(lokalise_data, our_data)

        return {
            "endpoint": our_endpoint,
            "params": params,
            "matches": len(differences) == 0,
            "differences": differences,
            "lokalise_data_sample": json.dumps(lokalise_data, indent=2)[:500] + "...",
            "our_data_sample": json.dumps(our_data, indent=2)[:500] + "...",
        }


# Create global tester instance (only if configuration is available)
try:
    tester = APIParityTester()
except ValueError as e:
    tester = None
    configuration_error = str(e)


# Utility function for manual testing
async def manual_comparison(
    lokalise_endpoint: str, our_endpoint: str, params: dict[str, Any] | None = None
):
    """Manual comparison function for development/debugging."""
    if not tester:
        error_msg = (
            "API parity testing requires LOKALISE_API_TOKEN to be configured.\n"
            "Please ensure:\n"
            "1. LOKALISE_API_TOKEN is set in your .env file\n"
            "2. The .env file is being loaded by pytest\n"
            "3. The token is valid and has the required permissions"
        )
        if "configuration_error" in globals():
            error_msg += f"\n\nConfiguration error: {configuration_error}"
        raise ValueError(error_msg)

    result = await tester.test_endpoint_parity(lokalise_endpoint, our_endpoint, params)

    print(f"🔍 Testing: {our_endpoint}")
    print(f"Parameters: {params}")
    print(f"✅ Matches: {result['matches']}")

    if result["matches"]:
        print("🎉 Perfect match! Your endpoint returns identical data to Lokalise API.")
    else:
        print("\n❌ Differences found:")
        print(json.dumps(result["differences"], indent=2))

        print("\n📝 Lokalise API sample:")
        print(result["lokalise_data_sample"])

        print("\n📝 Your API sample:")
        print(result["our_data_sample"])

    return result


if __name__ == "__main__":
    # Example usage for development
    async def run_example():
        # Test projects endpoint
        result = await manual_comparison(
            lokalise_endpoint="projects",
            our_endpoint="api/v1/lokalise/",
            params={"include_statistics": 1, "include_settings": 1, "limit": 2},
        )

        return result

    # Run example
    asyncio.run(run_example())
