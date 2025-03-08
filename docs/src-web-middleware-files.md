---
layout: default
title: Web Middleware Files
parent: Web Interface
nav_order: 4
permalink: /src/web/middleware/files/
---

# Web Middleware Files Documentation

{% include navigation.html %}

## Overview

The Web Middleware Files documentation provides a detailed inventory and analysis of the files in the middleware component of the CreatureBox web interface, focusing on request processing, authentication, security, and other cross-cutting concerns.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

This document catalogs the files within the `src/web/middleware` directory that handle cross-cutting concerns in the web application. Middleware components intercept HTTP requests and responses to provide functionality that applies across multiple routes such as:

- Authentication and authorization
- Request logging and monitoring
- Security protections and headers
- Cross-origin resource sharing (CORS)
- Rate limiting
- Request validation

This documentation serves as a reference for developers working with the middleware layer, explaining the purpose and implementation of each file.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| __init__.py | Python | 0.3 KB | Package initialization |
| auth.py | Python | 2.4 KB | Authentication middleware |
| cors.py | Python | 0.8 KB | Cross-origin resource sharing |
| logging.py | Python | 1.1 KB | Request logging |
| rate_limit.py | Python | 1.3 KB | API rate limiting |
| security.py | Python | 1.6 KB | Security protections |
| validation.py | Python | 1.2 KB | Request validation |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### __init__.py
- **Primary Purpose**: Package initialization and middleware registration
- **Key Functions**:
  * `register_middleware(app)`: Registers all middleware with Flask app
  * `get_middleware_modules()`: Returns list of middleware modules
- **Dependencies**:
  * Flask
- **Technical Notes**: Maintains proper initialization order for dependent middleware

### auth.py
- **Primary Purpose**: Authentication and authorization
- **Key Functions**:
  * `configure_jwt(app)`: Sets up JWT authentication
  * `jwt_error_handler(error)`: Handles JWT errors
  * `identity_handler(payload)`: Resolves user from JWT payload
  * `admin_required(fn)`: Decorator for admin-only routes
  * `get_current_user()`: Retrieves current authenticated user
  * `login_required(fn)`: Decorator for protected routes
- **Dependencies**:
  * Flask-JWT-Extended
  * User database models
- **Technical Notes**: Implements token-based authentication with refresh tokens and role-based authorization

### cors.py
- **Primary Purpose**: Cross-origin resource sharing configuration
- **Key Functions**:
  * `configure_cors(app)`: Sets up CORS for the application
  * `cors_error_handler(error)`: Handles CORS errors
  * `get_allowed_origins()`: Determines allowed origins based on environment
- **Dependencies**:
  * Flask-CORS
  * Configuration settings
- **Technical Notes**: Configures allowed origins, methods, and headers for cross-origin requests

### logging.py
- **Primary Purpose**: Request logging and monitoring
- **Key Functions**:
  * `configure_request_logging(app)`: Sets up request logging
  * `log_request()`: Logs incoming request details
  * `log_response(response)`: Logs outgoing response details
  * `log_error(error)`: Logs request processing errors
  * `get_log_format()`: Determines log format based on environment
- **Dependencies**:
  * Flask logging
  * Python logging module
  * Configuration settings
- **Technical Notes**: Provides detailed logging for debugging and security monitoring

### rate_limit.py
- **Primary Purpose**: API request rate limiting
- **Key Functions**:
  * `configure_rate_limiting(app)`: Sets up rate limiting
  * `rate_limit_decorator(limit, period)`: Decorator for rate-limited routes
  * `ip_limit_key()`: Generates limit key based on IP
  * `user_limit_key()`: Generates limit key based on user ID
  * `handle_rate_limit_exceeded(error)`: Handles rate limit errors
  * `get_rate_limit_storage()`: Configures storage for rate limit data
- **Dependencies**:
  * Flask-Limiter
  * Redis (optional, for distributed rate limiting)
- **Technical Notes**: Different rate limits for authenticated vs. anonymous users

### security.py
- **Primary Purpose**: Web security protections
- **Key Functions**:
  * `configure_security(app)`: Sets up security features
  * `add_security_headers(response)`: Adds security HTTP headers
  * `validate_content_type()`: Validates request content types
  * `csrf_protect()`: CSRF protection for forms
  * `sanitize_input(data)`: Sanitizes user input
  * `xss_protect(fn)`: Decorator for XSS protection
- **Dependencies**:
  * Flask-WTF (for CSRF)
  * Content sanitization libraries
  * Configuration settings
- **Technical Notes**: Implements defense-in-depth security approach

### validation.py
- **Primary Purpose**: Request content validation
- **Key Functions**:
  * `validate_json(schema)`: Decorator for JSON validation
  * `validate_query_params(schema)`: Decorator for query param validation
  * `validation_error_handler(error)`: Handles validation errors
  * `format_validation_errors(errors)`: Formats error messages
  * `load_schema(schema_name)`: Loads schema from file
- **Dependencies**:
  * JSON Schema
  * Marshmallow
  * Schema definition files
- **Technical Notes**: Schema-based validation for API requests with detailed error messages

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Web Core](../web-interface/core.md): Middleware is registered with main application
  * [Web Routes](../web-interface/routes.md): Protects route handlers
  * [Web Services](../web-interface/services.md): Provides authenticated user context
- **Depends On**:
  * Flask middleware framework
  * Authentication libraries
  * User database models
  * [Configuration Settings](../core-components/configuration.md)
- **Used By**:
  * All web requests
  * API clients
  * Web interface

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **JWT Authentication**:
   - **Description**: Securing API endpoints with JWT token authentication.
   - **Example**: 
     ```python
     # In auth.py
     from flask_jwt_extended import JWTManager, create_access_token
     from datetime import timedelta
     
     def configure_jwt(app):
         jwt = JWTManager(app)
         app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
         app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
         
         @jwt.user_loader_callback_loader
         def user_loader_callback(identity):
             return User.query.get(identity)
     
     # In a route file
     @api_blueprint.route('/login', methods=['POST'])
     def login():
         username = request.json.get('username')
         password = request.json.get('password')
         user = User.authenticate(username, password)
         if not user:
             return jsonify({"error": "Invalid credentials"}), 401
         access_token = create_access_token(identity=user.id)
         return jsonify(access_token=access_token)
     ```

2. **Route Protection**:
   - **Description**: Restricting access to authenticated users or specific roles.
   - **Example**: 
     ```python
     # In auth.py
     from functools import wraps
     from flask_jwt_extended import jwt_required, get_jwt_identity
     
     def admin_required(fn):
         @wraps(fn)
         @jwt_required
         def wrapper(*args, **kwargs):
             current_user = get_current_user()
             if not current_user or not current_user.is_admin:
                 return jsonify({"error": "Admin access required"}), 403
             return fn(*args, **kwargs)
         return wrapper
     
     # In a route file
     @api_blueprint.route('/admin/settings', methods=['GET'])
     @admin_required
     def get_admin_settings():
         # Only admins can access this route
         return jsonify(settings=get_all_settings())
     ```

3. **Security Headers**:
   - **Description**: Adding security headers to all responses to mitigate common web vulnerabilities.
   - **Example**: 
     ```python
     # In security.py
     def add_security_headers(response):
         """Add security headers to response"""
         response.headers['Content-Security-Policy'] = "default-src 'self'"
         response.headers['X-Frame-Options'] = 'SAMEORIGIN'
         response.headers['X-XSS-Protection'] = '1; mode=block'
         response.headers['X-Content-Type-Options'] = 'nosniff'
         
         if request.is_secure:
             response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
         
         return response
     
     # In __init__.py
     def register_middleware(app):
         from .security import add_security_headers
         app.after_request(add_security_headers)
     ```

4. **API Rate Limiting**:
   - **Description**: Protecting APIs from abuse by limiting request rates.
   - **Example**: 
     ```python
     # In rate_limit.py
     from flask_limiter import Limiter
     from flask_limiter.util import get_remote_address
     
     limiter = None
     
     def configure_rate_limiting(app):
         global limiter
         limiter = Limiter(
             app,
             key_func=get_remote_address,
             default_limits=["200 per day", "50 per hour"],
             storage_uri="redis://localhost:6379/0"
         )
     
     def rate_limit_decorator(limit, period):
         def decorator(fn):
             return limiter.limit(f"{limit} per {period}")(fn)
         return decorator
     
     # In a route file
     @api_blueprint.route('/gallery/images', methods=['GET'])
     @rate_limit_decorator(100, 'hour')
     def get_gallery_images():
         # This endpoint is limited to 100 requests per hour per IP
         return jsonify(images=get_images())
     ```

</div>
</details>
