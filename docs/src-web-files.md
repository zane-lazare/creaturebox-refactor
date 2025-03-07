# src/web Directory Documentation

## Core Application Files

### app.py
- **Purpose**: Primary Flask application entry point
- **Functionality**: Web application initialization and routing

### config.py
- **Purpose**: Web application configuration management
- **Functionality**: Environment and settings configuration

### error_handlers.py
- **Purpose**: Centralized error handling
- **Functionality**: HTTP error management and logging

### middleware.py
- **Purpose**: Request/response processing middleware
- **Functionality**: Pre and post-processing of web requests

## Subdirectories

### middleware/
- **Files**:
  * `__init__.py`: Package initialization
  * `auth.py`: Authentication and authorization mechanisms

### routes/
- **Purpose**: API endpoint definitions
- **Functionality**: Route mapping and request handling

### services/
- **Purpose**: Business logic implementations
- **Functionality**: Core application services

### static/
- **Purpose**: Static web resources
- **Functionality**: CSS, JavaScript, images

### tests/
- **Purpose**: Web application test suite
- **Functionality**: Comprehensive testing infrastructure

### utils/
- **Purpose**: Utility functions and helpers
- **Functionality**: Cross-cutting support functions
