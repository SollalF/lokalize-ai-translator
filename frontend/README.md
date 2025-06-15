# Lokalize AI Translator - Frontend

A modern React-based frontend application for managing translation projects with AI-powered assistance. This application provides an intuitive interface for managing Lokalise projects, creating translation keys, and editing translations with automated translation capabilities.

## 🚀 Features

- **Project Management**: Browse and select Lokalise projects with detailed statistics
- **Translation Management**: View, edit, and manage translations across multiple languages
- **AI-Powered Translation**: Automatic translation with glossary term preservation
- **Translation Evaluation**: Get detailed LLM feedback on translation quality
- **Glossary Management**: Upload XLSX glossary files to Lokalise projects
- **Key Creation**: Create new translation keys with support for multiple platforms
- **Real-time Editing**: In-place translation editing with review status management
- **Responsive Design**: Modern UI built with Tailwind CSS and shadcn/ui components

## 🛠 Tech Stack

- **Framework**: React 19.1.0 with TypeScript
- **Build Tool**: Vite 6.3.5
- **Styling**: Tailwind CSS 4.x with shadcn/ui components
- **Icons**: Lucide React
- **State Management**: React hooks (useState, useEffect)
- **HTTP Client**: Native fetch API with custom service layer
- **Development Tools**: ESLint, Prettier, TypeScript

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/           # React components
│   │   ├── ui/              # shadcn/ui base components
│   │   ├── TranslationManager.tsx    # Main application component
│   │   ├── ProjectSelector.tsx       # Project selection interface
│   │   ├── TranslationList.tsx      # Translation listing and management
│   │   ├── TranslationEditor.tsx    # Translation editing modal
│   │   ├── KeyCreator.tsx           # Key creation interface
│   │   ├── GlossaryUploader.tsx     # Glossary file upload interface
│   │   └── TestConnection.tsx       # Backend connection testing
│   ├── services/            # API service layer
│   │   └── api.ts          # API client and service functions
│   ├── types/              # TypeScript type definitions
│   │   └── api.ts          # API response and request types
│   ├── lib/                # Utility functions
│   │   └── utils.ts        # Common utilities (cn function)
│   ├── assets/             # Static assets
│   ├── App.tsx             # Root application component
│   ├── main.tsx            # Application entry point
│   └── index.css           # Global styles and Tailwind config
├── public/                 # Static assets
├── package.json            # Dependencies and scripts
├── vite.config.ts          # Vite configuration
├── tsconfig.json           # TypeScript configuration
├── eslint.config.js        # ESLint configuration
├── .prettierrc             # Prettier configuration
└── Dockerfile              # Docker container configuration
```

## 🔧 Setup and Installation

### Prerequisites

- Node.js 20.x or higher
- pnpm (recommended package manager)
- Backend API running (typically on port 8000)

### Installation

1. **Install dependencies**:

   ```bash
   pnpm install
   ```

2. **Environment Configuration**:

   ```bash
   cp .env.example .env
   ```

   Configure your environment variables in `.env`:

   ```env
   VITE_API_URL=http://localhost:8000
   VITE_APP_NAME=Lokalize AI Translator
   VITE_APP_VERSION=0.1.0
   VITE_ENABLE_ANALYTICS=false
   VITE_ENABLE_DEBUG_MODE=false
   ```

3. **Start the development server**:

   ```bash
   pnpm dev
   ```

   The application will be available at `http://localhost:5173`

## 📜 Available Scripts

- `pnpm dev` - Start development server with hot reload
- `pnpm build` - Build for production
- `pnpm preview` - Preview production build locally
- `pnpm lint` - Run ESLint for code quality checks
- `pnpm format` - Format code with Prettier
- `pnpm format:check` - Check code formatting

## 🏗 Architecture Overview

### Component Hierarchy

```
App
└── TranslationManager (Main container)
    ├── ProjectSelector (Project selection)
    ├── TranslationList (Translation management)
    │   └── TranslationEditor (Modal for editing)
    ├── KeyCreator (Modal for creating keys)
    └── GlossaryUploader (Modal for uploading glossary files)
```

### API Integration

The application communicates with a backend API through a service layer (`src/services/api.ts`) that provides:

- **Project Management**: Fetch projects, project details, and statistics
- **Translation Operations**: CRUD operations for translations
- **Key Management**: Create and manage translation keys
- **Glossary Management**: Upload and manage glossary files
- **AI Translation**: Automated translation with glossary support

### State Management

- **Local State**: React hooks (useState, useEffect) for component-level state
- **Props**: Data flow between parent and child components
- **Callbacks**: Event handling and state updates propagated through props

## 🎨 UI Components

Built with **shadcn/ui** components for consistency and accessibility:

- **Button**: Primary actions and controls
- **Form Elements**: Inputs, textareas, checkboxes
- **Modals**: Overlay dialogs for editing and creation
- **Dropdowns**: Project selection and filtering
- **Status Indicators**: Translation review status and progress

## 🔄 API Proxy Configuration

Development requests are proxied to the backend through Vite configuration:

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

## 📱 Features in Detail

### Project Selection

- Browse available Lokalise projects
- View project statistics (keys, progress, languages)
- Automatic translation loading on project selection

### Translation Management

- Group translations by key for better organization
- View translation status (reviewed, unverified, pending)
- In-place editing with review status management
- Individual auto-translation with glossary term preservation
- Bulk auto-translation for all missing translations at once
- Real-time progress tracking for bulk operations
- LLM-powered translation evaluation with detailed feedback
- Glossary compliance checking and scoring
- Objective translation quality metrics (BLEU, TER, chrF)

### Key Creation

- Create multiple keys simultaneously
- Support for multiple platforms (iOS, Android, Web, Other)
- Add descriptions, tags, and context
- Set character limits and custom attributes

### Glossary Management

- Upload XLSX files containing glossary terms
- Support for multiple source languages
- Automatic validation of file format and size
- Real-time upload progress and detailed statistics
- Display term counts by category (case-sensitive, forbidden, translatable)

### AI Translation

- Preserve glossary terms during translation
- Batch translation capabilities
- Language detection and validation
- Translation verification and suggestions

## 🚀 Production Deployment

### Docker Deployment

1. **Build the Docker image**:

   ```bash
   docker build -t lokalize-frontend .
   ```

2. **Run the container**:
   ```bash
   docker run -p 80:80 lokalize-frontend
   ```

### Manual Deployment

1. **Build for production**:

   ```bash
   pnpm build
   ```

2. **Deploy the `dist/` folder** to your web server

## 🔧 Development Guidelines

### Code Style

- **ESLint**: Enforces code quality and consistency
- **Prettier**: Automatic code formatting
- **TypeScript**: Strong typing for better development experience

### Component Patterns

- **Functional Components**: Use React hooks for state management
- **Props Interface**: Define TypeScript interfaces for all props
- **Error Handling**: Implement proper error boundaries and user feedback
- **Loading States**: Show loading indicators for async operations

### File Naming

- **Components**: PascalCase (e.g., `TranslationManager.tsx`)
- **Utilities**: camelCase (e.g., `utils.ts`)
- **Types**: Descriptive interfaces (e.g., `Translation`, `Project`)

## 🐛 Troubleshooting

### Common Issues

- **API Connection**: Ensure backend is running on port 8000
- **Environment Variables**: Check `.env` file configuration
- **Dependencies**: Run `pnpm install` to ensure all packages are installed
- **Port Conflicts**: Change the dev server port in `vite.config.ts` if needed

### Debug Mode

Enable debug mode in `.env`:

```env
VITE_ENABLE_DEBUG_MODE=true
```

## 📄 License

This project is part of the Lokalize AI Translator system. Please refer to the main project license.
