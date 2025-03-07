---
layout: default
title: Core Web Components
parent: Web Interface
nav_order: 1
---

# Core Web Components

{% include navigation.html %}

## Overview

The core web components form the foundation of the CreatureBox web interface, providing the application structure, configuration management, error handling, and middleware framework.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The core web files serve as the entry point and foundation for the Flask-based web application of the CreatureBox system. These components are responsible for:

- Creating and configuring the Flask application instance
- Managing application configuration across environments
- Registering routes and extensions
- Setting up error handling and middleware
- Initializing the logging system
- Providing the entry point for the development server

These files establish the framework upon which all other web interface components are built, ensuring a consistent, modular, and maintainable web application.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| app.py | Python | 1.6 KB | Application entry point and factory |
| config.py | Python | 0.9 KB | Configuration management |
| error_handlers.py | Python | 1.2 KB | Centralized error handling |
| middleware.py | Python | 0.8 KB | Request processing middleware |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### app.py
- **Primary Purpose**: Serves as the entry point for the Flask web application
- **Key Functions**:
  * `create_app(env_name='development')`: Application factory that initializes Flask
  * `register_blueprints(app)`: Registers route blueprints with the application
  * `configure_logging(app)`: Sets up application logging
  * `main()`: Entry point when run directly, configures and starts the development server
- **Dependencies**:
  * Flask
  * Blueprints from routes directory
  * Middleware components
  * Error handlers
- **Technical Notes**: Implements the application factory pattern for flexible configuration and testing

### config.py
- **Primary Purpose**: Manages application configuration across environments 
- **Key Functions**:
  * `get_config()`: Retrieves configuration dictionary based on environment
  * `load_environment_variables()`: Loads variables from .env file or environment
  * `configure_app(app, env_name)`: Applies configuration to Flask app
- **Dependencies**:
  * os module
  * dotenv (optional)
- **Technical Notes**: Supports development, testing, and production environments with different settings

### error_handlers.py
- **Primary Purpose**: Centralizes HTTP error handling for the application
- **Key Functions**:
  * `register_error_handlers(app)`: Registers all error handlers with Flask app
  * `handle_400_error(e)`: Handles bad request errors
  * `handle_404_error(e)`: Handles page not found errors
  * `handle_500_error(e)`: Handles server errors
  * `log_error(e)`: Logs error details to application logger
- **Dependencies**:
  * Flask
  * logging module
- **Technical Notes**: Provides consistent error responses in both API and HTML formats based on request type

### middleware.py
- **Primary Purpose**: Implements request/response processing middleware
- **Key Functions**:
  * `configure_middleware(app)`: Sets up all middleware for the application
  * `log_request()`: Before-request handler for logging
  * `add_security_headers(response)`: After-request handler for security headers
- **Dependencies**:
  * Flask
  * Middleware modules from middleware/ directory
- **Technical Notes**: Uses Flask's before_request and after_request hooks for cross-cutting concerns

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [API Routes](./routes.md): API endpoints that use core app
  * [Services](./services.md): Background services used by app
  * [Utilities](./utils.md): Utility functions called by app
  * [Middleware](./middleware.md): Additional middleware components
  * [Static Resources](./static.md): Frontend assets served by app
  * [Tests](./tests.md): Test suite for web application
- **Depends On**:
  * Flask and related libraries
  * [Configuration Module](../core-components/configuration.md): System configuration files
  * [Power Management Module](../core-components/power-management.md): For system power control features
  * [Software Module](../core-components/software-module.md): For camera and system control
- **Used By**:
  * Web browser clients
  * [Deployment](../deployment.md): WSGI server and web server configuration

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Web Application Initialization**:
   - **Description**: Creating and configuring a Flask application with all necessary components.
   - **Example**: 
     ```python
     from src.web.app import create_app
     app = create_app('production')
     # Web application is now ready to serve requests
     ```

2. **Environment-specific Configuration**:
   - **Description**: Loading different settings based on the environment.
   - **Example**: 
     ```python
     app = create_app('development')  # Uses development settings with debug enabled
     # vs
     app = create_app('production')   # Uses production settings with optimized performance
     ```

3. **Consistent Error Handling**:
   - **Description**: Centralized error handling for all routes.
   - **Example**: When a route raises a 404 error, the handle_404_error function returns a JSON response for API requests or renders an error template for browser requests.

4. **Request Processing Pipeline**:
   - **Description**: Setting up a request processing pipeline that logs requests and adds security headers.
   - **Example**: Each incoming request is logged and each outgoing response gets security headers like Content-Security-Policy.

</div>
</details>

## Application Architecture

The web application follows the Flask application factory pattern, which provides several benefits:

1. **Modularity**: Components can be easily added or removed
2. **Testability**: Different configurations can be used for testing
3. **Flexibility**: The application can be configured for different environments

The sequence of application initialization is:

1. `create_app()` is called with environment name
2. Environment-specific configuration is loaded
3. Error handlers are registered
4. Middleware is configured
5. Blueprints (routes) are registered
6. Logging is configured
7. The application is ready to process requests

This core foundation enables the modular web interface that makes the CreatureBox system easy to control and monitor.