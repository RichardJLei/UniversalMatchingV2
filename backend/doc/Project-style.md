Purpose: Outlines naming conventions, folder placements, coding standards, and rules for how code must be structured.

Naming Conventions:
    Use PascalCase for React components (e.g., MyComponent.tsx).
    Use docstrings for every function (describing its purpose and parameters).

Backend Folder Placement:
    Domain-Specific Features (e.g., file mgmt, parsing, comparison) go in \backend\apps.
    Vendor-Specific/External Integrations (e.g., GCS, DB) go in \backend\services.
    Centralized Auth & Role-Based Access goes in \backend\shared\middleware.
    Utility Functions (ID generators, etc.) in \backend\shared\utils.
    Configuration Handling (config.py) in \backend\config.
    Backend Environment Variables in \backend\.env.

Frontend Folder Placement:
    Feature-Specific UI in \frontend\apps.
    Layout Components (header, footer, sidebars) in \frontend\shared\layouts.
    Reusable UI Elements (buttons, modals) in \frontend\shared\components.
    React Context for global state in \frontend\shared\contexts.
    Utilities in \frontend\shared\utils.
    Page-Level Components in \frontend\pages.
    Frontend Environment Variables in \frontend\.env.

## Environment Configuration

### Environment Files
- `.env.template` - Template with all required parameters
- `.env` - Development environment settings
- `.env.integration` - Integration test settings

### Usage
1. Copy `.env.template` to create new environment files
2. Never commit `.env` or `.env.integration`
3. Keep parameters consistent between environments
4. Use different values for development vs testing

### Parameter Naming
- Use UPPERCASE for all environment variables
- Use underscores for word separation
- Group related variables with common prefixes

### Required Parameters
Database:
- DATABASE_PROVIDER: Service provider (e.g., mongodb)
- MONGODB_CONNECTION_STRING: Connection URL
- MONGODB_DATABASE: Database name

Firebase:
- AUTH_PROVIDER: Authentication provider (firebase)
- FIREBASE_PROJECT_ID: Google project ID
- GOOGLE_APPLICATION_CREDENTIALS: Path to credentials

Storage:
- STORAGE_PROVIDER: Storage provider (gcs, s3)
- GCS_BUCKET_NAME: Storage bucket name
- GOOGLE_CLOUD_PROJECT: Must match FIREBASE_PROJECT_ID