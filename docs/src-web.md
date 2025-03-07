# Web Interface Module Documentation

{% include navigation.html %}

## Overview

The Web Interface module provides a browser-based control panel for the CreatureBox system, allowing users to configure settings, manage photos, and control system operations through an intuitive interface.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `src/web` directory contains the complete web application component of the CreatureBox system. It provides a modular Flask-based web interface for controlling and monitoring the CreatureBox wildlife monitoring hardware. This component enables users to:

- Configure camera settings
- Capture photos on demand
- View the photo gallery
- Manage file storage
- Control system power and scheduling
- Monitor system status

The web interface is accessible both locally on the device network and remotely when properly configured for external access.

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
  * [Web Routes](./src-web-routes.md): API endpoints that use core app
  * [Web Services](./src-web-services.md): Background services used by app
  * [Web Utilities](./src-web-utils.md): Utility functions called by app
  * [Web Middleware](./src-web-middleware.md): Additional middleware components
  * [Web Static](./src-web-static.md): Frontend assets served by app
  * [Web Tests](./src-web-tests.md): Test suite for web application
- **Depends On**:
  * Flask and related libraries
  * [Configuration Module](./src-config.md): System configuration files
  * [Power Module](./src-power.md): For system power control features
  * [Software Module](./src-software.md): For camera and system control
- **Used By**:
  * Web browser clients
  * [Deployment](./deployment.md): WSGI server and web server configuration

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
