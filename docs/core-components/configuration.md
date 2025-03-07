---
layout: default
title: Configuration
parent: Core Components
nav_order: 1
permalink: /core-components/configuration/
---

# Configuration Module

{% include navigation.html %}

## Overview

The Configuration Module contains the core system settings files that control the CreatureBox's operational parameters, including camera settings, control mappings, and scheduling configurations.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `src/config` directory serves as the central repository for all configuration files that define system-wide settings and parameters for the CreatureBox system. These files establish default values, valid ranges, and current settings for various components including:

- Camera operation and image capture parameters
- System controls and input mappings
- Scheduling and automated operations
- System-wide operational constants and thresholds
- Default configuration values for initial setup

These configuration files provide a centralized location for settings that affect multiple parts of the system, enabling consistent configuration management and allowing for both programmatic and user-driven customization of system behavior.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| camera_settings.csv | CSV | 1.2 KB | Camera configuration parameters |
| controls.txt | Text | 0.8 KB | System control settings |
| schedule_settings.csv | CSV | 0.9 KB | Automated schedule configuration |
| wordlist.csv | CSV | 20.1 KB | Extended lexical resources |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### camera_settings.csv
- **Primary Purpose**: Defines camera configuration parameters for photo capture
- **Key Fields**:
  * `setting_name`: Name of the camera setting
  * `value`: Current configured value
  * `default`: Default value if not configured
  * `min_value`: Minimum allowable value (for numeric settings)
  * `max_value`: Maximum allowable value (for numeric settings)
  * `options`: Available choices (for enumerated settings)
  * `description`: Human-readable description of the setting
  * `type`: Data type (integer, float, string, boolean, enum)
- **Key Settings**:
  * `resolution`: Image capture resolution (width x height)
  * `exposure_mode`: Camera exposure setting (auto, night, action, etc.)
  * `white_balance`: White balance mode (auto, sunlight, cloudy, etc.)
  * `iso`: ISO sensitivity setting (100-800)
  * `shutter_speed`: Manual shutter speed in microseconds
  * `image_effect`: Special effects (none, negative, sketch, etc.)
  * `led_enabled`: Enable/disable camera LED indicator
- **Dependencies**:
  * src/web/utils/camera.py (for applying settings)
  * src/web/routes/camera.py (for API access)
- **Technical Notes**: 
  * CSV format enables easy parsing and modification
  * Includes validation constraints for each setting
  * Organized by functional categories (exposure, resolution, etc.)
  * Changes require camera service restart to take effect

### controls.txt
- **Primary Purpose**: Defines system-wide control settings and operational parameters
- **Key Sections**:
  * System identification (name, ID, location)
  * Operational modes (normal, power-saving, maintenance)
  * Network configuration (connection preferences)
  * Notification settings (alerts, status reports)
  * Security parameters (access control)
  * GPIO pin mappings for physical buttons
  * Function assignments for each control
  * Long-press and short-press behavior definitions
  * LED indicator mappings
- **Dependencies**:
  * src/web/utils/system.py (for applying settings)
  * src/web/routes/settings.py (for API access)
- **Technical Notes**: 
  * Uses simple key-value format for easy parsing
  * Comments denoted with # character
  * Includes documentation for each setting inline
  * Read on system startup, changes require restart

### schedule_settings.csv
- **Primary Purpose**: Configures automated scheduling of system operations
- **Key Fields**:
  * `schedule_id`: Unique identifier for schedule entry
  * `operation`: Type of operation (photo, backup, power)
  * `time`: Time to execute operation (24-hour format)
  * `days`: Days to execute (comma-separated or daily/weekday/weekend)
  * `parameters`: JSON-encoded parameters for operation
  * `enabled`: Boolean indicating if schedule is active
  * `description`: Human-readable description
  * `last_run`: Timestamp of last execution
- **Key Settings**:
  * `start_time`: Daily start time for system activation
  * `end_time`: Daily end time for system shutdown
  * `capture_interval`: Time between photo captures (minutes)
  * `attraction_duration`: How long to run attraction features
  * `power_management`: Power profile to use (standard, eco, extreme)
  * `weekend_schedule`: Alternative settings for weekends
  * `holiday_mode`: Settings for extended unattended operation
- **Dependencies**:
  * src/software/scripts/auto_capture.py (for scheduled execution)
  * src/web/routes/settings.py (for API access)
- **Technical Notes**: 
  * CSV format enables easy parsing and modification
  * Supports complex scheduling patterns
  * Includes tracking of execution history
  * Processed by scheduler daemon, changes apply on next cycle

### wordlist.csv
- **Primary Purpose**: Extended lexical resources for system processing
- **Size**: 20.1 KB
- **Content**: Comprehensive word list for system processing and natural language functions
- **Dependencies**:
  * Text processing and analysis functions
- **Technical Notes**:
  * Supports extensible language processing features
  * Regularly updated with new terminology

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Software Module](../software-module.md): Uses configuration for operational parameters
  * [Power Module](../power-management.md): Gets power settings from configuration
  * [Web Interface](../../web-interface.md): Provides UI for editing configurations
  * src/web/config.py (application configuration)
  * src/web/routes/settings.py (settings management API)
- **Depends On**:
  * System hardware capabilities (for valid parameter ranges)
  * File system permissions (for modifications)
  * System default templates
  * User preferences
- **Used By**:
  * Camera control functions
  * Scheduler service
  * System initialization process
  * Web interface configuration panels
  * System settings API

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Camera Configuration Management**:
   - **Implementation**: The camera_settings.csv file defines all configurable parameters for the camera system.
   - **Example**:
     ```python
     # Reading camera settings in camera utility module
     def get_camera_settings():
         settings = {}
         with open('/opt/creaturebox/src/config/camera_settings.csv', 'r') as f:
             reader = csv.DictReader(f)
             for row in reader:
                 settings[row['setting_name']] = {
                     'value': convert_to_type(row['value'], row['type']),
                     'default': convert_to_type(row['default'], row['type']),
                     'type': row['type'],
                     'description': row['description']
                 }
         return settings
     ```

2. **Scheduled Operations Configuration**:
   - **Implementation**: The schedule_settings.csv file enables configuration of automated system operations.
   - **Example**:
     ```python
     # In scheduler module
     def load_schedules():
         schedules = []
         with open('/opt/creaturebox/src/config/schedule_settings.csv', 'r') as f:
             reader = csv.DictReader(f)
             for row in reader:
                 if row['enabled'].lower() == 'true':
                     schedules.append({
                         'id': row['schedule_id'],
                         'operation': row['operation'],
                         'time': row['time'],
                         'days': parse_days(row['days']),
                         'parameters': json.loads(row['parameters']),
                         'description': row['description']
                     })
         return schedules
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

## Validation Notes
- All configuration files are CSV or text-based for easy manual and programmatic editing
- The configuration system supports both user-driven and programmatic modifications
- Changes to configuration files trigger appropriate system responses (restarts, refreshes)
- Configuration values include validation constraints to ensure system stability