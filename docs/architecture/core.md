# Core Module (`mcp_core`)

The `mcp_core` module is the heart of the application. It contains the business logic and defines the interfaces for data access.

## Key Components

- **Models**: Pydantic models defining the data structures (e.g., `Context`, `Tool`, `Message`).
- **Repository**: Abstract base classes for data access, allowing for different storage implementations (in-memory, database, etc.).
- **Services**: Business logic layers that coordinate operations between repositories and other components.
