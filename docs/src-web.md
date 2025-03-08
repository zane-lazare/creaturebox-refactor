---
layout: default
title: Web Interface Module
nav_order: 3
permalink: /src/web/
---

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
| config.py | Python | 0.9 KB | Web app configuration management |
| error_handlers.py | Python | 1.2 KB | Centralized error handling |
| middleware.py | Python | 0.8 KB | Request processing middleware |
| wsgi.py | Python | 0.4 KB | WSGI entry point for production |
| __init__.py | Python | 0.2 KB | Module initialization |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### app.py
- **Primary Purpose**: Main entry point for the Flask web application
- **Key Functions**:
  * `create_app(env_name='development')`: Application factory that initializes Flask
  * `register_blueprints(app)`: Registers route blueprints with the application
  * `configure_logging(app)`: Sets up application logging
  * `main()`: Entry point when run directly, starts the development server
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
- **Technical Notes**: Provides consistent error responses in both API and HTML formats

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

### wsgi.py
- **Primary Purpose**: WSGI entry point for production deployment
- **Key Functions**:
  * Imports and creates the Flask application object
  * Configures it for production environment
  * Provides the application variable for WSGI servers like Gunicorn
- **Dependencies**:
  * app.py (create_app function)
- **Technical Notes**: Minimal file that focuses on production deployment concerns only

### __init__.py
- **Primary Purpose**: Marks the directory as a Python package
- **Key Functions**:
  * Package initialization
  * Version definition
  * Package-level imports
- **Dependencies**: None
- **Technical Notes**: Keeps minimal code to avoid circular dependencies

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
  * Flask framework
  * [Configuration Module](./core-components/configuration.md): For system settings
  * [Software Module](./core-components/software-module.md): For camera functionality
  * [Power Management](./core-components/power-management.md): For system power control
- **Used By**:
  * Web browser clients
  * [Deployment](./deployment.md): For production deployment
  * Mobile apps (if applicable)

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Application Initialization**:
   - **Description**: Starting up the Flask application with appropriate configuration.
   - **Example**: 
     ```python
     # Development server startup
     from src.web.app import create_app
     
     app = create_app('development')
     app.run(host='0.0.0.0', port=5000, debug=True)
     ```

2. **Production Deployment**:
   - **Description**: Deploying the application with a WSGI server.
   - **Example**: 
     ```bash
     # Command line using Gunicorn
     gunicorn --workers=4 --bind=0.0.0.0:8000 src.web.wsgi:application
     ```

3. **Environment-specific Configuration**:
   - **Description**: Loading different settings based on the environment.
   - **Example**: 
     ```python
     app_dev = create_app('development')  # Debug enabled, development database
     app_test = create_app('testing')     # Test database, no email sending
     app_prod = create_app('production')  # Production optimized, error emails
     ```

4. **Consistent Error Handling**:
   - **Description**: Providing tailored error responses based on request type.
   - **Example**: 
     ```python
     # Example of how errors are handled
     from flask import request, jsonify, render_template
     
     def handle_404_error(e):
         if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
            # API request
            return jsonify({"error": "Not found", "code": 404}), 404
         # Browser request
         return render_template("errors/404.html"), 404
     ```

5. **Request Processing Pipeline**:
   - **Description**: Setting up a request processing pipeline that logs requests and adds security headers.
   - **Example**: Each incoming request is logged and each outgoing response gets security headers like Content-Security-Policy.

</div>
</details>
