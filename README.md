# Lokalize AI Translator

A modern web application for managing Lokalise translation projects with AI-powered assistance. This system provides an intuitive interface for translating content, managing glossaries, and ensuring translation quality through automated evaluation.

## 🏗 Architecture

- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui
- **Backend**: FastAPI + Python (with AI translation services)
- **Integration**: Lokalise API for project management
- **AI**: Google Gemini for translations, LLM evaluation for quality assessment

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20.x or higher
- **Python** 3.8+
- **pnpm** (for frontend package management)
- **uv** (for Python package management)
- **Lokalise API** access and project

### Local Development Setup

1. **Clone and setup**:

   ```bash
   git clone <repository-url>
   cd lokalize-ai-translator
   ```

2. **Backend setup**:

   ```bash
   cd backend
   uv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   uv pip install -e .

   # Configure environment variables
   cp .env.example .env
   # Edit .env with your API keys (Lokalise, Google Gemini, etc.)

   # Start backend server
   uv run python main.py
   ```

3. **Frontend setup**:

   ```bash
   cd frontend
   pnpm install

   # Configure environment
   cp .env.example .env
   # Default backend URL should work: VITE_API_URL=http://localhost:8000

   # Start development server
   pnpm run dev
   ```

4. **Access the application**:
   - Frontend: `http://localhost:5173`
   - Backend API docs: `http://localhost:8000/docs`

## 🎯 Core Functions

### Project Management

- **Browse Projects**: Select and load Lokalise projects
- **Project Overview**: View keys, name, and project id

### Translation Operations

- **View Translations**: Organized by key with status indicators (Reviewed/Unverified/Pending)
- **Edit Translations**: In-place editing with metadata tracking
- **Auto-Translate**: AI-powered translation with glossary preservation
- **Bulk Translation**: Translate all missing translations at once
- **Status Management**: Mark translations as reviewed/unverified

### Glossary Management

- **Upload Glossaries**: Import XLSX files with term definitions
- **Term Validation**: Automatic validation and categorization
- **Compliance Tracking**: Monitor glossary term usage in translations

### Quality Assurance

- **LLM Evaluation**: Get detailed feedback on translation quality
- **Metric Scoring**: BLEU, TER, chrF scores for objective assessment
- **Glossary Compliance**: Check adherence to project terminology
- **Detailed Feedback**: Strengths, weaknesses, and improvement suggestions

### Key Management

- **Create Keys**: Add new translation keys with metadata
- **Multi-platform Support**: iOS, Android, Web, Other platforms
- **Batch Creation**: Create multiple keys simultaneously

## 🔧 Development

### Frontend Commands

```bash
cd frontend
pnpm run dev          # Start development server
pnpm run build        # Build for production
pnpm run lint         # Run ESLint
pnpm run format       # Format code with Prettier
```

### Backend Commands

```bash
cd backend
uvicorn app.main:app --reload    # Start development server
pytest                           # Run tests
ruff check .                     # Lint code
ruff format .                    # Format code
```

### Docker Deployment

```bash
# Frontend
docker build -t lokalize-frontend ./frontend
docker run -p 80:80 lokalize-frontend

# Backend (configure as needed)
docker build -t lokalize-backend ./backend
docker run -p 8000:8000 lokalize-backend
```

## 🎨 Tech Stack

**Frontend**:

- React 19 with TypeScript
- Vite for build tooling
- Tailwind CSS + shadcn/ui components
- Lucide React icons
- Native fetch for API calls

**Backend**:

- FastAPI framework
- Pydantic for data validation
- Google Gemini API integration
- Lokalise API integration
- Async/await patterns

## ⚠️ Development Challenges & Current Limitations

During the development of this project, several challenges were encountered that impacted the final implementation:

### Lokalise API Integration Complexity

- **Extensive API Surface**: Lokalise provides a vast API with numerous endpoints for projects, keys, translations, comments, screenshots, and file management
- **Authentication & Rate Limits**: Managing API tokens, request limits, and error handling across multiple endpoints
- **Data Model Complexity**: Lokalise's data structures are intricate, requiring comprehensive TypeScript interfaces and careful mapping
- **Endpoint Variations**: Different endpoints have varying parameter requirements and response formats, making standardization challenging

### Time-Constrained Development

- **UI/UX Compromises**: The user interface took a backseat due to time limitations, resulting in functional but not optimally designed components
- **Limited Polish**: Many UI components lack refinement, responsive design considerations, and accessibility features
- **Basic State Management**: Using simple React hooks instead of more robust state management solutions

### Testing Gaps

- **Minimal Test Coverage**: Limited time prevented implementation of comprehensive test suites
- **Manual Testing Only**: Most functionality was verified through manual testing rather than automated tests
- **Integration Testing Missing**: No end-to-end testing of API integrations and user workflows

### Technical Debt

- **Code Organization**: Some components became too large and complex (e.g., `TranslationList.tsx` at 367 lines)
- **Error Handling**: Inconsistent error handling patterns across components
- **Performance Considerations**: No optimization for large datasets or virtual scrolling implementation

### Backend Integration Issues

- **Glossary Processing**: Backend encountered errors when uploading glossary terms to Lokalise API
- **Metric Calculations**: TER and BLEU score implementations need proper library integration
- **Database Layer Missing**: No persistent storage for LLM evaluations, user preferences, or translation history

### API Design Decisions

- **Frontend-Backend Coupling**: Some API responses are tightly coupled to Lokalise's data format
- **Limited Error Context**: Error messages don't always provide sufficient context for debugging
- **Inconsistent Response Formats**: Some endpoints return different data structures than expected

These challenges highlight the complexity of building production-ready translation management tools and provide a roadmap for future improvements.

## 📈 Potential Improvements

### Short-term Enhancements

- **Translation Memory**: Cache and reuse previous translations
- **Advanced Filtering**: Filter translations by status, language, date
- **Export Functions**: Download translations in various formats
- **Notification System**: Progress alerts and completion notifications
- **Keyboard Shortcuts**: Improve productivity with hotkeys

### Infrastructure & Architecture

- **UI Overhaul**: Redesign interface for better scalability and maintainability, right now it is only good for a few translations
- **Database Integration**: Persistent storage for LLM comments, translation history, and user analytics
- **Lokalise API Expansion**: Implement comprehensive coverage of remaining API endpoints
- **Multi-container Docker**: Robust orchestrated setup with database, cache, and service containers

### Quality & Performance

- **Metric Scoring Solutions**: Implement proper TER and BLEU score calculation libraries
- **Comprehensive Test Suite**: Unit, integration, and end-to-end testing across all components
- **Code Cleanup**: Refactor legacy code, eliminate duplication, improve maintainability
- **Batch Operations**: More bulk operations (delete, status updates)
- **Translation History**: Track and revert changes with full audit trails
- **Performance Optimization**: Virtual scrolling, lazy loading for large datasets
- **Error Recovery**: Better error handling, retry mechanisms, and user feedback
- **LLM Provider Abstraction**: Use portkey or openrouter to abstract the LLM provider completely

### Advanced Features

- **Machine Learning**: Custom translation models per project
- **Analytics Dashboard**: Translation productivity metrics and insights
- **Integration Expansion**: Support for other translation platforms (Crowdin, Transifex)
- **Advanced Glossary**: Term suggestions, auto-detection, and smart recommendations
- **Quality Scoring**: Custom quality metrics and configurable thresholds
- **Workflow Management**: Review processes, approval chains, and task assignment

### Developer Experience

- **GitHub Actions CI/CD**: Automated testing, building, and deployment pipeline
- **API Documentation**: Enhanced OpenAPI specs with interactive examples
- **Testing Infrastructure**: Automated test frameworks with coverage reporting
- **Code Quality**: Automated linting, formatting, and code review processes
- **Development Tools**: Better debugging utilities and development environment setup
- **Monitoring & Observability**: Application performance monitoring, logging, and alerting
