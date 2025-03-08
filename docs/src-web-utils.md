---
layout: default
title: Web Utilities
parent: Web Interface
nav_order: 7
permalink: /src/web/utils/
---

# Web Utilities Documentation

{% include navigation.html %}

## Overview

The Web Utilities Module provides helper functions and reusable components that support the CreatureBox web application, offering camera interfaces, file management, system operations, and common utility functions.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `src/web/utils` directory contains utility functions and helper components that are used throughout the CreatureBox web application. This module provides:

- Camera control interfaces for web components
- File management utilities
- System operation wrappers
- Date and time processing
- Data validation and transformation
- Common helper functions for web routes and services

These utilities encapsulate implementation details and provide clean, reusable interfaces for common operations, improving code maintainability and reducing duplication.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| __init__.py | Python | 0.2 KB | Package initialization |
| camera.py | Python | 2.4 KB | Camera interfaces |
| files.py | Python | 1.8 KB | File operations |
| system.py | Python | 2.1 KB | System interaction |
| date_utils.py | Python | 1.2 KB | Date/time utilities |
| validators.py | Python | 1.5 KB | Data validation |
| formatters.py | Python | 0.9 KB | Data formatting |
| image_utils.py | Python | 1.6 KB | Image processing utilities |
| security.py | Python | 1.3 KB | Security helper functions |
| network.py | Python | 1.7 KB | Network operations |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### __init__.py
- **Primary Purpose**: Package initialization
- **Key Functions**:
  * Exports common utility functions
- **Dependencies**: None
- **Technical Notes**: Only used for package identification

### camera.py
- **Primary Purpose**: Camera control interfaces
- **Key Functions**:
  * `initialize_camera()`: Set up camera with settings
  * `capture_image(options)`: Take photo with specified parameters
  * `start_preview()`: Begin camera preview stream
  * `stop_preview()`: End camera preview
  * `adjust_settings(settings)`: Change camera parameters
  * `get_supported_modes()`: List available camera modes
  * `set_attraction_mode(enable)`: Control wildlife attraction features
- **Dependencies**:
  * Hardware camera drivers
  * Camera libraries (picamera, gphoto)
  * Camera-specific utilities
- **Technical Notes**: Abstract interface supporting multiple camera types

### files.py
- **Primary Purpose**: File operations
- **Key Functions**:
  * `safe_filename(original)`: Create safe filename
  * `get_file_type(path)`: Detect file type
  * `list_directory(path, filter)`: List directory contents
  * `create_directory(path)`: Create directory if not exists
  * `get_file_info(path)`: Get metadata for file
  * `calculate_directory_size(path)`: Calculate total directory size
  * `find_duplicate_images(path)`: Find similar/duplicate images
- **Dependencies**:
  * File system access
  * File type detection libraries
- **Technical Notes**: Handles error conditions and edge cases

### system.py
- **Primary Purpose**: System operation interfaces
- **Key Functions**:
  * `get_system_info()`: Retrieve system statistics
  * `get_memory_usage()`: Get memory utilization
  * `get_disk_usage(path)`: Get storage utilization
  * `get_cpu_temperature()`: Measure CPU temperature
  * `execute_command(command)`: Run system command safely
  * `reboot_system()`: Trigger system reboot
  * `shutdown_system()`: Trigger system shutdown
  * `get_network_info()`: Get network interface details
- **Dependencies**:
  * System command execution
  * Hardware interfaces
  * OS-specific libraries
- **Technical Notes**: Implements safe execution patterns for system commands

### date_utils.py
- **Primary Purpose**: Date and time utilities
- **Key Functions**:
  * `format_timestamp(timestamp, format)`: Format timestamp for display
  * `parse_date_string(string, format)`: Parse date from string
  * `get_time_difference(start, end)`: Calculate time difference
  * `is_night_time()`: Determine if current time is night
  * `get_sunrise_sunset()`: Get sunrise/sunset times
  * `get_local_timezone()`: Get system timezone
- **Dependencies**:
  * Python datetime module
  * Timezone libraries
- **Technical Notes**: Handles timezone awareness properly

### validators.py
- **Primary Purpose**: Data validation
- **Key Functions**:
  * `validate_email(email)`: Validate email format
  * `validate_ip_address(ip)`: Validate IP address format
  * `validate_settings(settings, schema)`: Validate settings against schema
  * `validate_file_upload(file, allowed_types)`: Validate uploaded file
  * `sanitize_html(content)`: Clean HTML content
  * `is_valid_path(path)`: Check path for validity/security
- **Dependencies**:
  * Validation libraries
  * Schema validation
- **Technical Notes**: Used for input validation and security

### formatters.py
- **Primary Purpose**: Data formatting
- **Key Functions**:
  * `format_file_size(size)`: Format bytes to human-readable
  * `format_duration(seconds)`: Format seconds to HH:MM:SS
  * `truncate_text(text, length)`: Truncate text with ellipsis
  * `format_json(data, pretty)`: Format JSON data
  * `strip_html(html)`: Remove HTML tags
  * `pluralize(noun, count)`: Correctly pluralize words
- **Dependencies**: None
- **Technical Notes**: Simple pure functions for formatting

### image_utils.py
- **Primary Purpose**: Image processing utilities
- **Key Functions**:
  * `create_thumbnail(image_path, size)`: Generate image thumbnail
  * `add_watermark(image, text)`: Add text watermark to image
  * `adjust_image(image, brightness, contrast)`: Adjust image properties
  * `detect_motion(image1, image2)`: Compare images for motion
  * `crop_image(image, dimensions)`: Crop image to specified dimensions
- **Dependencies**:
  * Pillow/PIL library
  * OpenCV (for motion detection)
- **Technical Notes**: Optimized for embedded hardware performance

### security.py
- **Primary Purpose**: Security helper functions
- **Key Functions**:
  * `generate_token()`: Create secure random token
  * `hash_password(password)`: Securely hash password
  * `verify_password(password, hash)`: Verify password against hash
  * `encrypt_data(data, key)`: Encrypt sensitive data
  * `decrypt_data(encrypted, key)`: Decrypt data
  * `generate_secure_filename()`: Create secure random filename
- **Dependencies**:
  * Cryptography libraries
  * Password hashing libraries
- **Technical Notes**: Implements security best practices

### network.py
- **Primary Purpose**: Network operations
- **Key Functions**:
  * `check_connectivity()`: Test internet connection
  * `download_file(url, destination)`: Download remote file
  * `get_local_ip()`: Get device IP address
  * `scan_network()`: Discover devices on network
  * `test_bandwidth()`: Measure connection speed
  * `upload_file(file, url)`: Upload file to remote server
- **Dependencies**:
  * Networking libraries
  * Request libraries
- **Technical Notes**: Handles connection errors gracefully

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Web Interface](../web-interface/core.md): Core web application
  * [Web Interface Utils](../web-interface/utils.md): Comprehensive documentation
  * [Web Routes](../web-interface/routes.md): Used by route handlers
  * [Web Services](../web-interface/services.md): Used by business logic services
  * [Web Tests](../web-interface/tests.md): Used in test fixtures
- **Depends On**:
  * [Software Module](../core-components/software-module.md): For camera and system control
  * [Configuration](../core-components/configuration.md): For settings access
  * [Power Management](../core-components/power-management.md): For power state management
  * System libraries and interfaces
- **Used By**:
  * Most web application components
  * Background tasks
  * API endpoints
  * User interface elements

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Camera Control from Web Interface**:
   - **Description**: Taking photos via the web interface.
   - **Example**: 
     ```python
     # In a route handler
     from src.web.utils.camera import capture_image
     
     @camera_bp.route('/api/camera/capture', methods=['POST'])
     def take_photo():
         # Get parameters from request
         options = request.get_json() or {}
         exposure = options.get('exposure', 'auto')
         resolution = options.get('resolution', '1920x1080')
         format = options.get('format', 'jpeg')
         
         try:
             # Use camera utility to capture image
             result = capture_image(
                 exposure=exposure,
                 resolution=resolution,
                 format=format
             )
             
             return jsonify({
                 "success": True,
                 "file_path": result['path'],
                 "timestamp": result['timestamp'],
                 "metadata": result['metadata']
             })
         except Exception as e:
             return jsonify({"success": False, "error": str(e)}), 500
     ```

2. **File Management**:
   - **Description**: Working with files in the web application.
   - **Example**: 
     ```python
     # In a service or route handler
     from src.web.utils.files import list_directory, get_file_info, safe_filename
     
     @gallery_bp.route('/api/gallery', methods=['GET'])
     def get_gallery():
         # Get directory listing
         directory = request.args.get('directory', 'captures')
         filter_type = request.args.get('type')
         
         try:
             # List files in directory with optional filter
             files = list_directory(directory, filter_type=filter_type)
             
             # Get detailed information for each file
             result = []
             for file_path in files:
                 info = get_file_info(file_path)
                 result.append({
                     "name": info['name'],
                     "path": file_path,
                     "size": info['size'],
                     "type": info['type'],
                     "created": info['created'],
                     "modified": info['modified'],
                     "dimensions": info.get('dimensions')
                 })
             
             return jsonify({"files": result})
         except Exception as e:
             return jsonify({"error": str(e)}), 500
             
     @gallery_bp.route('/api/gallery/upload', methods=['POST'])
     def upload_file():
         if 'file' not in request.files:
             return jsonify({"error": "No file provided"}), 400
             
         file = request.files['file']
         if file.filename == '':
             return jsonify({"error": "Empty filename"}), 400
             
         # Create safe filename
         filename = safe_filename(file.filename)
         
         # Save file
         file.save(os.path.join('uploads', filename))
         
         return jsonify({"success": True, "filename": filename})
     ```

3. **System Information Display**:
   - **Description**: Showing system status in the dashboard.
   - **Example**: 
     ```python
     # In a route handler
     from src.web.utils.system import get_system_info, get_memory_usage, get_disk_usage
     from src.web.utils.formatters import format_file_size
     
     @system_bp.route('/api/system/status', methods=['GET'])
     def system_status():
         try:
             # Get system information
             info = get_system_info()
             memory = get_memory_usage()
             disk = get_disk_usage('/')
             
             # Format for display
             memory_used_formatted = format_file_size(memory['used'])
             memory_total_formatted = format_file_size(memory['total'])
             
             return jsonify({
                 "hostname": info['hostname'],
                 "uptime": info['uptime'],
                 "cpu_temp": info['cpu_temperature'],
                 "memory": {
                     "used": memory_used_formatted,
                     "total": memory_total_formatted,
                     "percent": memory['percent']
                 },
                 "disk": {
                     "used": format_file_size(disk['used']),
                     "total": format_file_size(disk['total']),
                     "percent": disk['percent']
                 },
                 "network": info['network']
             })
         except Exception as e:
             return jsonify({"error": str(e)}), 500
     ```

4. **Date and Time Handling**:
   - **Description**: Using date utilities for scheduling and display.
   - **Example**: 
     ```python
     # In a service or route handler
     from src.web.utils.date_utils import format_timestamp, get_sunrise_sunset, is_night_time
     
     @scheduler_bp.route('/api/scheduler/optimal-times', methods=['GET'])
     def get_optimal_capture_times():
         try:
             # Get sunrise and sunset times
             times = get_sunrise_sunset()
             
             # Format for display
             sunrise = format_timestamp(times['sunrise'], "%H:%M")
             sunset = format_timestamp(times['sunset'], "%H:%M")
             
             # Calculate optimal wildlife photography times
             # (dawn and dusk are often best)
             dawn_start = format_timestamp(times['sunrise'] - 1800, "%H:%M")  # 30 min before sunrise
             dawn_end = format_timestamp(times['sunrise'] + 1800, "%H:%M")    # 30 min after sunrise
             dusk_start = format_timestamp(times['sunset'] - 1800, "%H:%M")   # 30 min before sunset
             dusk_end = format_timestamp(times['sunset'] + 1800, "%H:%M")     # 30 min after sunset
             
             # Check if it's currently night time
             is_night = is_night_time()
             
             return jsonify({
                 "sunrise": sunrise,
                 "sunset": sunset,
                 "optimal_periods": [
                     {"name": "Dawn", "start": dawn_start, "end": dawn_end},
                     {"name": "Dusk", "start": dusk_start, "end": dusk_end}
                 ],
                 "is_night": is_night,
                 "current_period": "Night" if is_night else "Day"
             })
         except Exception as e:
             return jsonify({"error": str(e)}), 500
     ```

5. **Security Operations**:
   - **Description**: Implementing secure operations in the application.
   - **Example**:
     ```python
     # In an authentication service
     from src.web.utils.security import hash_password, verify_password, generate_token
     
     def create_user(username, password):
         # Hash password securely before storing
         password_hash = hash_password(password)
         
         # Store in database
         user = User(
             username=username,
             password_hash=password_hash,
             created_at=datetime.now()
         )
         db.session.add(user)
         db.session.commit()
         
         return user
         
     def authenticate_user(username, password):
         # Find user
         user = User.query.filter_by(username=username).first()
         if not user:
             return None
             
         # Verify password
         if not verify_password(password, user.password_hash):
             return None
             
         # Generate authentication token
         token = generate_token()
         
         # Store token with expiration
         auth_token = AuthToken(
             user_id=user.id,
             token=token,
             expires_at=datetime.now() + timedelta(hours=24)
         )
         db.session.add(auth_token)
         db.session.commit()
         
         return {
             "user": user,
             "token": token,
             "expires_at": auth_token.expires_at
         }
     ```

</div>
</details>

## Utility Best Practices

When using the utility functions:

1. **Error Handling**: Always wrap utility calls in try/except blocks to handle potential errors gracefully
2. **Input Validation**: Validate inputs before passing to utility functions, especially for file paths and system commands
3. **Resource Management**: Close resources (files, connections) properly after using utility functions that open them
4. **Caching**: Consider caching results from expensive utility functions (like system status) that change infrequently
5. **Asynchronous Operations**: Use asynchronous versions of utilities for operations that may block (network, file I/O)
6. **Security**: Use security utilities to handle sensitive data and prevent security vulnerabilities
7. **Testing**: Create mocks for hardware-dependent utilities to enable effective testing
8. **Documentation**: Reference the utility documentation for detailed parameter descriptions and example usage
