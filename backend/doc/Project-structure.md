# Project Structure

## Directory Layout
backend/
├── __init__.py                # Makes the backend directory a Python package
├── apps/                      # Application-specific code
│   └── app1/                  # First application module
│       └── services/          # Application-specific services
│           └── file_service.py # Handles file operations for app1
├── config/                    # Configuration management
│   └── config.py             # Central configuration using Pydantic settings
├── services/                  # Core services layer
│   ├── __init__.py           # Makes services a package
│   ├── factory.py            # Factory pattern for service instantiation
│   ├── implementations/      # Concrete implementations of services
│   │   ├── auth/            # Authentication implementations
│   │   │   └── firebase_auth.py # Firebase authentication service
│   │   ├── database/        # Database implementations
│   │   │   └── mongodb.py   # MongoDB service implementation
│   │   └── storage/         # Storage implementations
│   │       ├── gcs.py       # Google Cloud Storage implementation
│   │       └── s3.py        # AWS S3 storage implementation
│   └── interfaces/          # Service interfaces/contracts
│       ├── auth.py          # Authentication service interface
│       ├── database.py      # Database service interface
│       └── storage.py       # Storage service interface
├── tests/                    # Test suite
│   ├── __init__.py          # Makes tests a package
│   ├── conftest.py          # Shared pytest fixtures
│   ├── test_basic.py        # Basic functionality tests
│   ├── test_factory.py      # Tests for service factory
│   ├── integration/         # Integration tests with real services
│   │   ├── __init__.py     # Makes integration tests a package
│   │   ├── conftest.py     # Integration-specific test fixtures
│   │   ├── test_mongodb.py # MongoDB integration tests
│   │   ├── test_storage_gcs.py # GCS integration tests
│   │   ├── test_storage_s3.py # S3 integration tests
│   │   └── test_firebase.py # Firebase integration tests
│   ├── mocks/              # Mock implementations for testing
│   │   ├── __init__.py    # Makes mocks a package
│   │   └── mock_services.py # Mock service implementations
│   └── services/           # Unit tests for services
│       ├── __init__.py    # Makes service tests a package
│       ├── test_auth_service.py # Auth service tests
│       ├── test_database_service.py # Database service tests
│       └── test_storage_service.py # Storage service tests
├── doc/                     # Project documentation
│   ├── Project-structure.md # This file - project structure documentation
│   ├── Project-style.md    # Coding style guidelines
│   └── Project-updates.md  # Project update logs
├── .env                    # Environment variables for development
├── .env.integration        # Environment variables for integration testing
├── pytest.ini             # Pytest configuration and test markers
├── requirements.txt       # Project dependencies
└── requirements-test.txt  # Testing dependencies

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