# Detailed Project Structure

📁 project/
├── 📁 backend/                  # Backend Python application root
│   ├── 📁 apps/                # Application-specific business logic
│   │   └── 📁 app1/           # First application module
│   │       └── 📁 services/   # App-specific services
│   │           └── 📄 file_service.py  # Handles file operations with storage service
│   │
│   ├── 📁 config/             # Configuration management
│   │   ├── 📄 __init__.py    # Makes config a package
│   │   ├── 📄 config.py      # Central configuration using Pydantic
│   │   └── 📄 *.json         # Credential files (gitignored)
│   │
│   ├── 📁 services/          # Core services layer
│   │   ├── 📄 factory.py     # Service factory for dependency injection
│   │   ├── 📁 interfaces/    # Abstract base classes for services
│   │   │   ├── 📄 auth.py    # Authentication service interface
│   │   │   ├── 📄 database.py # Database service interface
│   │   │   └── 📄 storage.py  # Storage service interface
│   │   └── 📁 implementations/ # Concrete service implementations
│   │       ├── 📁 auth/       # Auth implementations
│   │       │   └── 📄 firebase_auth.py  # Firebase authentication
│   │       ├── 📁 database/   # Database implementations
│   │       │   └── 📄 mongodb.py  # MongoDB implementation
│   │       └── 📁 storage/    # Storage implementations
│   │           ├── 📄 gcs.py  # Google Cloud Storage
│   │           └── 📄 s3.py   # AWS S3 Storage
│   │
│   ├── 📁 tests/             # Test suite
│   │   ├── 📄 conftest.py    # Shared test fixtures
│   │   ├── 📁 integration/   # Integration tests
│   │   │   ├── 📄 conftest.py  # Integration-specific fixtures
│   │   │   ├── 📄 test_firebase_auth.py  # Firebase auth tests
│   │   │   ├── 📄 test_gcs_storage.py    # GCS storage tests
│   │   │   └── 📄 test_mongodb.py        # MongoDB tests
│   │   ├── 📁 mocks/         # Mock implementations for testing
│   │   │   └── 📄 mock_services.py  # Mock service implementations
│   │   └── 📁 services/      # Service-specific tests
│   │       ├── 📄 test_auth_service.py    # Auth service tests
│   │       ├── 📄 test_database_service.py # Database service tests
│   │       └── 📄 test_storage_service.py  # Storage service tests
│   │
│   └── 📁 doc/              # Documentation
│       ├── 📄 Project-structure.md  # Project structure documentation
│       ├── 📄 Project-style.md     # Coding style guide
│       └── 📄 Project-updates.md   # Changelog and updates
│
└── 📁 frontend/            # Frontend React application
    ├── 📁 src/            # Source code directory
    │   ├── 📁 apps/      # Feature-specific modules
    │   │   ├── 📁 files/     # File management feature
    │   │   ├── 📁 parser/    # File parsing feature
    │   │   ├── 📁 comparison/ # File comparison feature
    │   │   └── 📁 users/     # User management feature
    │   │
    │   ├── 📁 shared/    # Shared components and utilities
    │   │   ├── 📁 components/ # Reusable UI components
    │   │   │   ├── 📄 Header.tsx     # Main header with navigation
    │   │   │   ├── 📄 Footer.tsx     # Site footer
    │   │   │   ├── 📄 Logo.tsx       # App logo component
    │   │   │   └── 📄 ThemeToggle.tsx # Dark/light mode toggle
    │   │   ├── 📁 contexts/  # React contexts
    │   │   │   └── 📄 ThemeContext.tsx # Theme management
    │   │   └── 📁 layouts/   # Layout components
    │   │       └── 📄 MainLayout.tsx  # Main app layout
    │   │
    │   ├── 📄 App.tsx    # Root React component
    │   └── 📄 main.tsx   # Application entry point
    │
    ├── 📄 package.json   # NPM dependencies and scripts
    ├── 📄 tsconfig.json  # TypeScript configuration
    └── 📄 vite.config.ts # Vite build configuration