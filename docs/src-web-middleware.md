# Web Middleware Module Documentation

{% include navigation.html %}

## Overview

The Web Middleware Module provides authentication, request processing, and security features that handle requests before they reach the route handlers in the CreatureBox web application.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `src/web/middleware` directory contains components that intercept and process HTTP requests before they reach route handlers, and responses before they are sent to clients. This module:

- Implements authentication and authorization
- Applies security headers and protections
- Logs request information
- Validates request content
- Manages cross-origin resource sharing
- Provides rate limiting for API endpoints

Middleware in this module ensures that all requests are properly authenticated, sanitized, and tracked before business logic is executed.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Purpose |
|----------|------|------|---------|
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
- **Dependencies**:
  * Flask-JWT-Extended
  * User models
- **Technical Notes**: Implements token-based authentication with refresh tokens

### cors.py
- **Primary Purpose**: Cross-origin resource sharing configuration
- **Key Functions**:
  * `configure_cors(app)`: Sets up CORS for the application
  * `cors_error_handler(error)`: Handles CORS errors
- **Dependencies**:
  * Flask-CORS
- **Technical Notes**: Configures allowed origins, methods, and headers for cross-origin requests

### logging.py
- **Primary Purpose**: Request logging and monitoring
- **Key Functions**:
  * `configure_request_logging(app)`: Sets up request logging
  * `log_request()`: Logs incoming request details
  * `log_response(response)`: Logs outgoing response details
  * `log_error(error)`: Logs request processing errors
- **Dependencies**:
  * Flask logging
  * Python logging module
- **Technical Notes**: Provides detailed logging for debugging and security monitoring

### rate_limit.py
- **Primary Purpose**: API request rate limiting
- **Key Functions**:
  * `configure_rate_limiting(app)`: Sets up rate limiting
  * `rate_limit_decorator(limit, period)`: Decorator for rate-limited routes
  * `ip_limit_key()`: Generates limit key based on IP
  * `user_limit_key()`: Generates limit key based on user ID
  * `handle_rate_limit_exceeded(error)`: Handles rate limit errors
- **Dependencies**:
  * Flask-Limiter
- **Technical Notes**: Different rate limits for authenticated vs. anonymous users

### security.py
- **Primary Purpose**: Web security protections
- **Key Functions**:
  * `configure_security(app)`: Sets up security features
  * `add_security_headers(response)`: Adds security HTTP headers
  * `validate_content_type()`: Validates request content types
  * `csrf_protect()`: CSRF protection for forms
  * `sanitize_input(data)`: Sanitizes user input
- **Dependencies**:
  * Flask-WTF (for CSRF)
  * Content sanitization libraries
- **Technical Notes**: Implements defense-in-depth security approach

### validation.py
- **Primary Purpose**: Request content validation
- **Key Functions**:
  * `validate_json(schema)`: Decorator for JSON validation
  * `validate_query_params(schema)`: Decorator for query param validation
  * `validation_error_handler(error)`: Handles validation errors
  * `format_validation_errors(errors)`: Formats error messages
- **Dependencies**:
  * JSON Schema
  * Marshmallow
- **Technical Notes**: Schema-based validation for API requests

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Web Core](./src-web.md): Middleware is registered with main application
  * [Web Routes](./src-web-routes.md): Protects route handlers
  * [Web Services](./src-web-services.md): Provides authenticated user context
- **Depends On**:
  * Flask middleware framework
  * Authentication libraries
  * User database models
  * Configuration settings
- **Used By**:
  * All web requests
  * API clients
  * Web interface

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **User Authentication**:
   - **Description**: Authenticating API requests with JWT tokens.
   - **Example**: 
     ```python
     # auth.py middleware implementation
     from flask_jwt_extended import JWTManager, jwt_required
     from functools import wraps
     
     def configure_jwt(app):
         jwt = JWTManager(app)
         
         @jwt.user_identity_loader
         def user_identity_lookup(user):
             return user.id
             
         @jwt.user_loader_callback_loader
         def user_loader_callback(identity):
             return User.query.get(identity)
     
     def admin_required(fn):
         @wraps(fn)
         @jwt_required
         def wrapper(*args, **kwargs):
             current_user = get_current_user()
             if not current_user or not current_user.is_admin:
                 return jsonify({"error": "Admin access required"}), 403
             return fn(*args, **kwargs)
         return wrapper
     ```

2. **Request Rate Limiting**:
   - **Description**: Preventing API abuse through rate limits.
   - **Example**: 
     ```python
     # rate_limit.py middleware implementation
     from flask_limiter import Limiter
     from flask_limiter.util import get_remote_address
     
     limiter = None
     
     def configure_rate_limiting(app):
         global limiter
         limiter = Limiter(
             app,
             key_func=get_remote_address,
             default_limits=["200 per day", "50 per hour"]
         )
         
         # Higher limits for authenticated users
         @app.before_request
         def update_rate_limit_key():
             if current_user.is_authenticated:
                 limiter.key_func = user_limit_key
             else:
                 limiter.key_func = get_remote_address
                 
     def camera_capture_limit():
         """Limit camera capture to 10 per hour"""
         return "10 per hour"
     ```

3. **Security Headers**:
   - **Description**: Adding security headers to prevent common web vulnerabilities.
   - **Example**: 
     ```python
     # security.py middleware implementation
     def add_security_headers(response):
         """Add security headers to response"""
         # Content Security Policy
         response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data:; script-src 'self'"
         
         # Prevent click-jacking
         response.headers['X-Frame-Options'] = 'SAMEORIGIN'
         
         # XSS protection
         response.headers['X-XSS-Protection'] = '1; mode=block'
         
         # Prevent MIME type sniffing
         response.headers['X-Content-Type-Options'] = 'nosniff'
         
         # Force HTTPS
         response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
         
         return response
     ```

4. **Request Validation**:
   - **Description**: Validating API request parameters.
   - **Example**: 
     ```python
     # validation.py middleware implementation
     import jsonschema
     from functools import wraps
     from flask import request, jsonify
     
     def validate_json(schema):
         """Validate JSON request against schema"""
         def decorator(fn):
             @wraps(fn)
             def wrapper(*args, **kwargs):
                 try:
                     if not request.is_json:
                         return jsonify({"error": "Request must be JSON"}), 400
                         
                     data = request.get_json()
                     jsonschema.validate(data, schema)
                     return fn(*args, **kwargs)
                 except jsonschema.exceptions.ValidationError as e:
                     return jsonify({"error": "Validation error", "message": str(e)}), 400
             return wrapper
         return decorator
     ```

</div>
</details>
