---
layout: default
title: Configuration Files
parent: Source Configuration
nav_order: 2
permalink: /src/config/files/
---

# Configuration Files Documentation

{% include navigation.html %}

## Overview

The Configuration Files within the `src/config` directory provide the foundational settings and parameters that control the CreatureBox system's behavior. These files define camera operation parameters, control mappings, scheduling settings, and system-wide constants.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The configuration files in the `src/config` directory serve several crucial purposes:

- Define system-wide settings that affect multiple components
- Establish default values and valid ranges for configurable parameters
- Provide a centralized location for all adjustable system settings
- Support both programmatic and user-driven configuration changes
- Enable persistence of configuration across system restarts
- Standardize the format and structure of configuration data
- Allow for runtime modification of system behavior without code changes

These files are designed to be human-readable, easily modifiable by both automated processes and manual editing, and provide clear documentation of available settings.

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
| default_config.json | JSON | 2.3 KB | System-wide default settings |
| wordlist.csv | CSV | 20.1 KB | Extended lexical resources |
| hardware_mappings.yaml | YAML | 1.5 KB | Hardware-specific configuration |
| network_config.json | JSON | 0.7 KB | Network connection parameters |
| alert_thresholds.csv | CSV | 0.6 KB | System alert configuration |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### camera_settings.csv
- **Primary Purpose**: Defines all configurable parameters for the camera system
- **Key Fields**:
  * `setting_name`: Parameter identifier
  * `value`: Current configured value
  * `default`: Factory default value
  * `min_value` / `max_value`: Valid range for numeric parameters
  * `options`: Available choices for enumerated settings
  * `type`: Data type (integer, float, boolean, string, enum)
  * `description`: Human-readable explanation
- **Key Settings**:
  * Resolution configuration (width, height)
  * Exposure parameters (mode, compensation)
  * Image quality settings (ISO, white balance)
  * Special effects and processing options
- **Technical Notes**: 
  * Changes require camera system restart
  * CSV format enables both human and machine editing
  * Includes validation constraints for each setting

### controls.txt
- **Primary Purpose**: Defines system input and control mappings
- **Format**: Key-value pairs with # comments
- **Key Sections**:
  * GPIO pin assignments
  * Button function mappings
  * Multi-press behavior configuration
  * LED indicator patterns
  * Input debounce settings
  * Long-press duration thresholds
- **Technical Notes**:
  * Simple text format for easy editing
  * Read at system startup
  * Comments provide in-file documentation
  * Changes require system restart to take effect

### schedule_settings.csv
- **Primary Purpose**: Configures automated operations scheduling
- **Key Fields**:
  * `schedule_id`: Unique entry identifier
  * `operation`: Action type (photo, backup, power)
  * `time`: Execution time (24-hour format)
  * `days`: Schedule days (daily, weekday, weekend, comma-separated days)
  * `parameters`: JSON-encoded operation parameters
  * `enabled`: Active/inactive flag
  * `description`: Human-readable description
  * `last_run`: Previous execution timestamp
- **Technical Notes**:
  * Processed by scheduler daemon
  * Changes apply on next scheduler cycle
  * Supports complex scheduling patterns
  * Maintains execution history

### default_config.json
- **Primary Purpose**: System-wide default configuration
- **Key Sections**:
  * System identification (name, location, ID)
  * User interface preferences
  * Security settings
  * Storage management policies
  * Performance optimization parameters
  * Logging configuration
  * Development/production mode flags
- **Technical Notes**:
  * JSON format for structured data
  * Used for initial system setup
  * Provides reference defaults
  * Used for configuration reset operations

### wordlist.csv
- **Primary Purpose**: Lexical resources for text processing
- **Content**:
  * Vocabulary for natural language functions
  * Domain-specific terminology
  * Alternative spellings and forms
  * Word classification tags
- **Technical Notes**:
  * Large reference dataset (20.1 KB)
  * Used by text analysis functions
  * Regularly updated with new terminology
  * Supports extensible language processing

### hardware_mappings.yaml
- **Primary Purpose**: Hardware-specific configuration
- **Key Sections**:
  * Hardware component identifiers
  * Pin assignments for peripherals
  * Device addressing information
  * Interface specifications
  * Component capabilities and limitations
- **Technical Notes**:
  * YAML format for readability and structure
  * Supports different hardware configurations
  * Used during system initialization
  * Changes require full system restart

### network_config.json
- **Primary Purpose**: Network communication settings
- **Key Settings**:
  * Connection parameters
  * Web server configuration
  * API endpoint definitions
  * Local network preferences
  * Remote connectivity options
  * Connection fallback policies
- **Technical Notes**:
  * JSON format for structured data
  * Used by networking components
  * Dynamic update supported for some settings
  * Security-sensitive information handled securely

### alert_thresholds.csv
- **Primary Purpose**: System monitoring thresholds
- **Key Fields**:
  * `metric_name`: Monitored parameter
  * `warning_threshold`: Warning level trigger
  * `critical_threshold`: Critical level trigger
  * `evaluation_period`: Measurement window
  * `notification_method`: Alert delivery method
  * `enabled`: Active/inactive flag
- **Technical Notes**:
  * Defines when system alerts are triggered
  * Used by monitoring daemon
  * Changes apply immediately
  * CSV format for easy modification

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Core Configuration Module](../core-components/configuration.md): Comprehensive documentation
  * [Software Module](../core-components/software-module.md): Uses configuration parameters
  * [Power Management](../core-components/power-management.md): Power-related settings
  * [Web Interface](../web-interface/core.md): UI for configuration management
- **Depends On**:
  * File system permissions (for modifications)
  * System hardware capabilities (for valid parameter ranges)
  * Default templates and reference configurations
- **Used By**:
  * Camera control system (`src/software/camera_manager.py`)
  * System scheduler (`src/software/scheduler.py`)
  * Web configuration API (`src/web/routes/settings.py`)
  * System initialization process (`src/software/init.py`)
  * Power management system (`src/power/power_controller.py`)
  * Input handling system (`src/software/input_handler.py`)

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Reading Camera Settings Programmatically**:
   - **Description**: Application code accessing camera configuration
   - **Example**:
     ```python
     # In src/software/camera_manager.py
     def get_camera_settings():
         settings = {}
         with open('/opt/creaturebox/src/config/camera_settings.csv', 'r') as f:
             reader = csv.DictReader(f)
             for row in reader:
                 # Convert value to appropriate type
                 if row['type'] == 'integer':
                     value = int(row['value'])
                 elif row['type'] == 'float':
                     value = float(row['value'])
                 elif row['type'] == 'boolean':
                     value = row['value'].lower() == 'true'
                 else:
                     value = row['value']
                     
                 settings[row['setting_name']] = value
         return settings
     ```

2. **Modifying Configuration Through Web Interface**:
   - **Description**: User updating settings via web UI
   - **Example**:
     ```python
     # In src/web/routes/settings.py
     @app.route('/api/settings/camera', methods=['POST'])
     def update_camera_settings():
         # Get settings from request
         new_settings = request.get_json()
         
         # Read current settings
         with open('/opt/creaturebox/src/config/camera_settings.csv', 'r') as f:
             reader = csv.DictReader(f)
             current_settings = list(reader)
             
         # Update changed settings
         for setting in current_settings:
             if setting['setting_name'] in new_settings:
                 setting['value'] = str(new_settings[setting['setting_name']])
                 
         # Write back to file
         with open('/opt/creaturebox/src/config/camera_settings.csv', 'w', newline='') as f:
             writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
             writer.writeheader()
             writer.writerows(current_settings)
             
         # Apply changes
         restart_camera_service()
         return jsonify({"status": "success"})
     ```

3. **Scheduling Automated Operations**:
   - **Description**: Setting up automated tasks via schedule configuration
   - **Example**:
     ```python
     # In src/software/scheduler.py
     def load_schedules():
         schedules = []
         with open('/opt/creaturebox/src/config/schedule_settings.csv', 'r') as f:
             reader = csv.DictReader(f)
             for row in reader:
                 if row['enabled'].lower() == 'true':
                     # Parse schedule entry
                     schedule = {
                         'id': row['schedule_id'],
                         'operation': row['operation'],
                         'time': datetime.strptime(row['time'], '%H:%M').time(),
                         'days': parse_days(row['days']),
                         'parameters': json.loads(row['parameters']),
                         'description': row['description']
                     }
                     schedules.append(schedule)
         return schedules
         
     def run_scheduled_operations():
         schedules = load_schedules()
         now = datetime.now()
         for schedule in schedules:
             if should_run(schedule, now):
                 execute_operation(schedule['operation'], schedule['parameters'])
                 update_last_run(schedule['id'], now)
     ```

4. **Resetting to Default Configuration**:
   - **Description**: Restoring system to default settings
   - **Example**:
     ```python
     # In src/software/config_manager.py
     def reset_to_defaults():
         # Load default configuration
         with open('/opt/creaturebox/src/config/default_config.json', 'r') as f:
             defaults = json.load(f)
             
         # Apply defaults to each configuration file
         for config_type, settings in defaults.items():
             if config_type == 'camera':
                 reset_camera_settings(settings)
             elif config_type == 'schedule':
                 reset_schedule_settings(settings)
             elif config_type == 'network':
                 reset_network_settings(settings)
                 
         # Restart services to apply changes
         restart_required_services()
     ```

5. **Hardware-Specific Configuration**:
   - **Description**: Adapting to specific hardware capabilities
   - **Example**:
     ```python
     # In src/software/hardware_manager.py
     def initialize_hardware():
         # Load hardware mappings
         with open('/opt/creaturebox/src/config/hardware_mappings.yaml', 'r') as f:
             hardware_config = yaml.safe_load(f)
         
         # Configure GPIO based on hardware model
         model = detect_hardware_model()
         if model in hardware_config:
             pin_config = hardware_config[model]['pins']
             configure_gpio(pin_config)
             
             # Set up camera interface
             camera_interface = hardware_config[model]['camera']['interface']
             initialize_camera(camera_interface)
         else:
             raise Exception(f"Unsupported hardware model: {model}")
     ```

</div>
</details>

## Configuration Management Best Practices

- Always use the configuration API rather than direct file modification when possible
- Validate all configuration changes against defined constraints
- Back up configuration files before making significant changes
- Use version control to track configuration changes over time
- Implement proper file locking when making programmatic changes
- Provide appropriate user feedback when configuration changes require service restarts
- Follow the principle of least privilege for file permissions
