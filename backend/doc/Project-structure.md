# Project Structure

## Backend Services

### 1. Authentication Service (✅ Completed)
- Interface: `backend/services/interfaces/auth.py`
- Implementation: `backend/services/implementations/auth/firebase_auth.py`
- Features:
  - User creation and management
  - Token verification
  - Error handling

### 2. Storage Service (✅ Completed)
- Interface: `backend/services/interfaces/storage.py`
- Implementation: `backend/services/implementations/storage/gcs.py`
- Features:
  - File upload with signed URLs
  - File deletion
  - Error handling
  - Permission management

### 3. Database Service (✅ Completed)
- Interface: `backend/services/interfaces/database.py`
- Implementation: `backend/services/implementations/database/mongodb.py`
- Features:
  - CRUD operations
  - Collection management
  - Error handling

## Frontend Structure

### 1. Core Components (✅ Completed)
- Layout: `frontend/src/shared/layouts/MainLayout.tsx`
- Navigation: `frontend/src/shared/components/NavigationBar.tsx`
- Theme: 
  - Toggle: `frontend/src/shared/components/ThemeToggle.tsx`
  - Context: `frontend/src/shared/contexts/ThemeContext.tsx`

### 2. Feature Modules
- Files Management: `frontend/src/apps/files/*`
- Parser: `frontend/src/apps/parser/*`
- Comparison: `frontend/src/apps/comparison/*`
- User Management: `frontend/src/apps/users/*`

## Project Layout

## Directory Layout
roject/
├── backend/ # Backend Python application
│ ├── init.py # Makes backend a Python package
│ ├── apps/ # Application-specific code
│ │ └── app1/ # First application module
│ │ └── services/ # App-specific services
│ ├── config/ # Configuration management
│ │ ├── init.py # Makes config a package
│ │ ├── config.py # Central configuration using Pydantic
│ │ └── .json # Credential files (gitignored)
│ ├── services/ # Core services layer
│ │ ├── init.py # Makes services a package
│ │ ├── factory.py # Service factory with dependency injection
│ │ ├── interfaces/ # Service interfaces/contracts
│ │ │ ├── auth.py # Authentication interface
│ │ │ ├── database.py # Database interface
│ │ │ └── storage.py # Storage interface
│ │ └── implementations/ # Concrete implementations
│ │ ├── auth/ # Auth implementations
│ │ ├── database/ # Database implementations
│ │ └── storage/ # Storage implementations
│ ├── tests/ # Test suite
│ │ ├── init.py # Makes tests a package
│ │ ├── conftest.py # Shared test fixtures
│ │ ├── integration/ # Integration tests
│ │ └── unit/ # Unit tests
│ └── doc/ # Documentation
└── frontend/ # Frontend React application
├── src/ # Source code directory
│ ├── apps/ # Feature-specific modules
│ │ ├── files/ # File management feature
│ │ │ ├── components/ # Feature-specific components
│ │ │ └── pages/ # File management pages
│ │ │ └── FileListPage.tsx # File list view
│ │ ├── parser/ # File parsing feature
│ │ │ └── pages/
│ │ │ └── ParserPage.tsx # Parser interface
│ │ ├── comparison/ # File comparison feature
│ │ │ └── pages/
│ │ │ └── ComparisonPage.tsx # Comparison interface
│ │ └── users/ # User management feature
│ │ └── pages/
│ │ └── UserManagementPage.tsx # User management interface
│ ├── shared/ # Shared components and utilities
│ │ ├── components/ # Reusable UI components
│ │ │ ├── AppRouter.tsx # Application routing
│ │ │ ├── NavigationBar.tsx # Main navigation
│ │ │ └── ThemeToggle.tsx # Theme switcher
│ │ ├── contexts/ # React contexts
│ │ │ └── ThemeContext.tsx # Theme management
│ │ ├── layouts/ # Layout components
│ │ │ └── MainLayout.tsx # Main app layout
│ │ └── utils/ # Utility functions
│ ├── App.tsx # Root component
│ ├── main.tsx # Application entry point
│ └── index.css # Global styles
├── public/ # Static assets
├── index.html # HTML entry point
├── package.json # Dependencies and scripts
├── tsconfig.json # TypeScript configuration
├── tailwind.config.js # Tailwind CSS configuration
└── vite.config.ts # Vite build configuration

## Key Components Explanation

### Applications (`apps/`)
Contains application-specific logic separated into modules. Each app module can have its own services, models, and utilities.

### Configuration (`config/`)
Manages all configuration settings using Pydantic for type safety and validation. Supports different environments (development, testing, production).

### Services (`services/`)
Core service layer implementing the dependency injection pattern:
- `interfaces/`: Defines abstract base classes for services
- `implementations/`: Contains concrete implementations for each service type
- `factory.py`: Provides service instantiation based on configuration

### Tests (`tests/`)
Comprehensive test suite organized by test type:
- `integration/`: Tests with real external services
  - `conftest.py`: Integration-specific fixtures and configurations
  - Test files for each service integration (MongoDB, GCS, S3, Firebase)
- `mocks/`: Mock implementations for testing
- `services/`: Unit tests for individual services
- `conftest.py`: Shared pytest fixtures

### Documentation (`doc/`)
Project documentation:
- `Project-structure.md`: This file
- `Project-style.md`: Coding conventions and style guide
- `Project-updates.md`: Changelog and update history

### Configuration Files
- `.env`: Development environment variables
- `.env.integration`: Integration test environment variables
  - Contains real service configurations for testing
  - Database, storage, and authentication settings
- `pytest.ini`: Pytest configuration including custom markers
  - Defines test categories (unit, integration, etc.)
  - Sets up asyncio testing
- `requirements.txt`: Production dependencies
- `requirements-test.txt`: Testing dependencies

## Testing Structure
- Unit Tests: Test individual components in isolation
- Integration Tests: Test with real external services
- Mock Services: Provide test implementations
- Fixtures: Reusable test setup and cleanup
- Markers: Categorize and organize tests