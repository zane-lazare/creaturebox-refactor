# src/web/utils Directory Documentation

## Directory Purpose
The `src/web/utils` directory contains utility modules that provide reusable helper functions and classes for the CreatureBox web application. These utilities encapsulate common operations related to camera control, file management, and system interaction, creating a clean abstraction layer between the web routes and the underlying system functionality. By centralizing these utilities, the application maintains consistent behavior, reduces code duplication, and simplifies maintenance across multiple components.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| camera.py | Python | 1.8 KB | Camera control utilities |
| files.py | Python | 1.5 KB | File operation utilities |
| system.py | Python | 1.7 KB | System interaction utilities |

## Detailed File Descriptions

### camera.py
- **Primary Purpose**: Provides utility functions for camera control and management
- **Key Functions**:
  * `initialize_camera()`: Sets up camera with proper settings
  * `capture_photo(output_path, settings={})`: Takes a photo with specified settings
  * `get_camera_settings()`: Retrieves current camera configuration
  * `update_camera_settings(settings)`: Updates camera configuration
  * `get_camera_stream()`: Provides access to the camera stream
  * `release_camera()`: Properly releases camera resources
- **Dependencies**:
  * picamera module
  * src/config/camera_settings.csv
  * src/software/Take_Photo.py (indirect)
- **Technical Notes**: 
  * Implements thread-safe camera access
  * Manages hardware resources efficiently
  * Provides error handling for hardware issues
  * Supports multiple camera models through abstraction

### files.py
- **Primary Purpose**: Handles file operations for photos and configuration
- **Key Functions**:
  * `get_photos_by_date(date=None, limit=None)`: Retrieves photos filtered by date
  * `get_photo_metadata(photo_path)`: Extracts metadata from photo file
  * `generate_thumbnail(photo_path, size=(200, 200))`: Creates thumbnail for photo
  * `delete_photo(photo_path)`: Safely removes photo with confirmation
  * `get_storage_stats()`: Returns storage usage information
  * `ensure_directory_exists(path)`: Ensures directory is available for writing
- **Dependencies**:
  * os, shutil, glob modules
  * PIL (for image processing)
  * src/web/services/storage.py (indirect)
- **Technical Notes**: 
  * Implements safe file operations with error handling
  * Supports various file formats and organization schemes
  * Includes permission checking and path validation
  * Optimized for performance with large file collections

### system.py
- **Primary Purpose**: Provides system-level operations and monitoring
- **Key Functions**:
  * `get_system_status()`: Returns comprehensive system information
  * `reboot_system(delay=0)`: Initiates system reboot
  * `shutdown_system(delay=0)`: Initiates system shutdown
  * `get_cpu_temperature()`: Retrieves CPU temperature
  * `get_memory_usage()`: Returns memory usage statistics
  * `execute_system_command(command)`: Safely executes system commands
  * `toggle_attraction_lights(state)`: Controls wildlife attraction lights
- **Dependencies**:
  * os, subprocess modules
  * psutil (for system information)
  * src/software/Attract_On.py
  * src/software/Shut_Down.py
- **Technical Notes**: 
  * Implements security measures for command execution
  * Provides cross-platform compatibility where possible
  * Includes detailed error reporting
  * Optimized for Raspberry Pi hardware

## Relationship Documentation
- **Related To**:
  * src/web/routes/ (used by route handlers)
  * src/web/services/ (interacts with background services)
- **Depends On**:
  * src/config/ (configuration settings)
  * src/software/ (core system functionality)
  * Hardware-specific libraries
- **Used By**:
  * API route handlers
  * Web interface functionality
  * Background services

## Use Cases
1. **Photo Capture via Web Interface**:
   - **Implementation**: The camera.py utilities provide an abstraction for camera control used by the web API.
   - **Example**:
     ```python
     # In routes/camera.py
     from src.web.utils.camera import capture_photo, get_camera_settings
     
     @bp.route('/api/camera/capture', methods=['POST'])
     def api_capture_photo():
         # Get settings from request
         settings = request.json or {}
         
         # Generate output path
         date_dir = datetime.now().strftime('%Y-%m-%d')
         timestamp = datetime.now().strftime('%H%M%S')
         output_dir = f'/opt/creaturebox/data/photos/{date_dir}'
         output_path = f'{output_dir}/{timestamp}.jpg'
         
         # Create directory if needed
         from src.web.utils.files import ensure_directory_exists
         ensure_directory_exists(output_dir)
         
         # Capture photo using utility function
         try:
             result = capture_photo(output_path, settings)
             return jsonify({
                 'success': True,
                 'photo_path': result['path'],
                 'settings': result['settings']
             })
         except Exception as e:
             return jsonify({'error': str(e)}), 500
     ```

2. **Photo Gallery Management**:
   - **Implementation**: The files.py utilities provide functions for organizing and accessing photos.
   - **Example**:
     ```python
     # In routes/gallery.py
     from src.web.utils.files import get_photos_by_date, generate_thumbnail
     
     @bp.route('/api/gallery/photos', methods=['GET'])
     def api_get_photos():
         # Get query parameters
         date = request.args.get('date')
         limit = request.args.get('limit', 50, type=int)
         page = request.args.get('page', 1, type=int)
         
         # Get photos using utility function
         photos = get_photos_by_date(date, limit=limit, page=page)
         
         # Ensure thumbnails exist
         for photo in photos:
             if not os.path.exists(photo['thumbnail_path']):
                 generate_thumbnail(photo['path'])
         
         return jsonify({
             'photos': photos,
             'total': len(photos),
             'page': page
         })
     ```

3. **System Control and Monitoring**:
   - **Implementation**: The system.py utilities enable system management through the web interface.
   - **Example**:
     ```python
     # In routes/system.py
     from src.web.utils.system import get_system_status, reboot_system, toggle_attraction_lights
     
     @bp.route('/api/system/status', methods=['GET'])
     def api_system_status():
         # Get system information using utility function
         status = get_system_status()
         return jsonify(status)
     
     @bp.route('/api/system/reboot', methods=['POST'])
     def api_system_reboot():
         # Validate authorization (simplified)
         if not is_authorized('admin'):
             return jsonify({'error': 'Not authorized'}), 403
             
         # Get delay parameter
         delay = request.json.get('delay', 0)
         
         # Initiate reboot using utility function
         reboot_system(delay)
         return jsonify({
             'success': True,
             'message': f'System will reboot in {delay} seconds'
         })
     
     @bp.route('/api/system/toggle-lights', methods=['POST'])
     def api_toggle_lights():
         state = request.json.get('state', 'on')
         toggle_attraction_lights(state == 'on')
         return jsonify({
             'success': True,
             'lights': state
         })
     ```

4. **Storage Management**:
   - **Implementation**: The files.py utilities provide storage information and management capabilities.
   - **Example**:
     ```python
     # In routes/storage.py
     from src.web.utils.files import get_storage_stats, delete_photo
     
     @bp.route('/api/storage/stats', methods=['GET'])
     def api_storage_stats():
         # Get storage information using utility function
         stats = get_storage_stats()
         return jsonify(stats)
     
     @bp.route('/api/gallery/photos/<path:photo_path>', methods=['DELETE'])
     def api_delete_photo(photo_path):
         # Sanitize path (simplified)
         safe_path = sanitize_path(photo_path)
         
         # Delete photo using utility function
         try:
             result = delete_photo(safe_path)
             return jsonify({
                 'success': result,
                 'path': safe_path
             })
         except Exception as e:
             return jsonify({'error': str(e)}), 500
     ```
