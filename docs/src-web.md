# src/web Directory Documentation

## Directory Purpose
The `src/web` directory contains the complete web application component of the CreatureBox system. It provides a modular Flask-based web interface for controlling and monitoring the CreatureBox wildlife monitoring hardware. This component enables users to configure camera settings, capture photos, view the gallery, manage storage, and control system functions through an intuitive browser interface, accessible both locally and remotely when configured.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| app.py | Python | 1.6 KB | Application entry point and factory |
| config.py | Python | 0.9 KB | Configuration management |
| error_handlers.py | Python | 1.2 KB | Centralized error handling |
| middleware.py | Python | 0.8 KB | Request processing middleware |

## Detailed File Descriptions

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

## Relationship Documentation
- **Related To**:
  * src/web/routes/ (API endpoints that use core app)
  * src/web/services/ (Background services used by app)
  * src/web/utils/ (Utility functions called by app)
  * src/web/middleware/ (Additional middleware components)
  * src/web/static/ (Frontend assets served by app)
  * src/web/tests/ (Test suite for web application)
- **Depends On**:
  * Flask and related libraries
  * src/config/ (System configuration files)
  * src/power/ (For system power control features)
  * src/software/ (For camera and system control)
- **Used By**:
  * Web browser clients
  * deployment/gunicorn.conf.py (WSGI server configuration)
  * deployment/nginx.conf (Web server configuration)

## Use Cases
1. **Web Application Initialization**:
   - **Implementation**: The app.py file implements the application factory pattern, creating and configuring a Flask application with all necessary components.
   - **Example**: 
     ```python
     from src.web.app import create_app
     app = create_app('production')
     # Web application is now ready to serve requests
     ```

2. **Environment-specific Configuration**:
   - **Implementation**: The config.py file loads different settings based on the environment.
   - **Example**: 
     ```python
     app = create_app('development')  # Uses development settings with debug enabled
     # vs
     app = create_app('production')   # Uses production settings with optimized performance
     ```

3. **Consistent Error Handling**:
   - **Implementation**: error_handlers.py provides centralized error handling for all routes.
   - **Example**: When a route raises a 404 error, the handle_404_error function returns a JSON response for API requests or renders an error template for browser requests.

4. **Request Processing Pipeline**:
   - **Implementation**: middleware.py sets up a request processing pipeline that logs requests and adds security headers.
   - **Example**: Each incoming request is logged and each outgoing response gets security headers like Content-Security-Policy.
