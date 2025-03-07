---
layout: default
title: Configuration
parent: Core Components
nav_order: 1
permalink: /core-components/configuration/
---

# Configuration

The configuration module defines system-wide settings and parameters for the CreatureBox system.

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