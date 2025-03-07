# Configuration Module Documentation

{% include navigation.html %}

## Overview

The Configuration Module contains the core system settings files that control the CreatureBox's operational parameters, including camera settings, control mappings, and scheduling configurations.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `src/config` directory serves as the central repository for all configuration files that control the behavior of the CreatureBox system. This module provides:

- Structured settings for camera operation
- Input control mappings and definitions
- Scheduling parameters for automated operation
- System-wide operational constants and thresholds
- Default configuration values for initial setup

These configuration files are used by various system components to ensure consistent behavior across the application and to allow customization without code changes.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Purpose |
|----------|------|------|---------|
| camera_settings.csv | CSV | 1.2 KB | Camera configuration parameters |
| controls.txt | Text | 0.8 KB | Input control mappings |
| schedule_settings.csv | CSV | 0.9 KB | Automated operation scheduling |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### camera_settings.csv
- **Primary Purpose**: Defines camera operational parameters
- **Key Settings**:
  * `resolution`: Image capture resolution (width x height)
  * `exposure_mode`: Camera exposure setting (auto, night, action, etc.)
  * `white_balance`: White balance mode (auto, sunlight, cloudy, etc.)
  * `iso`: ISO sensitivity setting (100-800)
  * `shutter_speed`: Manual shutter speed in microseconds
  * `image_effect`: Special effects (none, negative, sketch, etc.)
  * `led_enabled`: Enable/disable camera LED indicator
- **Format**: CSV with header row and parameter values
- **Technical Notes**: Changes require camera service restart to take effect

### controls.txt
- **Primary Purpose**: Maps hardware controls to system functions
- **Key Settings**:
  * GPIO pin mappings for physical buttons
  * Function assignments for each control
  * Long-press and short-press behavior definitions
  * LED indicator mappings
- **Format**: Plain text with key=value pairs
- **Technical Notes**: Read on system startup, changes require restart

### schedule_settings.csv
- **Primary Purpose**: Defines automated operation schedule
- **Key Settings**:
  * `start_time`: Daily start time for system activation
  * `end_time`: Daily end time for system shutdown
  * `capture_interval`: Time between photo captures (minutes)
  * `attraction_duration`: How long to run attraction features
  * `power_management`: Power profile to use (standard, eco, extreme)
  * `weekend_schedule`: Alternative settings for weekends
  * `holiday_mode`: Settings for extended unattended operation
- **Format**: CSV with header row and schedule parameters
- **Technical Notes**: Processed by scheduler daemon, changes apply on next cycle

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Software Module](./src-software.md): Uses configuration for operational parameters
  * [Power Module](./src-power.md): Gets power settings from configuration
  * [Web Interface](./src-web.md): Provides UI for editing configurations
- **Depends On**:
  * System default templates
  * User preferences
- **Used By**:
  * Camera control scripts
  * Scheduler service
  * System initialization process
  * Web interface configuration panels

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Camera Configuration**:
   - **Description**: Setting up optimal camera parameters for wildlife photography.
   - **Example**: 
     ```python
     # Read camera settings from configuration
     import csv
     
     with open('/path/to/camera_settings.csv', 'r') as f:
         reader = csv.DictReader(f)
         settings = next(reader)  # Get first row
     
     # Apply settings to camera
     camera.resolution = (int(settings['resolution_x']), int(settings['resolution_y']))
     camera.exposure_mode = settings['exposure_mode']
     camera.iso = int(settings['iso'])
     ```

2. **Scheduled Operation**:
   - **Description**: Configuring automated capture schedules.
   - **Example**: 
     ```python
     # Parse schedule settings
     import csv
     from datetime import datetime, time
     
     with open('/path/to/schedule_settings.csv', 'r') as f:
         reader = csv.DictReader(f)
         schedule = next(reader)
     
     # Determine if system should be active
     now = datetime.now().time()
     start = datetime.strptime(schedule['start_time'], '%H:%M').time()
     end = datetime.strptime(schedule['end_time'], '%H:%M').time()
     
     if start <= now <= end:
         # System should be active
         activate_system()
     else:
         # System should be in low power mode
         enter_low_power_mode()
     ```

3. **Control Mapping**:
   - **Description**: Mapping hardware buttons to software functions.
   - **Example**: 
     ```python
     # Load control mappings
     controls = {}
     with open('/path/to/controls.txt', 'r') as f:
         for line in f:
             if line.strip() and not line.startswith('#'):
                 key, value = line.strip().split('=')
                 controls[key.strip()] = value.strip()
     
     # Set up GPIO for button
     import RPi.GPIO as GPIO
     GPIO.setmode(GPIO.BCM)
     
     capture_button_pin = int(controls['capture_button_gpio'])
     GPIO.setup(capture_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
     GPIO.add_event_detect(capture_button_pin, GPIO.FALLING, 
                          callback=take_photo, bouncetime=300)
     ```

4. **Configuration Update**:
   - **Description**: Updating configuration through the web interface.
   - **Example**: 
     ```python
     # Web route to update camera settings
     @app.route('/api/settings/camera', methods=['POST'])
     def update_camera_settings():
         new_settings = request.get_json()
         
         # Validate settings
         if 'resolution_x' not in new_settings or 'resolution_y' not in new_settings:
             return jsonify({'error': 'Missing resolution parameters'}), 400
             
         # Write to CSV
         with open('/path/to/camera_settings.csv', 'w', newline='') as f:
             writer = csv.DictWriter(f, fieldnames=new_settings.keys())
             writer.writeheader()
             writer.writerow(new_settings)
             
         # Restart camera service to apply changes
         subprocess.run(['systemctl', 'restart', 'creaturebox-camera.service'])
         
         return jsonify({'success': True})
     ```

</div>
</details>
