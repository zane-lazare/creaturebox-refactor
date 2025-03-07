# src/config Directory Documentation

## Directory Purpose
The `src/config` directory contains configuration files that define system-wide settings and parameters for the CreatureBox system. These files establish default values, valid ranges, and current settings for various components including camera operation, system controls, and scheduling. The configuration files provide a centralized location for settings that affect multiple parts of the system, enabling consistent configuration management and allowing for both programmatic and user-driven customization of system behavior.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| camera_settings.csv | CSV | 0.8 KB | Camera configuration parameters |
| controls.txt | Text | 0.5 KB | System control settings |
| schedule_settings.csv | CSV | 0.7 KB | Automated schedule configuration |

## Detailed File Descriptions

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
- **Dependencies**:
  * src/web/utils/camera.py (for applying settings)
  * src/web/routes/camera.py (for API access)
- **Technical Notes**: 
  * CSV format enables easy parsing and modification
  * Includes validation constraints for each setting
  * Organized by functional categories (exposure, resolution, etc.)

### controls.txt
- **Primary Purpose**: Defines system-wide control settings and operational parameters
- **Key Sections**:
  * System identification (name, ID, location)
  * Operational modes (normal, power-saving, maintenance)
  * Network configuration (connection preferences)
  * Notification settings (alerts, status reports)
  * Security parameters (access control)
- **Dependencies**:
  * src/web/utils/system.py (for applying settings)
  * src/web/routes/settings.py (for API access)
- **Technical Notes**: 
  * Uses simple key-value format for easy parsing
  * Comments denoted with # character
  * Includes documentation for each setting inline

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
- **Dependencies**:
  * src/software/scripts/auto_capture.py (for scheduled execution)
  * src/web/routes/settings.py (for API access)
- **Technical Notes**: 
  * CSV format enables easy parsing and modification
  * Supports complex scheduling patterns
  * Includes tracking of execution history

## Relationship Documentation
- **Related To**:
  * src/web/config.py (application configuration)
  * src/web/routes/settings.py (settings management API)
- **Depends On**:
  * System hardware capabilities (for valid parameter ranges)
  * File system permissions (for modifications)
- **Used By**:
  * Camera control functions
  * Scheduling system
  * System settings API
  * Web interface for configuration

## Use Cases
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
     
     # Updating a camera setting
     def update_camera_setting(name, value):
         settings = get_camera_settings()
         if name not in settings:
             raise ValueError(f"Unknown setting: {name}")
             
         # Validate value against constraints
         # Update in-memory representation
         settings[name]['value'] = value
         
         # Write back to CSV file
         # Apply setting to camera hardware
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
     
     # In cron-like scheduler
     def check_schedules():
         now = datetime.now()
         today = now.strftime('%A').lower()
         current_time = now.strftime('%H:%M')
         
         schedules = load_schedules()
         for schedule in schedules:
             if today in schedule['days'] and current_time == schedule['time']:
                 execute_scheduled_operation(schedule)
                 update_last_run(schedule['id'])
     ```

3. **System Control Configuration**:
   - **Implementation**: The controls.txt file defines system-wide operational parameters.
   - **Example**:
     ```python
     # Reading system controls
     def get_system_controls():
         controls = {}
         with open('/opt/creaturebox/src/config/controls.txt', 'r') as f:
             for line in f:
                 line = line.strip()
                 if not line or line.startswith('#'):
                     continue
                     
                 key, value = line.split('=', 1)
                 controls[key.strip()] = value.strip()
         return controls
     
     # Using control values to determine system behavior
     def should_enable_feature(feature_name):
         controls = get_system_controls()
         if f"{feature_name}_enabled" in controls:
             return controls[f"{feature_name}_enabled"].lower() == 'true'
         return False  # Default to disabled if not specified
     ```

4. **Configuration Validation and Update**:
   - **Implementation**: Configuration files include validation constraints that are enforced when updated.
   - **Example**:
     ```python
     # API route for updating camera settings
     @app.route('/api/camera/settings', methods=['POST'])
     def update_camera_settings():
         settings = request.json
         
         # Read current configuration with constraints
         current_settings = read_camera_settings_with_constraints()
         
         # Validate and apply updates
         validation_errors = []
         for name, value in settings.items():
             if name not in current_settings:
                 validation_errors.append(f"Unknown setting: {name}")
                 continue
                 
             constraints = current_settings[name]
             
             # Type validation
             if constraints['type'] == 'integer':
                 if not isinstance(value, int):
                     validation_errors.append(f"{name} must be an integer")
                     continue
             
             # Range validation for numeric values
             if 'min_value' in constraints and value < constraints['min_value']:
                 validation_errors.append(
                     f"{name} must be at least {constraints['min_value']}")
                 continue
             
             # Apply valid setting
             update_camera_setting(name, value)
             
         if validation_errors:
             return jsonify({"errors": validation_errors}), 400
             
         return jsonify({"success": True})
     ```
