# Web Routes Module Documentation

{% include navigation.html %}

## Overview

The Web Routes Module defines all API endpoints and page handlers for the CreatureBox web interface, organizing endpoints into logical blueprints for different system functionalities.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `src/web/routes` directory contains Flask blueprints that define all the API endpoints and page handlers for the CreatureBox web interface. This module:

- Provides RESTful API endpoints for system control
- Defines page routes for the web interface
- Handles request processing and validation
- Maps URL patterns to controller functions
- Organizes endpoints into logical functional groups

Routes are grouped into blueprints based on functionality, such as camera control, system management, gallery access, and configuration.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Purpose |
|----------|------|------|---------|
| __init__.py | Python | 0.2 KB | Blueprint initialization |
| api.py | Python | 1.8 KB | RESTful API endpoint definitions |
| auth.py | Python | 1.4 KB | Authentication routes |
| camera.py | Python | 2.2 KB | Camera control endpoints |
| config.py | Python | 1.6 KB | Configuration management routes |
| gallery.py | Python | 2.4 KB | Photo gallery access |
| system.py | Python | 1.9 KB | System management endpoints |
| views.py | Python | 1.7 KB | Web UI page routes |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### __init__.py
- **Primary Purpose**: Package initialization and blueprint registration
- **Key Functions**:
  * `get_blueprints()`: Returns list of all route blueprints
- **Dependencies**:
  * Flask Blueprint system
- **Technical Notes**: Simplifies blueprint registration in main app.py

### api.py
- **Primary Purpose**: Core API endpoint definitions
- **Key Routes**:
  * `GET /api/status`: System status information
  * `GET /api/version`: Software version details
  * `POST /api/reboot`: Trigger system reboot
  * `POST /api/shutdown`: Trigger system shutdown
- **Dependencies**:
  * System utilities module
  * Authentication middleware
- **Technical Notes**: All endpoints return JSON responses, require API authentication

### auth.py
- **Primary Purpose**: User authentication endpoints
- **Key Routes**:
  * `POST /auth/login`: User login
  * `POST /auth/logout`: User logout
  * `GET /auth/status`: Authentication status
  * `POST /auth/reset-password`: Password reset
- **Dependencies**:
  * Authentication service
  * User database models
- **Technical Notes**: Implements JWT-based authentication with refresh tokens

### camera.py
- **Primary Purpose**: Camera control functionality
- **Key Routes**:
  * `POST /api/camera/capture`: Take photo
  * `GET /api/camera/preview`: Live camera preview
  * `GET /api/camera/settings`: Current camera settings
  * `POST /api/camera/settings`: Update camera settings
  * `POST /api/camera/attraction`: Toggle attraction mode
- **Dependencies**:
  * Camera utility module
  * Configuration service
- **Technical Notes**: Provides both synchronous and asynchronous capture modes

### config.py
- **Primary Purpose**: System configuration management
- **Key Routes**:
  * `GET /api/config/settings`: Get all system settings
  * `POST /api/config/settings`: Update system settings
  * `GET /api/config/backup`: Download configuration backup
  * `POST /api/config/restore`: Restore from backup
  * `GET /api/config/defaults`: Reset to default settings
- **Dependencies**:
  * Configuration service
  * File utilities
- **Technical Notes**: Validates all configuration changes before applying

### gallery.py
- **Primary Purpose**: Photo gallery access and management
- **Key Routes**:
  * `GET /api/gallery/recent`: Get recent photos
  * `GET /api/gallery/photo/:id`: Get specific photo
  * `DELETE /api/gallery/photo/:id`: Delete photo
  * `POST /api/gallery/photo/:id/favorite`: Mark photo as favorite
  * `GET /api/gallery/download`: Download photo archive
- **Dependencies**:
  * Storage service
  * File utilities
- **Technical Notes**: Supports pagination, filtering, and image transformations

### system.py
- **Primary Purpose**: System operations management
- **Key Routes**:
  * `GET /api/system/info`: System information
  * `GET /api/system/logs`: System logs
  * `POST /api/system/update`: Software update
  * `GET /api/system/storage`: Storage status
  * `POST /api/system/backup`: Create system backup
- **Dependencies**:
  * System utilities
  * File system access
- **Technical Notes**: Some endpoints require admin privileges

### views.py
- **Primary Purpose**: Web UI page routes
- **Key Routes**:
  * `GET /`: Homepage
  * `GET /gallery`: Photo gallery page
  * `GET /settings`: Settings page
  * `GET /system`: System management page
  * `GET /login`: Login page
- **Dependencies**:
  * Template rendering
  * Authentication service
- **Technical Notes**: Renders HTML templates for browser interface

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Web Core](./src-web.md): Routes are registered with main application
  * [Web Services](./src-web-services.md): Routes use services for business logic
  * [Web Middleware](./src-web-middleware.md): Request processing before routes
  * [Web Utilities](./src-web-utils.md): Helper functions used by routes
- **Depends On**:
  * Flask framework
  * Authentication system
  * [Configuration Module](./src-config.md): System settings access
  * [Software Module](./src-software.md): System control functionality
- **Used By**:
  * Web browser clients
  * Mobile applications (via API)
  * System monitoring tools

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Camera Control via API**:
   - **Description**: Remote triggering of camera capture through API.
   - **Example**: 
     ```python
     # API route for camera capture
     @camera_bp.route('/api/camera/capture', methods=['POST'])
     @jwt_required
     def capture_image():
         # Get capture parameters
         params = request.get_json() or {}
         delay = params.get('delay', 0)
         count = params.get('count', 1)
         interval = params.get('interval', 1)
         
         # Validate parameters
         if count > 10:
             return jsonify({"error": "Cannot capture more than 10 images at once"}), 400
             
         # Trigger capture
         try:
             job_id = camera_service.schedule_capture(delay, count, interval)
             return jsonify({"success": True, "job_id": job_id})
         except Exception as e:
             return jsonify({"error": str(e)}), 500
     ```

2. **User Authentication**:
   - **Description**: User login and authentication process.
   - **Example**: 
     ```python
     # User login route
     @auth_bp.route('/auth/login', methods=['POST'])
     def login():
         # Get credentials
         credentials = request.get_json()
         username = credentials.get('username')
         password = credentials.get('password')
         
         # Validate input
         if not username or not password:
             return jsonify({"error": "Missing credentials"}), 400
             
         # Authenticate user
         try:
             user = auth_service.authenticate(username, password)
             if user:
                 access_token = create_access_token(identity=user.id)
                 refresh_token = create_refresh_token(identity=user.id)
                 return jsonify(access_token=access_token, refresh_token=refresh_token)
             else:
                 return jsonify({"error": "Invalid credentials"}), 401
         except Exception as e:
             return jsonify({"error": str(e)}), 500
     ```

3. **Configuration Management**:
   - **Description**: Updating system configuration through the web interface.
   - **Example**: 
     ```python
     # Update configuration settings
     @config_bp.route('/api/config/settings', methods=['POST'])
     @jwt_required
     @admin_required
     def update_settings():
         # Get settings
         new_settings = request.get_json()
         
         # Validate settings
         validation_errors = config_service.validate_settings(new_settings)
         if validation_errors:
             return jsonify({"error": "Invalid settings", "details": validation_errors}), 400
             
         # Apply settings
         try:
             config_service.update_settings(new_settings)
             return jsonify({"success": True})
         except Exception as e:
             return jsonify({"error": str(e)}), 500
     ```

4. **Photo Gallery Access**:
   - **Description**: Accessing and managing captured photos.
   - **Example**: 
     ```python
     # Get recent photos with pagination
     @gallery_bp.route('/api/gallery/recent', methods=['GET'])
     @jwt_required
     def get_recent_photos():
         # Parse query parameters
         page = request.args.get('page', 1, type=int)
         per_page = request.args.get('per_page', 20, type=int)
         date_from = request.args.get('from')
         date_to = request.args.get('to')
         
         # Apply limits
         per_page = min(per_page, 50)  # Maximum 50 per page
         
         # Get photos from storage service
         photos, total = gallery_service.get_photos(
             page=page,
             per_page=per_page,
             date_from=date_from,
             date_to=date_to
         )
         
         # Return paginated results
         return jsonify({
             "photos": photos,
             "total": total,
             "page": page,
             "per_page": per_page,
             "pages": (total + per_page - 1) // per_page
         })
     ```

</div>
</details>
