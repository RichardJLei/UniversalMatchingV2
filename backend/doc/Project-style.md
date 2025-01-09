DRY (Don't Repeat Yourself)
    Refer to ./Project-file-structure.md for existing services and modules.
    Reuse existing services/modules:
        Reuse logic from existing services or modules whenever possible.
    Build new services/modules:
        When the required logic is new.
        When coordination with multiple existing modules is necessary.
    Use abstractions:
        Introduce shared abstractions for reusable business logic.

Consistent Interface
    Follow established patterns for interfaces in services and modules.
    Ensure that changes to a service are isolated and do not affect unrelated modules.

Naming Conventions
    React Components: Use PascalCase (e.g., MyComponent.tsx).
    Functions: Include docstrings describing their purpose and parameters.
    REST API Endpoints:
        Use kebab-case (e.g., /file-management/parse).
        Prefix with version numbers (e.g., /api/v1/).
    Variables:
        Use camelCase for JavaScript/React variables.
        Use snake_case for Python variables.

Backend Folder Placement
    Domain-Specific Features: Place in \backend\apps.
    Vendor-Specific Integrations: Place in \backend\services.
    Shared Middleware: Place centralized auth and role-based access logic in \backend\shared\middleware.
    Utility Functions: Place shared utilities (e.g., ID generators) in \backend\shared\utils.
    Abstractions: Place reusable business logic in \backend\shared\abstractions.
    Configuration: Place config.py in \backend\config.

Frontend Folder Placement
    Feature-Specific UI: Place in \frontend\apps.
    Reusable Components: Place common UI elements in \frontend\shared\components.
    Layouts: Place header, footer, and sidebar components in \frontend\shared\layouts.
    React Context: Place global state management in \frontend\shared\contexts.
    Utilities: Place shared frontend utilities in \frontend\shared\utils.
    
Centralize reusable mock objects in tests/mocks/.
