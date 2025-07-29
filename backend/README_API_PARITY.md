# API Parity Testing Framework

This framework ensures that your service endpoints return exactly the same data as the Lokalise API. It's designed to help you build reliable API mirrors with confidence.

The framework is now organized in a comprehensive test suite located in the `tests/` directory, with dedicated sections for different API categories.

## 🎯 What It Does

- **Compares responses** between Lokalise API and your service
- **Detects differences** in data structure, values, and fields
- **Provides detailed reports** of any mismatches found
- **Supports parameter testing** with different query combinations
- **Handles data normalization** (sorting, float precision, etc.)

## 🚀 Quick Start

### 1. Test Structure Overview

```
tests/
├── conftest.py                     # Pytest configuration
├── api/
│   ├── test_lokalise/             # Lokalise API parity tests
│   │   ├── test_projects.py       # Projects API tests
│   │   ├── test_keys.py           # Keys API tests
│   │   └── ...                    # Other Lokalise endpoints
│   ├── test_translation/          # Translation service tests
│   └── test_glossary_processor/   # Glossary processor tests
└── utils/
    └── test_parity.py             # API parity utilities
```

### 2. Basic Comparison

```python
from tests.utils.test_parity import manual_comparison

# Compare a simple endpoint
result = await manual_comparison(
    lokalise_endpoint="projects",
    our_endpoint="api/v1/lokalise/",
    params={"include_statistics": 1, "limit": 5}
)
```

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific Lokalise API parity tests
pytest tests/api/test_lokalise/ -v

# Run individual test files
pytest tests/api/test_lokalise/test_projects.py -v

# Run with markers
pytest -m "lokalise" -v
```

## 📚 How to Use for New Endpoints

### Step 1: Create Your Service Endpoint

First, implement your service endpoint that mirrors a Lokalise API endpoint.

### Step 2: Add Test Case

Choose the appropriate test file in `tests/api/test_lokalise/` and add your test:

```python
# In tests/api/test_lokalise/test_keys.py
import pytest
from ...utils.test_parity import manual_comparison, tester

class TestKeysAPI:
    @pytest.mark.asyncio
    @pytest.mark.lokalise
    async def test_project_keys_list(self):
        """Test project keys list endpoint."""
        result = await manual_comparison(
            lokalise_endpoint="projects/123/keys",  # Lokalise API path
            our_endpoint="api/v1/lokalise/123/keys",  # Your endpoint path
            params={
                "filter_keys": "welcome",
                "include_translations": 1,
                "limit": 10
            }
        )

        assert result['matches'], (
            f"Keys endpoint mismatch: {result['differences']}"
        )
```

### Step 3: Run Your Test

```bash
# Run your specific test
pytest tests/api/test_lokalise/test_keys.py::TestKeysAPI::test_project_keys_list -v

# Run all keys tests
pytest tests/api/test_lokalise/test_keys.py -v
```

### Step 4: Interpret Results

#### ✅ Perfect Match

```
🎉 Perfect match! Your endpoint returns identical data to Lokalise API.
```

#### ❌ Differences Found

```json
{
  "projects[0].settings._keys": {
    "lokalise_only": ["new_field"],
    "ours_only": ["old_field"]
  },
  "projects[0].statistics.progress_total": {
    "lokalise": 75.5,
    "ours": 75.0
  }
}
```

## 🛠️ Advanced Features

### Ignoring Fields

Sometimes you want to ignore certain fields (like timestamps):

```python
# In your test file
from ...utils.test_parity import tester

# Direct usage of the parity tester
result = await tester.test_endpoint_parity(
    lokalise_endpoint="projects",
    our_endpoint="api/v1/lokalise/",
    params={"limit": 5},
    ignore_fields=[
        "projects[0].created_at",  # Ignore creation timestamp
        "projects[0].uuid"         # Ignore UUID field
    ]
)
```

### Custom Comparison Logic

The framework automatically handles:

- **Sorting lists** by ID fields (project_id, language_id, etc.)
- **Float precision** (rounds to 2 decimal places)
- **Dictionary key ordering**
- **Nested object comparisons**

### Testing Different Parameter Combinations

Use pytest's parametrize decorator for systematic testing:

```python
# In tests/api/test_lokalise/test_projects.py
import pytest
from ...utils.test_parity import manual_comparison

class TestProjectsAPI:
    @pytest.mark.asyncio
    @pytest.mark.lokalise
    @pytest.mark.parametrize(
        "params",
        [
            {"include_statistics": 1, "include_settings": 1, "limit": 5},
            {"include_statistics": 0, "include_settings": 0, "limit": 5},
            {"filter_team_id": 123, "limit": 10},
            {"page": 2, "limit": 5}
        ],
    )
    async def test_projects_list_parameter_variations(self, params):
        """Test projects list with various parameter combinations."""
        result = await manual_comparison(
            lokalise_endpoint="projects",
            our_endpoint="api/v1/lokalise/",
            params=params
        )

        assert result['matches'], (
            f"Projects list with params {params} mismatch: {result['differences']}"
        )
```

## 🔧 Framework Structure

### Core Components

1. **`APIParityTester`** - Main testing class
2. **`manual_comparison()`** - Simple comparison function
3. **`test_endpoint_parity()`** - Detailed testing method

### Key Methods

#### `call_lokalise_api(endpoint, params)`

Makes direct calls to Lokalise API with proper authentication.

#### `call_our_api(endpoint, params)`

Makes calls to your FastAPI service using TestClient.

#### `compare_responses(lokalise_data, our_data)`

Performs deep comparison and returns detailed difference report.

#### `normalize_data(data)`

Normalizes data for fair comparison (sorting, rounding, etc.).

## 📝 Example Workflow

### 1. Implement New Endpoint

```python
# In your FastAPI router (app/api/v1/endpoints/lokalise/...)
@router.get("/{project_id}/keys")
async def get_project_keys(project_id: str, limit: int = 100):
    return await lokalise_keys_service.list_keys(project_id, limit=limit)
```

### 2. Create Test

Add your test to the appropriate file in `tests/api/test_lokalise/`:

```python
# In tests/api/test_lokalise/test_keys.py
import pytest
from ...utils.test_parity import manual_comparison, tester

class TestKeysAPI:
    @pytest.mark.asyncio
    @pytest.mark.lokalise
    async def test_project_keys_list(self):
        """Test project keys list endpoint."""
        # Get a real project ID first
        projects_data = await tester.call_lokalise_api("projects", {"limit": 1})

        if not projects_data.get("projects"):
            pytest.skip("No projects available for testing")

        project_id = projects_data["projects"][0]["project_id"]

        # Test the endpoint
        result = await manual_comparison(
            lokalise_endpoint=f"projects/{project_id}/keys",
            our_endpoint=f"api/v1/lokalise/{project_id}/keys",
            params={"limit": 5}
        )

        assert result['matches'], (
            f"Keys endpoint mismatch: {result['differences']}"
        )
```

### 3. Run and Fix

```bash
# Run your specific test
pytest tests/api/test_lokalise/test_keys.py::TestKeysAPI::test_project_keys_list -v

# Or run all keys tests
pytest tests/api/test_lokalise/test_keys.py -v
```

### 4. Iterate Until Perfect

Keep adjusting your service implementation until the test shows:

```
🎉 Perfect match! Your endpoint returns identical data to Lokalise API.
```

## 🎛️ Configuration

### Environment Setup

Make sure your `.env` file has:

```env
LOKALISE_API_TOKEN=your_api_token_here
```

### Custom Base URLs

Modify the tester if needed:

```python
tester = APIParityTester()
tester.lokalise_base_url = "https://api.lokalise.com/api2"  # Default
tester.our_base_url = "http://localhost:8000/api/v1"        # Your API
```

## 🚦 Best Practices

### 1. Start Simple

Begin with basic endpoints (like projects list) before moving to complex ones.

### 2. Test Parameter Variations

Don't just test default parameters - try different combinations.

### 3. Use Real Data

Test with actual project IDs, not mock data.

### 4. Handle Missing Endpoints Gracefully

```python
try:
    result = await manual_comparison(...)
except Exception as e:
    if "404" in str(e):
        print("⚠️ Endpoint not implemented yet")
    else:
        raise
```

### 5. Automate Your Tests

Add parity tests to your CI/CD pipeline using the organized test structure:

```bash
# In your CI/CD pipeline
# Run all Lokalise API parity tests
pytest tests/api/test_lokalise/ -v --tb=short

# Run with coverage
pytest tests/api/test_lokalise/ --cov=app --cov-report=html

# Run only tests that require Lokalise API
pytest -m "lokalise" -v

# Generate test report
pytest tests/ --html=report.html --self-contained-html
```

The organized test structure makes it easy to:

- Run specific endpoint categories
- Track test coverage by API domain
- Integrate with CI/CD systems
- Generate detailed test reports

## 🎉 Success Stories

Once you see this message, you know your endpoint is production-ready:

```
🎉 Perfect match! Your endpoint returns identical data to Lokalise API.
```

This means:

- ✅ **Data structure** matches exactly
- ✅ **Field names** are identical
- ✅ **Value types** are correct
- ✅ **Nested objects** are properly handled
- ✅ **Parameters** work as expected

## 🛟 Troubleshooting

### Common Issues

#### "404 Not Found"

- Check your endpoint path in FastAPI router
- Verify the endpoint is included in your app

#### "Field required" Pydantic errors

- Your schema is stricter than the API response
- Make fields optional or add default values

#### "Too many differences"

- Start with simple parameters first
- Check if you're missing required query parameters
- Verify authentication is working

#### Authentication errors

- Check your `LOKALISE_API_TOKEN` environment variable
- Verify the token has correct permissions

### Getting Help

1. **Check the difference report** - it shows exactly what doesn't match
2. **Test with minimal parameters** first
3. **Compare raw JSON responses** using the sample outputs
4. **Verify your schema** matches the actual API response structure

Remember: The goal is **identical responses**. Even small differences in field names or data types will be caught by this framework.

## 📁 Test Organization

The test suite is organized into logical categories:

### Lokalise API Tests (`tests/api/test_lokalise/`)

Each Lokalise API domain has its own test file:

- **`test_projects.py`** - ✅ Projects API (implemented)
- **`test_keys.py`** - 🚧 Keys API (placeholder)
- **`test_languages.py`** - 🚧 Languages API (placeholder)
- **`test_glossary.py`** - 🚧 Glossary API (placeholder)
- **`test_translations.py`** - 🚧 Translations API (placeholder)
- **`test_files.py`** - 🚧 Files API (placeholder)

### Custom Service Tests

- **`test_translation/`** - Translation service endpoints
- **`test_glossary_processor/`** - Glossary processing endpoints

### Shared Utilities (`tests/utils/`)

- **`test_parity.py`** - Core API parity testing framework
- Common fixtures and utilities for all tests

This organization makes it easy to:

- Find tests for specific API domains
- Add new endpoints within existing categories
- Run targeted test suites during development
- Maintain clean separation between Lokalise parity and custom features
