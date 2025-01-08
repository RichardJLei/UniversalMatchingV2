# Project Structure

## Frontend Structure

### 1. Core Components (✅ Completed)
- Layout: 
  - `MainLayout.tsx`: Main application layout with header, content area, and footer
  - `Header.tsx`: Application header with logo, navigation, and user controls
  - `Footer.tsx`: Application footer with links and copyright information
- Navigation:
  - `NavigationBar.tsx`: Main navigation menu
  - `Logo.tsx`: Application logo and branding
  - `UserMenu.tsx`: User authentication controls
- Theme: 
  - `ThemeToggle.tsx`: Dark/light mode toggle
  - `ThemeContext.tsx`: Theme state management

### 2. Feature Modules
- Files Management: `frontend/src/apps/files/*`
- Parser: `frontend/src/apps/parser/*`
- Comparison: `frontend/src/apps/comparison/*`
- User Management: `frontend/src/apps/users/*`

## Directory Layout

project/
├── backend/                   # Backend Python application
│   ├── __init__.py           # Makes backend a Python package
│   ├── apps/                 # Application-specific code
│   │   └── app1/            # First application module
│   │       └── services/    # App-specific services
│   ├── config/              # Configuration management
│   │   ├── __init__.py     # Makes config a package
│   │   ├── config.py       # Central configuration using Pydantic
│   │   └── *.json          # Credential files (gitignored)
│   ├── services/           # Core services layer
│   │   ├── __init__.py     # Makes services a package
│   │   ├── factory.py      # Service factory with dependency injection
│   │   ├── interfaces/     # Service interfaces/contracts
│   │   │   ├── auth.py     # Authentication interface
│   │   │   ├── database.py # Database interface
│   │   │   └── storage.py  # Storage interface
│   │   └── implementations/ # Concrete implementations
│   │       ├── auth/       # Auth implementations
│   │       ├── database/   # Database implementations
│   │       └── storage/    # Storage implementations
│   ├── tests/              # Test suite
│   │   ├── __init__.py    # Makes tests a package
│   │   ├── conftest.py    # Shared test fixtures
│   │   ├── integration/   # Integration tests
│   │   └── unit/         # Unit tests
│   └── doc/              # Documentation
│       ├── Project-structure.md  # Project structure documentation
│       ├── Project-style.md     # Coding style guide
│       └── Project-updates.md   # Changelog and updates
└── frontend/                    # Frontend React application
    ├── src/
    │   ├── apps/               # Feature-specific modules
    │   │   ├── files/         # File management feature
    │   │   │   ├── components/ # Feature-specific components
    │   │   │   └── pages/     # File management pages
    │   │   │       └── FileListPage.tsx
    │   │   ├── parser/        # File parsing feature
    │   │   │   └── pages/
    │   │   │       └── ParserPage.tsx
    │   │   ├── comparison/    # File comparison feature
    │   │   │   └── pages/
    │   │   │       └── ComparisonPage.tsx
    │   │   └── users/         # User management feature
    │   │       └── pages/
    │   │           └── UserManagementPage.tsx
    │   ├── shared/            # Shared components and utilities
    │   │   ├── components/    # Reusable UI components
    │   │   │   ├── AppRouter.tsx     # Application routing
    │   │   │   ├── Header.tsx        # Main header component
    │   │   │   ├── Footer.tsx        # Main footer component
    │   │   │   ├── Logo.tsx          # App logo and branding
    │   │   │   ├── NavigationBar.tsx # Main navigation
    │   │   │   ├── ThemeToggle.tsx   # Theme switcher
    │   │   │   └── UserMenu.tsx      # User authentication UI
    │   │   ├── contexts/     # React contexts
    │   │   │   └── ThemeContext.tsx  # Theme management
    │   │   ├── layouts/      # Layout components
    │   │   │   └── MainLayout.tsx    # Main app layout
    │   │   └── utils/        # Utility functions
    │   ├── App.tsx          # Root component
    │   ├── main.tsx         # Application entry point
    │   └── index.css        # Global styles and theme variables
    ├── public/              # Static assets
    ├── index.html          # HTML entry point
    ├── package.json        # Dependencies and scripts
    ├── tsconfig.json      # TypeScript configuration
    ├── tailwind.config.js # Tailwind CSS configuration
    └── vite.config.ts     # Vite build configuration

## Component Architecture

### Layout Components
- **MainLayout**: Provides the base structure
  - Header: App-wide navigation and controls
  - Main content area: Feature-specific pages
  - Footer: Links and copyright information

### Navigation System
- **Header**: Contains:
  - Logo: App branding
  - NavigationBar: Main menu
  - ThemeToggle: Theme controls
  - UserMenu: Authentication options

### Theme System
- **ThemeContext**: Manages theme state
  - Persists user preference
  - Provides theme switching
  - Applies consistent styling

### Feature Pages
Each feature module contains:
- Pages: Main view components
- Components: Feature-specific UI elements
- Utils: Feature-specific utilities

## Styling Architecture
- Tailwind CSS for utility-first styling
- Dark/light theme support
- Consistent color schemes
- Responsive design
- Interactive elements (hover, focus states)

## Configuration
- TypeScript for type safety
- Path aliases for clean imports
- Vite for development and building
- Environment-specific settings

## Next Steps
1. API Integration
   - [ ] Authentication endpoints
   - [ ] File management API
   - [ ] Parser service integration
   - [ ] Comparison service integration

2. Feature Implementation
   - [ ] File upload interface
   - [ ] PDF parsing visualization
   - [ ] Comparison tool UI
   - [ ] User profile management

3. Documentation
   - [ ] Component documentation
   - [ ] API integration guides
   - [ ] Deployment procedures