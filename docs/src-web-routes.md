---
layout: default
title: Web Routes
parent: Web Interface
nav_order: 2
permalink: /src/web/routes/
---

# Web Routes Documentation

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

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| __init__.py | Python | 0.2 KB | Blueprint initialization |
| api.py | Python | 1.8 KB | RESTful API endpoint definitions |
| auth.py | Python | 1.4 KB | Authentication routes |
| camera.py | Python | 2.2 KB | Camera control endpoints |
| config.py | Python | 1.6 KB | Configuration management routes |
| gallery.py | Python | 2.4 KB | Photo gallery access |
| system.py | Python | 1.9 KB | System management endpoints |
| views.py | Python | 1.7 KB | Web UI page routes |
| scheduler.py | Python | 1.5 KB | Task scheduling endpoints |
| storage.py | Python | 1.8 KB | Storage management routes |

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

### scheduler.py
- **Primary Purpose**: Task scheduling management
- **Key Routes**:
  * `GET /api/scheduler/tasks`: List scheduled tasks
  * `POST /api/scheduler/tasks`: Create new scheduled task
  * `DELETE /api/scheduler/tasks/:id`: Delete scheduled task
  * `PUT /api/scheduler/tasks/:id`: Update scheduled task
  * `GET /api/scheduler/history`: View task execution history
- **Dependencies**:
  * Scheduler service
  * Task queue system
- **Technical Notes**: Supports recurring and one-time scheduled operations

### storage.py
- **Primary Purpose**: Storage management functionality
- **Key Routes**:
  * `GET /api/storage/status`: Storage space overview
  * `POST /api/storage/cleanup`: Trigger storage cleanup
  * `GET /api/storage/directories`: List storage directories
  * `POST /api/storage/backup`: Export storage backup
  * `POST /api/storage/restore`: Restore from backup
- **Dependencies**:
  * Storage service
  * File system utilities
- **Technical Notes**: Handles quota management and storage optimization

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Web Interface](../web-interface/core.md): Core web application
  * [Web Interface Routes](../web-interface/routes.md): Comprehensive documentation
  * [Web Services](../web-interface/services.md): Business logic called by routes
  * [Web Middleware](../web-interface/middleware.md): Request processing before routes
  * [Web Utilities](../web-interface/utils.md): Helper functions used by routes
- **Depends On**:
  * Flask framework
  * Authentication system
  * [Configuration](../core-components/configuration.md): System settings access
  * [Software Module](../core-components/software-module.md): System control functionality
- **Used By**:
  * Web browser clients
  * Mobile applications (via API)
  * System monitoring tools
  * 3rd party integrations
  * Automated scripts

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

5. **Task Scheduling**:
   - **Description**: Creating and managing scheduled tasks.
   - **Example**: 
     ```python
     # Create a new scheduled task
     @scheduler_bp.route('/api/scheduler/tasks', methods=['POST'])
     @jwt_required
     def create_scheduled_task():
         # Get task details
         task_data = request.get_json()
         task_type = task_data.get('type')
         schedule = task_data.get('schedule')
         parameters = task_data.get('parameters', {})
         
         # Validate input
         if not task_type or not schedule:
             return jsonify({"error": "Missing required fields"}), 400
             
         # Create task
         try:
             task_id = scheduler_service.create_task(
                 task_type=task_type,
                 schedule=schedule,
                 parameters=parameters,
                 user_id=get_jwt_identity()
             )
             return jsonify({"success": True, "task_id": task_id})
         except ValueError as e:
             return jsonify({"error": str(e)}), 400
         except Exception as e:
             return jsonify({"error": "Failed to create task: " + str(e)}), 500
     ```

</div>
</details>

## API Design Principles

The Web Routes module follows these API design principles:

1. **RESTful Design**: Resources are accessed via standard HTTP methods (GET, POST, PUT, DELETE)
2. **Authentication**: All API endpoints use JWT authentication for security
3. **Validation**: Input validation occurs before processing any request
4. **Response Consistency**: All responses use consistent JSON formatting
5. **Error Handling**: Clear error messages and appropriate HTTP status codes
6. **Pagination**: List endpoints support pagination for large result sets
7. **Filtering**: Resource collections can be filtered via query parameters
8. **Versioning**: API is versioned to support backward compatibility
9. **Rate Limiting**: Requests are rate-limited to prevent abuse
10. **Documentation**: All endpoints include OpenAPI documentation for discoverability
