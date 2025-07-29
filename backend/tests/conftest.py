"""
Pytest configuration and shared fixtures for the test suite.
"""

import os
import sys
from pathlib import Path

import pytest

# Add the backend app directory to Python path for imports
backend_root = Path(__file__).parent.parent
app_path = backend_root / "app"
if str(app_path) not in sys.path:
    sys.path.insert(0, str(app_path))
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

# Import after path setup
try:
    from fastapi.testclient import TestClient

    from app.core.config import get_settings
    from app.main import app

    @pytest.fixture(scope="session")
    def test_client():
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    @pytest.fixture(scope="session")
    def settings():
        """Get application settings."""
        return get_settings()

    @pytest.fixture(scope="session")
    def lokalise_api_available(settings):
        """Check if Lokalise API token is available for testing."""
        return bool(settings.LOKALISE_API_TOKEN)

    # Skip tests that require Lokalise API if token is not available
    skip_if_no_lokalise = pytest.mark.skipif(
        not os.getenv("LOKALISE_API_TOKEN"), reason="LOKALISE_API_TOKEN not configured"
    )

except (ImportError, ValueError) as e:
    # If app can't be imported, create dummy fixtures
    error_msg = str(e)

    @pytest.fixture(scope="session")
    def test_client():
        pytest.skip(f"FastAPI app not available: {error_msg}")

    @pytest.fixture(scope="session")
    def settings():
        pytest.skip(f"Settings not available: {error_msg}")

    @pytest.fixture(scope="session")
    def lokalise_api_available():
        return False

    skip_if_no_lokalise = pytest.mark.skip(reason="App configuration not available")


# Configure pytest
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "lokalise: mark test as requiring Lokalise API access"
    )
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "unit: mark test as a unit test")
