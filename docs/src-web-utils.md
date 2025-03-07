# Web Utilities Module Documentation

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

| Filename | Type | Size | Purpose |
|----------|------|------|---------|
| __init__.py | Python | 0.2 KB | Package initialization |
| camera.py | Python | 2.4 KB | Camera interfaces |
| files.py | Python | 1.8 KB | File operations |
| system.py | Python | 2.1 KB | System interaction |
| date_utils.py | Python | 1.2 KB | Date/time utilities |
| validators.py | Python | 1.5 KB | Data validation |
| formatters.py | Python | 0.9 KB | Data formatting |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### __init__.py
- **Primary Purpose**: Package initialization
- **Key Functions**:
  * Exports common utility functions
- **Dependencies**:
  * None
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
- **Dependencies**:
  * None
- **Technical Notes**: Simple pure functions for formatting

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Web Routes](./src-web-routes.md): Used by route handlers
  * [Web Services](./src-web-services.md): Used by business logic services
  * [Web Tests](./src-web-tests.md): Used in test fixtures
- **Depends On**:
  * [Software Module](./src-software.md): For camera and system control
  * [Configuration Module](./src-config.md): For settings access
  * [Power Module](./src-power.md): For power state management
  * System libraries and interfaces
- **Used By**:
  * Most web application components
  * Background tasks
  * API endpoints

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

</div>
</details>
