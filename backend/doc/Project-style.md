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