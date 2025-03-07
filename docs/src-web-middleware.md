# src/web/middleware Directory Documentation

## Directory Purpose
The `src/web/middleware` directory contains components that intercept and process HTTP requests and responses in the CreatureBox web application. These middleware modules provide cross-cutting functionality such as authentication, request logging, security enforcement, and error handling. By implementing the middleware pattern, these components separate core application logic from supporting infrastructure concerns, enhancing security, maintainability, and performance of the web interface.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| __init__.py | Python | 0.2 KB | Package initialization |
| auth.py | Python | 1.4 KB | Authentication middleware |

## Detailed File Descriptions

### __init__.py
- **Primary Purpose**: Initializes the middleware package and provides package-level utilities
- **Key Functions**:
  * `init_middleware()`: Initializes package-level resources
  * `register_middleware(app)`: Registers all middleware with Flask application
- **Dependencies**:
  * Flask
  * Other middleware modules in the package
- **Technical Notes**: 
  * Uses Flask's before_request and after_request hooks
  * Maintains clean import structure
  * Provides centralized middleware registration

### auth.py
- **Primary Purpose**: Implements authentication and authorization for the web application
- **Key Functions**:
  * `AuthMiddleware` class: Core authentication middleware implementation
  * `configure_auth(app, config)`: Configures authentication settings
  * `authenticate_request()`: Before-request handler for validation
  * `get_current_user()`: Retrieves authenticated user information
  * `require_auth(roles=None)`: Decorator for route-level authorization
  * `generate_token(user_id, expiry=None)`: Creates authentication tokens
  * `validate_token(token)`: Validates authentication tokens
- **Dependencies**:
  * Flask
  * JWT (JSON Web Tokens)
  * werkzeug.security (for password hashing)
  * src/config/controls.txt (for auth settings)
- **Technical Notes**: 
  * Implements stateless JWT-based authentication
  * Supports role-based access control
  * Includes token expiration and refresh
  * Securely handles credentials with proper hashing
  * Provides login rate limiting for security

## Relationship Documentation
- **Related To**:
  * src/web/app.py (uses middleware during initialization)
  * src/web/middleware.py (registers middleware components)
- **Depends On**:
  * Flask framework
  * Authentication libraries
  * src/config/ (for configuration settings)
- **Used By**:
  * All routes requiring authentication
  * Web interface front-end (indirectly)
  * API clients

## Use Cases
1. **User Authentication**:
   - **Implementation**: The auth.py middleware validates user credentials and generates secure tokens.
   - **Example**:
     ```python
     # In routes/users.py
     @bp.route('/login', methods=['POST'])
     def login():
         username = request.json.get('username')
         password = request.json.get('password')
         
         # Validate credentials
         if not validate_credentials(username, password):
             return jsonify({'error': 'Invalid credentials'}), 401
         
         # Generate token using auth middleware
         from src.web.middleware.auth import generate_token
         user_id = get_user_id(username)
         token = generate_token(user_id)
         
         return jsonify({'token': token})
     ```

2. **Route Authorization**:
   - **Implementation**: The auth.py middleware provides decorators for enforcing access control.
   - **Example**:
     ```python
     # In routes/admin.py
     from src.web.middleware.auth import require_auth
     
     @bp.route('/admin/settings', methods=['GET'])
     @require_auth(roles=['admin'])
     def admin_settings():
         # Only accessible to users with 'admin' role
         return jsonify(get_admin_settings())
     
     @bp.route('/api/camera/settings', methods=['GET'])
     @require_auth(roles=['admin', 'operator'])
     def camera_settings():
         # Accessible to users with either 'admin' or 'operator' role
         return jsonify(get_camera_settings())
     ```

3. **Global Authentication Enforcement**:
   - **Implementation**: The auth middleware intercepts requests to enforce authentication across all protected routes.
   - **Example**:
     ```python
     # In middleware/auth.py
     def authenticate_request():
         # Public paths that don't require authentication
         public_paths = [
             '/api/login',
             '/api/public',
             '/static/'
         ]
         
         # Skip authentication for public paths
         for path in public_paths:
             if request.path.startswith(path):
                 return
         
         # Check for and validate token
         token = request.headers.get('Authorization', '').replace('Bearer ', '')
         if not token:
             abort(401, 'Authentication required')
         
         # Validate token and attach user to request
         user = validate_token(token)
         if not user:
             abort(401, 'Invalid or expired token')
         
         # Store user in request context for later use
         g.user = user
     
     # In app.py during initialization
     app.before_request(authenticate_request)
     ```

4. **Secure Token Management**:
   - **Implementation**: The auth middleware implements secure token generation and validation.
   - **Example**:
     ```python
     # In middleware/auth.py
     def generate_token(user_id, expiry=None):
         # Default expiry time of 24 hours if not specified
         if not expiry:
             expiry = datetime.utcnow() + timedelta(hours=24)
         
         # Create payload with user ID and expiration
         payload = {
             'sub': user_id,
             'exp': expiry,
             'iat': datetime.utcnow(),
             'jti': str(uuid.uuid4())  # Unique token ID
         }
         
         # Sign with secret key
         secret_key = current_app.config['JWT_SECRET_KEY']
         token = jwt.encode(payload, secret_key, algorithm='HS256')
         
         # Record token in active tokens store
         record_active_token(payload['jti'], user_id, expiry)
         
         return token
     
     def validate_token(token):
         try:
             # Verify signature and decode
             secret_key = current_app.config['JWT_SECRET_KEY']
             payload = jwt.decode(token, secret_key, algorithms=['HS256'])
             
             # Check if token has been revoked
             if is_token_revoked(payload['jti']):
                 return None
             
             # Get user details
             user_id = payload['sub']
             user = get_user_by_id(user_id)
             
             return user
         except jwt.ExpiredSignatureError:
             # Token has expired
             return None
         except jwt.InvalidTokenError:
             # Token is invalid
             return None
     ```
