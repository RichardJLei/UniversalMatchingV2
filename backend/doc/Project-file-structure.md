# Detailed Project Structure

📁 project/
├── 📁 backend/                  # Backend Python application root
│   ├── 📁 apps/                # Application-specific business logic
│   │   ├── 📁 app1/           # First application module
│   │   │   └── 📁 services/   # App-specific services
│   │   │       └── 📄 file_service.py  # Handles file operations
│   │   └── 📁 auth/           # Authentication module
│   │       ├── 📄 __init__.py # Makes auth a package
│   │       └── 📄 routes.py   # Auth endpoints and handlers
│   │
│   ├── 📁 config/             # Configuration management
│   │   ├── 📄 __init__.py    # Makes config a package
│   │   ├── 📄 config.py      # Central configuration using Pydantic
│   │   └── 📄 *.json         # Credential files (gitignored)
│   │
│   ├── 📁 services/          # Core services layer
│   │   ├── 📄 factory.py     # Service factory for dependency injection
│   │   ├── 📁 interfaces/    # Abstract base classes for services
│   │   │   ├── 📄 __init__.py # Makes interfaces a package
│   │   │   ├── 📄 auth.py    # Authentication service interface
│   │   │   ├── 📄 database.py # Database service interface
│   │   │   └── 📄 storage.py  # Storage service interface
│   │   └── 📁 implementations/ # Concrete service implementations
│   │       ├── 📁 __init__.py  # Makes implementations a package
│   │       ├── 📁 auth/       # Auth implementations
│   │       │   ├── 📄 __init__.py  # Makes auth implementations a package
│   │       │   └── 📄 firebase_auth.py  # Firebase authentication
│   │       ├── 📁 database/   # Database implementations
│   │       │   └── 📄 mongodb.py  # MongoDB implementation
│   │       └── 📁 storage/    # Storage implementations
│   │           ├── 📄 gcs.py  # Google Cloud Storage
│   │           └── 📄 s3.py   # AWS S3 Storage
│   │
│   ├── 📁 tests/             # Test suite
│   │   ├── 📄 __init__.py    # Makes tests a package
│   │   ├── 📄 conftest.py    # Shared test fixtures
│   │   ├── 📄 test_basic.py  # Basic test configuration
│   │   ├── 📄 test_factory.py # Service factory tests
│   │   ├── 📄 test_file_service.py # File service tests
│   │   ├── 📁 integration/   # Integration tests
│   │   │   ├── 📄 __init__.py  # Makes integration tests a package
│   │   │   ├── 📄 conftest.py  # Integration-specific fixtures
│   │   │   ├── 📄 test_firebase_auth.py  # Firebase auth tests
│   │   │   ├── 📄 test_gcs_storage.py    # GCS storage tests
│   │   │   ├── 📄 test_mongodb.py        # MongoDB tests
│   │   │   └── 📄 test_storage_integration.py # Storage integration tests
│   │   ├── 📁 mocks/         # Mock implementations for testing
│   │   │   ├── 📄 __init__.py  # Makes mocks a package
│   │   │   └── 📄 mock_services.py  # Mock service implementations
│   │   └── 📁 services/      # Service-specific tests
│   │       ├── 📄 __init__.py  # Makes service tests a package
│   │       ├── 📄 test_auth_service.py    # Auth service tests
│   │       ├── 📄 test_database_service.py # Database service tests
│   │       └── 📄 test_storage_service.py  # Storage service tests
│   │
│   ├── 📄 app.py            # Flask application entry point
│   ├── 📄 setup.py          # Python package configuration
│   ├── 📄 requirements.txt  # Production dependencies
│   ├── 📄 requirements-test.txt # Test dependencies
│   ├── 📄 pytest.ini       # Pytest configuration
│   ├── 📄 .env             # Environment variables
│   ├── 📄 .env.template    # Environment template
│   ├── 📄 .env.integration # Integration test environment
│   └── 📄 .flaskenv        # Flask-specific settings
│
└── 📁 frontend/            # Frontend React application
    ├── 📁 src/            # Source code directory
    │   ├── 📁 apps/      # Feature-specific modules
    │   │   ├── 📁 comparison/ # File comparison feature
    │   │   │   └── 📁 pages/
    │   │   │       └── 📄 ComparisonPage.tsx
    │   │   ├── 📁 files/     # File management feature
    │   │   │   └── 📁 pages/
    │   │   │       └── 📄 FileListPage.tsx
    │   │   ├── 📁 home/      # Home feature
    │   │   │   └── 📁 pages/
    │   │   │       └── 📄 HomePage.tsx
    │   │   ├── 📁 parser/    # File parsing feature
    │   │   │   └── 📁 pages/
    │   │   │       └── 📄 ParserPage.tsx
    │   │   └── 📁 users/     # User management feature
    │   │       └── 📁 pages/
    │   │           └── 📄 UserManagementPage.tsx
    │   │
    │   ├── 📁 shared/    # Shared components and utilities
    │   │   ├── 📁 components/ # Reusable UI components
    │   │   │   ├── 📄 AppRouter.tsx  # Application routing
    │   │   │   ├── 📄 Footer.tsx     # Site footer
    │   │   │   ├── 📄 Header.tsx     # Main header with navigation
    │   │   │   ├── 📄 Logo.tsx       # App logo component
    │   │   │   ├── 📄 NavigationBar.tsx # Navigation menu
    │   │   │   ├── 📄 ThemeToggle.tsx # Dark/light mode toggle
    │   │   │   └── 📄 UserMenu.tsx    # User account menu
    │   │   ├── 📁 contexts/  # React contexts
    │   │   │   ├── 📄 AuthContext.tsx # Authentication context
    │   │   │   └── 📄 ThemeContext.tsx # Theme management
    │   │   ├── 📁 layouts/   # Layout components
    │   │   │   └── 📄 MainLayout.tsx  # Main app layout
    │   │   └── 📁 services/  # Frontend services
    │   │       ├── 📁 implementations/
    │   │       │   └── 📁 firebase/
    │   │       │       └── 📄 firebaseAuth.ts
    │   │       └── 📁 interfaces/
    │   │           └── 📄 auth.ts
    │   │
    │   ├── 📄 App.tsx    # Root React component
    │   ├── 📄 index.css  # Global styles
    │   └── 📄 main.tsx   # Application entry point
    │
    ├── 📄 .env           # Environment variables
    ├── 📄 .env.template  # Environment template
    ├── 📄 .gitignore     # Git ignore rules
    ├── 📄 package.json   # NPM dependencies and scripts
    ├── 📄 tailwind.config.js # Tailwind CSS configuration
    ├── 📄 tsconfig.json  # TypeScript configuration
    ├── 📄 tsconfig.node.json # Node-specific TS config
    └── 📄 vite.config.ts # Vite build configuration