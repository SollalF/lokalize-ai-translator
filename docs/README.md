# Lokalize AI Translator

A modern web application for AI-powered translation services, built with a React frontend and Python backend.

## Project Overview

This project is a full-stack application that provides AI-powered translation services. It consists of two main parts:

1. A modern React frontend built with TypeScript
2. A Python backend service

## Technology Stack

### Frontend

The frontend is built using the following technologies:

- **React 19**: Modern UI library for building user interfaces
- **TypeScript**: For type-safe JavaScript development
- **Vite**: Next-generation frontend tooling
- **TailwindCSS**: Utility-first CSS framework
- **shadcn/ui**: Re-usable components built with Radix UI and Tailwind CSS
- **Radix UI**: Unstyled, accessible components
- **Lucide React**: Beautiful & consistent icons
- **pnpm**: Fast, disk space efficient package manager for Node.js

#### Key Frontend Dependencies:

- `@radix-ui/react-slot`: For component composition
- `class-variance-authority`: For component variants
- `clsx` & `tailwind-merge`: For class name management
- `tailwindcss`: For styling

### Backend

The backend is built using:

- **Python 3.13+**: Modern Python version
- **Project Structure**: Using modern Python project layout with `pyproject.toml`
- **uv**: Fast Python package installer and resolver

## Project Structure

```
lokalize-ai-translator/
├── frontend/               # React frontend application
│   ├── src/               # Source code
│   │   ├── components/    # React components including shadcn/ui
│   │   └── ui/           # shadcn/ui components
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
├── backend/               # Python backend application
│   ├── app/              # Application code
│   ├── tests/            # Test files
│   └── pyproject.toml    # Project configuration
├── docs/                  # Project documentation
└── docker-compose.yml    # Docker compose configuration
```

## Development Setup

### Prerequisites

1. Install pnpm (if not already installed):

   ```bash
   npm install -g pnpm
   ```

2. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies using pnpm:

   ```bash
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   ```

### Backend Setup

1. Ensure Python 3.13+ is installed
2. Install project dependencies using uv:
   ```bash
   uv pip install -e .
   ```

## Docker Setup

The project includes Docker configuration for both frontend and backend services, making it easy to run the entire application in a containerized environment.

### Prerequisites

- Docker
- Docker Compose

### Running with Docker

1. Build and start the services:

   ```bash
   docker compose up --build
   ```

2. Access the application:

   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

3. Stop the services:
   ```bash
   docker compose down
   ```

### Docker Configuration

The project uses a multi-stage build process for both frontend and backend:

#### Frontend Dockerfile

- Uses Node.js for building the React application
- Nginx for serving the built application
- Includes proper caching and optimization
- Handles API proxy configuration

#### Backend Dockerfile

- Uses Python 3.13
- Implements uv for dependency management
- Includes proper caching for faster builds
- Configures environment variables

#### Docker Compose

- Orchestrates both frontend and backend services
- Sets up proper networking between services
- Includes health checks for the backend
- Configures environment variables

### Development with Docker

For development, you can use the following commands:

1. Rebuild a specific service:

   ```bash
   docker compose up --build <service-name>
   ```

2. View logs:

   ```bash
   docker compose logs -f
   ```

3. Access container shell:
   ```bash
   docker compose exec <service-name> sh
   ```

### Production Considerations

For production deployment:

1. Set appropriate environment variables
2. Configure proper CORS settings
3. Set up SSL/TLS certificates
4. Configure proper logging
5. Set up monitoring and health checks

## Available Scripts

### Frontend

- `pnpm dev`: Start development server
- `pnpm build`: Build for production
- `pnpm lint`: Run ESLint
- `pnpm preview`: Preview production build

## Package Management

### Frontend (pnpm)

This project uses pnpm as its package manager for the frontend. pnpm offers several advantages:

- Faster installation times
- Efficient disk space usage through content-addressable storage
- Strict dependency management
- Built-in monorepo support

### Backend (uv)

The backend uses uv for Python package management:

- Extremely fast package installation
- Modern dependency resolution
- Compatible with existing Python tooling
- Built-in virtual environment management

## UI Components

This project uses shadcn/ui, a collection of re-usable components built with Radix UI and Tailwind CSS. Key features:

- **Accessibility**: All components are built with accessibility in mind
- **Customization**: Components are fully customizable through Tailwind CSS
- **Type Safety**: Built with TypeScript for better developer experience
- **Copy-Paste**: Components can be copied directly into your project
- **Dark Mode**: Built-in support for dark mode
- **Theming**: Easy to customize and extend

### Adding New Components

To add new shadcn/ui components to the project:

```bash
pnpm dlx shadcn-ui@latest add [component-name]
```

For example, to add a button component:

```bash
pnpm dlx shadcn-ui@latest add button
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Add your license information here]
