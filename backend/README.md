# Lokalize AI Translator Backend

A sophisticated FastAPI backend that bridges Lokalise localization projects with AI-powered translation using Google Gemini, featuring comprehensive API integration and modular service architecture.

## 🚀 Features

### Core Services

- **🔗 Comprehensive Lokalise Integration**: Full API integration mirroring Lokalise's endpoints structure
  - Project keys management with advanced filtering
  - Translation operations (get, update, create)
  - Glossary management (CRUD operations)
  - Pagination and cursor-based navigation
- **🤖 AI Translation**: Google Gemini 2.0 Flash Experimental model for high-quality translations
- **🏗️ Modular Architecture**: Refactored service layer with specialized services
- **🔄 Batch Processing**: Efficient batch translation capabilities
- **🌍 Multi-language Support**: 21+ supported languages
- **🛡️ Advanced Error Handling**: Comprehensive error handling with retry logic
- **⚡ Performance Optimized**: Tenacity-based retry mechanisms and caching

### Technical Features

- FastAPI framework for high-performance API development
- Pydantic v2 for data validation and settings management
- Type hints with basedpyright for robust type checking
- Ruff for code formatting and linting
- Structured logging with configurable levels
- CORS support for web applications
- Environment-based configuration
- Modular service architecture with clean separation of concerns
- **Glossary-Aware Translation**: Advanced translation with term protection and verification
- **Provider-Agnostic Design**: Abstract translation providers for easy extensibility

## 🛠️ Prerequisites

- Python 3.13+
- uv package manager
- Google Gemini API key
- Lokalise API token

## ⚙️ Setup

### 1. Install Dependencies

Using uv (recommended):

```bash
uv sync
```

### 2. Environment Configuration

Copy the example environment file and configure your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your API credentials:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:80,http://localhost

# API Keys (Required)
GEMINI_API_KEY=your-gemini-api-key-here
LOKALISE_API_TOKEN=your-lokalise-api-token-here

# Logging
LOG_LEVEL=INFO
```

### 3. Run the Development Server

```bash
uv run python main.py
```

The API will be available at:

- **Main API**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## 📡 API Endpoints

### Health & Status

```
GET /                    # Welcome message
GET /health             # Health check
GET /test-connection    # Connection test with timestamp
```

### Lokalise Integration (Full API Mirror)

#### Keys Management

```
GET /api/v1/projects/{project_id}/keys
# Get project keys with comprehensive filtering options
# Supports all Lokalise API parameters:
# - include_translations, include_comments, include_screenshots
# - filter_translation_lang_ids, filter_tags, filter_platforms
# - filter_untranslated, filter_archived, filter_keys, filter_key_ids
# - pagination (limit, page)
# - Custom extension: reviewed_only filter
```

#### Translation Operations

```
GET /api/v1/projects/{project_id}/translations
# Get project translations with advanced filtering
# Supports Lokalise API parameters:
# - disable_references, filter_lang_id, filter_is_reviewed
# - filter_unverified, filter_untranslated, filter_qa_issues
# - filter_active_task_id, pagination (offset/cursor), limit

GET /api/v1/projects/{project_id}/translations/{translation_id}
# Get specific translation by ID

PUT /api/v1/projects/{project_id}/translations/{translation_id}
# Update specific translation
```

#### Glossary Management

```
GET    /api/v1/projects/{project_id}/glossary-terms         # List glossary terms
GET    /api/v1/projects/{project_id}/glossary-terms/{term_id} # Get specific term
POST   /api/v1/projects/{project_id}/glossary-terms         # Create new terms
PUT    /api/v1/projects/{project_id}/glossary-terms         # Update existing terms
DELETE /api/v1/projects/{project_id}/glossary-terms         # Delete terms
```

### AI Translation Services

```
POST /api/v1/translation/translate                # Single text translation
POST /api/v1/translation/translate/batch          # Batch translation
POST /api/v1/translation/translate/glossary       # Glossary-aware single translation
POST /api/v1/translation/translate/glossary/batch # Glossary-aware batch translation
GET  /api/v1/translation/languages                # Supported language codes
```

### Glossary Processor (XLSX File Processing)

```
POST /api/v1/glossary/load                # Load glossary from XLSX file
POST /api/v1/glossary/find-terms          # Find glossary terms in text
POST /api/v1/glossary/replace-terms       # Replace terms with translations
POST /api/v1/glossary/wrap-terms          # Wrap terms with protective tags
POST /api/v1/glossary/lookup-term         # Look up specific term information
GET  /api/v1/glossary/languages           # Get available languages in glossary
GET  /api/v1/glossary/stats               # Get glossary statistics
```

## 🌍 Supported Languages

English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic, Hindi, Dutch, Swedish, Danish, Norwegian, Finnish, Polish, Turkish, Thai, Vietnamese

## 📋 Usage Examples

### Single Translation

```bash
curl -X POST "http://localhost:8000/api/v1/translation/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "source_text": "Hello, world!",
    "source_lang": "en",
    "target_lang": "es"
  }'
```

### Batch Translation

```bash
curl -X POST "http://localhost:8000/api/v1/translation/translate/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello", "Goodbye", "Thank you"],
    "source_lang": "en",
    "target_lang": "fr"
  }'
```

### Glossary-Aware Translation

```bash
# Single glossary-aware translation
curl -X POST "http://localhost:8000/api/v1/translation/translate/glossary" \
  -H "Content-Type: application/json" \
  -d '{
    "source_text": "Welcome to our DeFi Staking platform with crypto dust protection",
    "source_lang": "en",
    "target_lang": "fr",
    "project_id": "your_project_id",
    "preserve_forbidden_terms": true,
    "translate_allowed_terms": true
  }'

# Batch glossary-aware translation
curl -X POST "http://localhost:8000/api/v1/translation/translate/glossary/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "DeFi Staking rewards are distributed daily",
      "Crypto dust can be consolidated automatically"
    ],
    "source_lang": "en",
    "target_lang": "es",
    "project_id": "your_project_id",
    "preserve_forbidden_terms": true,
    "translate_allowed_terms": true
  }'
```

### Get Project Keys with Filtering

```bash
# Get untranslated keys for Spanish
curl "http://localhost:8000/api/v1/projects/{project_id}/keys?filter_translation_lang_ids=es&filter_untranslated=1"

# Get keys with specific tags
curl "http://localhost:8000/api/v1/projects/{project_id}/keys?filter_tags=ui,buttons&include_translations=1"
```

### Glossary Management (Lokalise API)

```bash
# Get all glossary terms
curl "http://localhost:8000/api/v1/projects/{project_id}/glossary-terms"

# Create new glossary terms
curl -X POST "http://localhost:8000/api/v1/projects/{project_id}/glossary-terms" \
  -H "Content-Type: application/json" \
  -d '{
    "terms": [
      {
        "term": "API",
        "definition": "Application Programming Interface",
        "language_iso": "en",
        "part_of_speech": "noun"
      }
    ]
  }'
```

### Glossary Processor (XLSX File Processing)

```bash
# Load glossary from XLSX file
curl -X POST "http://localhost:8000/api/v1/glossary/load?project_id=your_project_id" \
  -F "file=@glossary.xlsx"

# Find terms in text
curl -X POST "http://localhost:8000/api/v1/glossary/find-terms?project_id=your_project_id" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Welcome to our DeFi Staking platform with crypto dust protection"
  }'

# Replace terms with translations
curl -X POST "http://localhost:8000/api/v1/glossary/replace-terms?project_id=your_project_id" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Welcome to our DeFi Staking platform with crypto dust protection",
    "target_lang": "fr"
  }'

# Wrap terms for LLM protection
curl -X POST "http://localhost:8000/api/v1/glossary/wrap-terms?project_id=your_project_id" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Welcome to our DeFi Staking platform with crypto dust protection",
    "wrapper_tag": "PROTECTED_TERM"
  }'

# Look up specific term
curl -X POST "http://localhost:8000/api/v1/glossary/lookup-term?project_id=your_project_id" \
  -H "Content-Type: application/json" \
  -d '{
    "term": "DeFi Staking"
  }'

# Get glossary statistics
curl "http://localhost:8000/api/v1/glossary/stats?project_id=your_project_id"
```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py                  # API router configuration
│   │       └── endpoints/              # API endpoints
│   │           ├── lokalise.py         # Comprehensive Lokalise API mirror
│   │           ├── translation.py      # AI translation endpoints (enhanced)
│   │           └── glossary_processor.py # XLSX glossary processor endpoints
│   ├── core/
│   │   ├── config.py                   # Application settings & validation
│   │   └── logging.py                  # Structured logging configuration
│   ├── services/                       # Business logic services
│   │   ├── lokalise/                   # Modular Lokalise services
│   │   │   ├── __init__.py             # Service exports & compatibility
│   │   │   ├── base.py                 # Base service with common functionality
│   │   │   ├── glossary.py             # Glossary operations service
│   │   │   ├── keys.py                 # Key operations service
│   │   │   └── translations.py         # Translation operations service
│   │   ├── __init__.py                 # Service initialization & instances
│   │   ├── translation_provider.py     # Abstract translation provider
│   │   ├── gemini_service.py           # Google Gemini AI service
│   │   ├── glossary_processor.py       # XLSX glossary file processor
│   │   └── glossary_aware_translation.py # Glossary-aware translation service
│   ├── schemas/                        # Pydantic data models
│   │   ├── translation.py              # Translation request/response schemas
│   │   ├── glossary_translation.py     # Glossary-aware translation schemas
│   │   ├── glossary_processor.py       # Glossary processor schemas
│   │   └── lokalise/                   # Lokalise API schemas
│   │       ├── __init__.py             # Schema exports
│   │       ├── glossary.py             # Glossary data models
│   │       ├── keys.py                 # Key data models
│   │       ├── projects.py             # Project data models
│   │       └── translations.py         # Translation data models
│   └── main.py                         # FastAPI application setup
├── logs/                               # Application logs (auto-created)
├── pyproject.toml                      # Project configuration & dependencies
├── main.py                             # Application entry point
├── Dockerfile                          # Container configuration
├── REFACTORING_SUMMARY.md             # Service refactoring documentation
└── README.md                          # This file
```

## 🔧 Development

### Code Quality

Format and lint code:

```bash
uv run ruff check . --fix
uv run ruff format .
```

Type checking:

```bash
uv run basedpyright
```

### Testing

Run tests:

```bash
uv run pytest
```

### Service Architecture

The backend uses a modular service architecture:

#### New Modular Approach (Recommended)

```python
from app.services.lokalise.keys import lokalise_keys_service,
from app.services.lokalise.translations import lokalise_translations_service,
from app.services.lokalise.glossary import lokalise_glossary_service

# Use specific services
keys = await lokalise_keys_service.get_keys(project_id)
translations = await lokalise_translations_service.get_translations(project_id)
glossary_terms = await lokalise_glossary_service.get_glossary_terms(project_id)
```

#### Backward Compatible Approach

```python
from app.services.lokalise import lokalise_service

# Legacy interface still works
keys = await lokalise_service.get_keys(project_id)
translations = await lokalise_service.get_translations(project_id)
```

## 🚨 Error Handling

The backend includes comprehensive error handling for:

- **API Authentication**: Invalid API keys (Gemini/Lokalise)
- **Rate Limiting**: Quota exceeded and rate limit errors
- **Network Issues**: Timeouts and connection failures
- **Data Validation**: Invalid project IDs and malformed requests
- **Service Errors**: Internal service failures with detailed logging

## 🔒 Security Notes

- Store API keys securely in environment variables
- Use HTTPS in production
- Configure CORS origins appropriately for your frontend
- Monitor API usage and rate limits
- Regularly rotate API keys
- The application validates API keys on startup

## 🎯 Use Cases

- **Localization Teams**: Comprehensive Lokalise project management
- **Translation Workflows**: Seamless integration between Lokalise and AI translation
- **Content Managers**: Full CRUD operations on glossaries and translations
- **Developers**: API-first translation services with extensive Lokalise integration
- **Translation Agencies**: Professional translation workflows with centralized management

## 🐳 Docker Support

Build and run with Docker:

```bash
docker build -t lokalize-ai-backend .
docker run -p 8000:8000 --env-file .env lokalize-ai-backend
```

## 📖 Recent Updates

- **Glossary-Aware Translation**: Advanced translation system with term protection and verification
- **Provider-Agnostic Architecture**: Abstract translation providers for easy extensibility
- **Enhanced Translation Endpoints**: New glossary-aware endpoints with comprehensive verification
- **Modular Service Architecture**: Refactored monolithic service into specialized services
- **Enhanced Lokalise Integration**: Full API mirroring with advanced filtering
- **XLSX Glossary Processor**: New module for processing Excel glossary files with term lookup and replacement
- **Improved Error Handling**: Centralized error management with retry logic
- **Type Safety**: Comprehensive type hints and validation
- **Performance Optimizations**: Retry mechanisms and better resource management
