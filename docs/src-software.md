# src/software Directory Documentation

## Directory Purpose
The `src/software` directory contains operational Python scripts that provide core functionality for the CreatureBox system. These scripts implement camera control, system management, file operations, and other essential features that enable the proper functioning of the wildlife monitoring system. The software in this directory serves as a bridge between the web interface and the underlying hardware, providing command-line utilities that can be invoked both programmatically and directly by users when needed.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| Attract_On.py | Python | 0.7 KB | Attraction light control |
| Backup_Files.py | Python | 1.2 KB | File backup utility |
| Enable_Camera.py | Python | 0.9 KB | Camera initialization |
| Shut_Down.py | Python | 0.6 KB | System shutdown handler |
| Take_Photo.py | Python | 1.3 KB | Photo capture controller |
| Update_Project.py | Python | 0.8 KB | Software update utility |
| Upload_Photo.py | Python | 1.1 KB | Photo upload handler |
| WiFi_Setup.py | Python | 0.9 KB | Wireless configuration |

## Detailed File Descriptions

### Attract_On.py
- **Primary Purpose**: Controls the attraction light system for wildlife photography
- **Key Functions**:
  * `set_light_state(state, brightness)`: Turns lights on/off with brightness control
  * `pulse_lights(duration, frequency)`: Creates pulsing light pattern
  * `schedule_light_cycle(start_time, end_time, interval)`: Sets up timed light cycles
- **Dependencies**:
  * RPi.GPIO (for hardware control)
  * time, datetime modules
  * src/config/controls.txt (for settings)
- **Technical Notes**: Supports PWM for variable brightness, includes safety timeout

### Backup_Files.py
- **Primary Purpose**: Creates backups of photo files and system configuration
- **Key Functions**:
  * `backup_photos(source_dir, backup_dir)`: Copies photo files to backup location
  * `backup_config(config_path, backup_dir)`: Backs up configuration files
  * `create_archive(source_dir, archive_name)`: Creates compressed archive
  * `verify_backup(source_dir, backup_dir)`: Validates backup integrity
- **Dependencies**:
  * os, shutil modules
  * subprocess (for compression)
  * hashlib (for file verification)
- **Technical Notes**: Implements incremental backup strategy, tracks changes via checksums

### Enable_Camera.py
- **Primary Purpose**: Initializes and configures the camera hardware
- **Key Functions**:
  * `initialize_camera()`: Performs hardware initialization
  * `load_camera_settings()`: Applies settings from configuration file
  * `test_camera()`: Performs camera self-test
  * `configure_camera_mode(mode)`: Sets specific operational modes
- **Dependencies**:
  * picamera module
  * src/config/camera_settings.csv (for settings)
  * subprocess (for hardware commands)
- **Technical Notes**: Handles camera hardware errors, includes retry logic

### Shut_Down.py
- **Primary Purpose**: Manages clean system shutdown process
- **Key Functions**:
  * `safe_shutdown(delay=0)`: Performs orderly system shutdown
  * `emergency_shutdown()`: Rapid shutdown for critical conditions
  * `cleanup_before_shutdown()`: Closes files and services
  * `log_shutdown_reason(reason)`: Records shutdown cause
- **Dependencies**:
  * os, sys modules
  * subprocess (for system commands)
  * logging module
- **Technical Notes**: Ensures all data is written before power off, includes notification

### Take_Photo.py
- **Primary Purpose**: Controls photo capture process with various settings
- **Key Functions**:
  * `capture_photo(output_path, settings={})`: Takes photo with specified settings
  * `capture_timelapse(count, interval, output_dir)`: Creates time-lapse sequence
  * `capture_burst(count, output_dir)`: Takes rapid burst of photos
  * `apply_image_effects(photo_path, effects)`: Applies post-processing effects
- **Dependencies**:
  * picamera module
  * src/config/camera_settings.csv
  * PIL (for post-processing)
  * os, time modules
- **Technical Notes**: Supports multiple resolution and quality settings, includes EXIF data

### Update_Project.py
- **Primary Purpose**: Handles software updates for the CreatureBox system
- **Key Functions**:
  * `check_for_updates()`: Checks repository for newer versions
  * `download_update()`: Retrieves update package
  * `verify_update_package(package_path)`: Validates update integrity
  * `apply_update(package_path)`: Installs update
  * `rollback_update()`: Reverts to previous version if needed
- **Dependencies**:
  * requests module
  * subprocess, os modules
  * hashlib (for package verification)
- **Technical Notes**: Includes backup of current version before update, supports staged rollout

### Upload_Photo.py
- **Primary Purpose**: Transfers photos to remote storage or services
- **Key Functions**:
  * `upload_to_server(photo_path, server_url)`: Uploads to HTTP server
  * `upload_to_cloud(photo_path, service="s3")`: Uploads to cloud storage
  * `upload_batch(photo_dir, destination)`: Processes multiple files
  * `check_connectivity()`: Verifies network connection before upload
- **Dependencies**:
  * requests module
  * boto3 (for AWS uploads)
  * os module
  * src/config/controls.txt (for settings)
- **Technical Notes**: Implements retry logic, bandwidth throttling, supports multiple services

### WiFi_Setup.py
- **Primary Purpose**: Configures and manages wireless network connectivity
- **Key Functions**:
  * `setup_wifi_connection(ssid, password)`: Configures new connection
  * `scan_networks()`: Lists available networks
  * `test_connection()`: Validates connectivity
  * `save_network_config(config)`: Stores connection settings
- **Dependencies**:
  * subprocess module
  * os module
  * requests (for connectivity testing)
- **Technical Notes**: Creates wpa_supplicant configuration, includes fallback to known networks

## Relationship Documentation
- **Related To**:
  * src/web/routes/ (invoked by web API)
  * src/power/ (used in power management)
- **Depends On**:
  * src/config/ (configuration files)
  * Hardware-specific libraries (RPi.GPIO, picamera)
  * System utilities (wpa_supplicant, shutdown)
- **Used By**:
  * Web application for system control
  * Scheduled tasks
  * User-initiated operations

## Use Cases
1. **Wildlife Photography with Attraction Lights**:
   - **Implementation**: The Attract_On.py script controls LED lighting to attract wildlife for better photos.
   - **Example**:
     ```python
     # Used in web interface to control lights
     def api_toggle_lights():
         state = request.json.get('state')
         brightness = request.json.get('brightness', 100)
         duration = request.json.get('duration', 0)
         
         # Call the script with appropriate parameters
         cmd = [
             'python', 
             '/opt/creaturebox/src/software/Attract_On.py',
             '--state', state,
             '--brightness', str(brightness)
         ]
         if duration:
             cmd.extend(['--duration', str(duration)])
             
         subprocess.Popen(cmd)
         return jsonify({"status": "success"})
     ```

2. **Scheduled Photo Capture**:
   - **Implementation**: The Take_Photo.py script enables automated photography at specified intervals.
   - **Example**:
     ```python
     # Used in scheduler for timed captures
     def scheduled_photo_capture():
         timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
         output_dir = f'/opt/creaturebox/data/photos/{datetime.now().strftime("%Y-%m-%d")}'
         os.makedirs(output_dir, exist_ok=True)
         
         # Call the script with appropriate settings
         cmd = [
             'python',
             '/opt/creaturebox/src/software/Take_Photo.py',
             '--output', f'{output_dir}/{timestamp}.jpg',
             '--resolution', 'high',
             '--effect', 'auto'
         ]
         subprocess.run(cmd)
     ```

3. **System Updates and Maintenance**:
   - **Implementation**: The Update_Project.py script provides a mechanism for updating the system software.
   - **Example**:
     ```python
     # Used in system maintenance API
     @app.route('/api/system/update', methods=['POST'])
     def update_system_software():
         # Start update in background process
         job = job_queue.enqueue(
             subprocess.run,
             ['python', '/opt/creaturebox/src/software/Update_Project.py', '--perform-update']
         )
         return jsonify({"job_id": job.id})
     ```

4. **Field Data Management**:
   - **Implementation**: The combination of Backup_Files.py and Upload_Photo.py enables managing photos in remote deployments.
   - **Example**:
     ```python
     # Used in storage management
     def weekly_data_maintenance():
         # First backup locally
         subprocess.run([
             'python',
             '/opt/creaturebox/src/software/Backup_Files.py',
             '--source', '/opt/creaturebox/data/photos',
             '--destination', '/mnt/backup'
         ])
         
         # Then upload if connection available
         if check_internet_connection():
             subprocess.run([
                 'python',
                 '/opt/creaturebox/src/software/Upload_Photo.py',
                 '--source', '/opt/creaturebox/data/photos',
                 '--destination', 'cloud',
                 '--service', 's3',
                 '--bucket', 'wildlife-monitoring-data'
             ])
     ```
