# Test Suite Documentation

This directory contains the comprehensive test suite for the Lokalize AI Translator backend.

## Directory Structure

```
tests/
├── conftest.py                     # Pytest configuration and shared fixtures
├── api/                           # API endpoint tests
│   ├── test_lokalise/            # Lokalise API parity tests
│   │   ├── test_projects.py      # Projects API (implemented)
│   │   ├── test_keys.py          # Keys API (placeholder)
│   │   ├── test_languages.py     # Languages API (placeholder)
│   │   ├── test_glossary.py      # Glossary API (placeholder)
│   │   ├── test_translations.py  # Translations API (placeholder)
│   │   └── test_files.py         # Files API (placeholder)
│   ├── test_translation/         # Translation service tests
│   │   └── test_translation_endpoints.py (placeholder)
│   └── test_glossary_processor/   # Glossary processor tests
│       └── test_glossary_processor_endpoints.py (placeholder)
└── utils/
    └── test_parity.py             # API parity testing utilities
```

## Test Categories

### 1. Lokalise API Parity Tests (`test_lokalise/`)

Tests that ensure our API endpoints return identical responses to the official Lokalise API.

**Features:**

- Direct comparison with Lokalise API responses
- Parameter validation
- Response format validation
- Error handling verification

**Status:**

- ✅ **Projects API** - Implemented and functional
- 🚧 **Keys API** - Placeholder (ready for implementation)
- 🚧 **Languages API** - Placeholder (ready for implementation)
- 🚧 **Glossary API** - Placeholder (ready for implementation)
- 🚧 **Translations API** - Placeholder (ready for implementation)
- 🚧 **Files API** - Placeholder (ready for implementation)

### 2. Translation Service Tests (`test_translation/`)

Tests for our custom translation endpoints and services.

**Features:**

- Text translation functionality
- Glossary-aware translation
- Translation quality evaluation
- Bulk translation processing

**Status:** 🚧 Placeholder (ready for implementation)

### 3. Glossary Processor Tests (`test_glossary_processor/`)

Tests for glossary upload, processing, and synchronization features.

**Features:**

- CSV/XLSX file upload
- Glossary term processing
- Validation and error handling
- Lokalise synchronization

**Status:** 🚧 Placeholder (ready for implementation)

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Categories

**Lokalise API Parity Tests:**

```bash
pytest tests/api/test_lokalise/ -v
```

**Translation Service Tests:**

```bash
pytest tests/api/test_translation/ -v
```

**Glossary Processor Tests:**

```bash
pytest tests/api/test_glossary_processor/ -v
```

### Run Individual Test Files

**Projects API Tests:**

```bash
pytest tests/api/test_lokalise/test_projects.py -v
```

**Specific Test Method:**

```bash
pytest tests/api/test_lokalise/test_projects.py::TestProjectsAPI::test_projects_list_with_full_data -v
```

### Test Markers

The test suite uses pytest markers to categorize tests:

- `@pytest.mark.lokalise` - Tests requiring Lokalise API access
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests

**Run tests by marker:**

```bash
pytest -m "lokalise" -v          # Only Lokalise API tests
pytest -m "unit" -v              # Only unit tests
pytest -m "integration" -v       # Only integration tests
```

## Environment Setup

### Required Environment Variables

For Lokalise API parity tests:

```bash
export LOKALISE_API_TOKEN="your-lokalise-api-token"
```

Tests will be automatically skipped if required environment variables are not configured.

## Test Development Guidelines

1. **API Parity Tests**: Use the `manual_comparison` utility from `tests.utils.test_parity`
2. **Naming Convention**: Test files should be prefixed with `test_`
3. **Markers**: Use appropriate pytest markers for test categorization
4. **Documentation**: Each test should have a clear docstring explaining its purpose
5. **Skipping**: Use `pytest.skip()` for placeholder tests that are not yet implemented

## Adding New Tests

### 1. Lokalise API Endpoint Tests

1. Add test methods to the appropriate file in `tests/api/test_lokalise/`
2. Use the `@pytest.mark.lokalise` marker
3. Use `manual_comparison` for API parity verification

### 2. Custom Service Tests

1. Create test files in the appropriate subdirectory
2. Use `@pytest.mark.unit` or `@pytest.mark.integration` markers
3. Use the shared fixtures from `conftest.py`

### 3. Utility Functions

Add shared test utilities to `tests/utils/`
