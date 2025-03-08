---
layout: default
title: Software Files
parent: Software Module
nav_order: 1
permalink: /src/software/files/
---

# Software Files Documentation

{% include navigation.html %}

## Overview

The Software Files within the `src/software` directory comprise the core operational scripts and utilities that drive the CreatureBox system's functionality. These scripts control critical functions including camera operations, attraction mode, system scheduling, power management, and diagnostic capabilities.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The software files in this directory serve as the operational core of the CreatureBox system, providing essential functionality:

- Control hardware components including cameras and attraction mechanisms
- Implement scheduling for automated system operations
- Provide diagnostic and debugging capabilities for troubleshooting
- Manage power consumption and system resources
- Enable backup and data management operations
- Support network configuration and connectivity
- Facilitate remote system administration
- Monitor system health and implement self-healing capabilities
- Control system startup, shutdown, and operational modes

These scripts bridge the gap between hardware components and user interfaces, allowing both automated and user-driven control of the system's capabilities.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

### Main Directory Files

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| Attract_On.py | Python | 2.3 KB | Enables wildlife attraction mode |
| Attract_Off.py | Python | 1.8 KB | Disables wildlife attraction mode |
| Backup_Files.py | Python | 3.1 KB | System data backup utility |
| DebugMode.py | Python | 2.5 KB | System diagnostic functionality |
| Measure_Power.py | Python | 1.7 KB | Power consumption monitoring |
| Scheduler.py | Python | 4.2 KB | Automated task scheduling system |
| TakePhoto.py | Python | 3.8 KB | Camera control and image capture |
| StartCron.py | Python | 0.9 KB | Enables scheduled task system |
| StopCron.py | Python | 0.7 KB | Disables scheduled task system |
| StopScheduledShutdown.py | Python | 1.1 KB | Cancels pending shutdown |
| TurnEverythingOff.py | Python | 1.5 KB | Complete system shutdown |
| RegisterNewWifi.sh | Shell | 1.2 KB | WiFi network configuration |
| readme.md | Markdown | 0.5 KB | Module documentation |
| __init__.py | Python | 0.1 KB | Package initialization |
| software_utils.py | Python | 2.4 KB | Common utility functions |
| hardware_interface.py | Python | 3.6 KB | Hardware abstraction layer |
| error_handling.py | Python | 1.9 KB | Error management system |

### Scripts Subdirectory

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| auto_capture.py | Python | 1.1 KB | Automated photo capture scheduler |
| diagnostic.py | Python | 1.4 KB | Extended system diagnostic tools |
| monitor_disk.py | Python | 0.8 KB | Storage usage monitoring |
| remote_control.py | Python | 1.2 KB | Remote command interface |
| system_check.py | Python | 0.9 KB | System health validation |
| image_processing.py | Python | 2.7 KB | Image enhancement utilities |
| notification.py | Python | 1.3 KB | Alert and notification system |
| data_cleanup.py | Python | 1.5 KB | Storage management utilities |
| sensor_reader.py | Python | 1.8 KB | Environmental sensor interface |
| motion_detection.py | Python | 2.2 KB | Motion-triggered operations |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### Core Operational Scripts

#### Attract_On.py / Attract_Off.py
- **Primary Purpose**: Control wildlife attraction mechanisms
- **Key Functions**:
  * `start_attraction_sequence()`: Activates lights, sounds, and other attractants
  * `set_attraction_mode(mode)`: Configures attraction intensity and pattern
  * `get_attraction_status()`: Reports current state of attraction systems
  * `stop_attraction_sequence()`: Safely terminates all attraction mechanisms
- **Technical Notes**:
  * Uses PWM for LED control with customizable patterns
  * Supports multiple audio playback options
  * Implements gradual startup/shutdown to avoid startling wildlife
  * Energy-efficient operation with configurable duty cycles

#### TakePhoto.py
- **Primary Purpose**: Camera control and image capture
- **Key Functions**:
  * `initialize_camera(settings)`: Configures camera with specified parameters
  * `capture_single_image(filename)`: Takes individual photo
  * `capture_sequence(count, interval)`: Takes series of photos
  * `adjust_camera_settings(params)`: Updates camera configuration
  * `get_camera_status()`: Reports camera state and settings
- **Technical Notes**:
  * Hardware abstraction layer supports multiple camera models
  * Implements adaptive exposure for varying light conditions
  * Configurable image resolution, quality, and format
  * Automatic image storage and organization

#### Scheduler.py
- **Primary Purpose**: Automated task scheduling
- **Key Functions**:
  * `load_schedule()`: Reads schedule configuration
  * `add_task(time, task, params)`: Adds new scheduled operation
  * `remove_task(task_id)`: Cancels specific scheduled task
  * `run_pending_tasks()`: Executes due operations
  * `generate_schedule_report()`: Creates summary of pending tasks
- **Technical Notes**:
  * Hybrid scheduling using cron for persistence and in-memory for precision
  * Supports complex schedules (daily, weekday, weekend, specific dates)
  * Schedule persistence across system restarts
  * Priority-based execution for conflicting tasks

### System Management

#### Backup_Files.py
- **Primary Purpose**: Data backup and archiving
- **Key Functions**:
  * `backup_configuration()`: Archives system settings
  * `backup_images(date_range)`: Archives captured photos
  * `backup_logs()`: Preserves system logs
  * `schedule_recurring_backup()`: Sets up automated backups
  * `verify_backup_integrity()`: Validates backup completeness
- **Technical Notes**:
  * Supports local and remote backup destinations (USB, network)
  * Implements incremental backups to conserve space
  * Configurable compression and encryption
  * Retention policy management for backup rotation

#### DebugMode.py
- **Primary Purpose**: System diagnostics and troubleshooting
- **Key Functions**:
  * `enable_debug_mode()`: Activates enhanced logging
  * `run_hardware_diagnostics()`: Tests system components
  * `analyze_logs()`: Searches logs for errors
  * `generate_diagnostic_report()`: Creates comprehensive system report
  * `capture_debug_data()`: Collects relevant system information
- **Technical Notes**:
  * Non-intrusive diagnostics safe for production use
  * Detailed hardware component testing
  * Performance impact monitoring
  * Secure handling of sensitive information

#### Measure_Power.py
- **Primary Purpose**: Power monitoring and management
- **Key Functions**:
  * `read_power_consumption()`: Measures current power usage
  * `check_battery_level()`: Determines remaining battery capacity
  * `log_power_metrics()`: Records power data for analysis
  * `notify_low_power()`: Triggers alerts for low power conditions
  * `activate_power_saving()`: Initiates conservation measures
- **Technical Notes**:
  * Compatible with standard power monitoring circuits
  * Calibration support for accurate measurements
  * Historical trend analysis capabilities
  * Integration with power management subsystem

### Control Scripts

#### StartCron.py / StopCron.py
- **Primary Purpose**: Scheduled task management
- **Key Functions**:
  * `enable_scheduled_tasks()`: Activates task scheduler
  * `disable_scheduled_tasks()`: Suspends task scheduler
  * `list_active_tasks()`: Reports currently scheduled operations
  * `modify_task_schedule()`: Updates task timing
- **Technical Notes**:
  * Safe manipulation of system scheduler
  * Task priority preservation
  * Maintains task metadata during suspension

#### StopScheduledShutdown.py
- **Primary Purpose**: Interrupt automated shutdown sequence
- **Key Functions**:
  * `cancel_pending_shutdown()`: Stops shutdown timer
  * `notify_shutdown_cancelled()`: Records cancellation event
  * `reset_shutdown_flags()`: Clears shutdown indicators
- **Technical Notes**:
  * Works with both soft (scheduled) and hard (imminent) shutdowns
  * Preserves system state during cancellation
  * Implements authorization checks for shutdown manipulation

#### TurnEverythingOff.py
- **Primary Purpose**: Complete system shutdown
- **Key Functions**:
  * `save_system_state()`: Preserves operational context
  * `stop_all_services()`: Gracefully terminates running services
  * `flush_file_buffers()`: Ensures data integrity
  * `power_down_hardware()`: Initiates hardware shutdown
  * `schedule_delayed_shutdown()`: Sets future shutdown time
- **Technical Notes**:
  * Implements safe shutdown procedure to prevent data loss
  * Configurable shutdown stages for partial operation
  * Shutdown verification to confirm successful completion

#### RegisterNewWifi.sh
- **Primary Purpose**: Network configuration
- **Key Functions**:
  * `scan_available_networks()`: Discovers nearby WiFi networks
  * `connect_to_network(ssid, password)`: Establishes connection
  * `store_network_credentials()`: Securely saves connection information
  * `test_connectivity()`: Verifies successful connection
- **Technical Notes**:
  * Support for both WPA/WPA2/WPA3 encryption
  * Headless operation capability
  * Multiple network profiles with priority
  * Connection quality monitoring

### Utility Scripts (scripts/ subdirectory)

#### auto_capture.py
- **Primary Purpose**: Automated photo capture system
- **Key Functions**:
  * `load_capture_schedule()`: Reads photo schedule configuration
  * `execute_scheduled_capture()`: Takes photos at specified times
  * `adjust_capture_parameters()`: Modifies settings based on conditions
  * `log_capture_events()`: Records photo capture activity
- **Technical Notes**:
  * Integration with wildlife activity patterns
  * Adaptive scheduling based on historical success
  * Environment-aware parameter selection
  * Efficient resource utilization during idle periods

#### diagnostic.py
- **Primary Purpose**: Extended system diagnostics
- **Key Functions**:
  * `perform_deep_diagnostics()`: Comprehensive system check
  * `test_camera_subsystem()`: Validates imaging capabilities
  * `verify_storage_integrity()`: Checks storage subsystem
  * `diagnose_network_issues()`: Troubleshoots connectivity problems
  * `generate_detailed_report()`: Creates comprehensive analysis
- **Technical Notes**:
  * Root cause analysis capabilities
  * Historical performance comparison
  * Component stress testing
  * Repair recommendations

#### monitor_disk.py
- **Primary Purpose**: Storage management
- **Key Functions**:
  * `check_available_space()`: Monitors free storage
  * `identify_large_files()`: Finds space-consuming data
  * `implement_cleanup_policy()`: Applies storage retention rules
  * `alert_storage_issues()`: Notifies of capacity problems
- **Technical Notes**:
  * Multi-level threshold monitoring
  * Intelligent file importance assessment
  * Automated archive and cleanup
  * Storage trend analysis

#### remote_control.py
- **Primary Purpose**: Remote system management
- **Key Functions**:
  * `start_command_server()`: Initiates remote control listener
  * `authenticate_remote_client()`: Verifies authorized access
  * `execute_remote_command()`: Processes incoming instructions
  * `report_command_results()`: Returns operation outcomes
- **Technical Notes**:
  * Secure communication with encryption
  * Command authorization framework
  * Audit logging of all remote operations
  * Bandwidth-efficient protocol for field deployments

#### motion_detection.py
- **Primary Purpose**: Motion-triggered system functions
- **Key Functions**:
  * `monitor_motion_sensors()`: Processes motion detection input
  * `trigger_capture_on_motion()`: Initiates photography on movement
  * `analyze_motion_pattern()`: Interprets motion characteristics
  * `adjust_sensitivity()`: Tunes detection parameters
- **Technical Notes**:
  * False positive filtering algorithms
  * Animal size classification
  * Direction-of-movement tracking
  * Integration with attraction system for targeted operation

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Software Module](../core-components/software-module.md): Comprehensive documentation
  * [Configuration](../core-components/configuration.md): Settings used by scripts
  * [Power Management](../core-components/power-management.md): Power control integration
  * [Web Interface](../web-interface/core.md): UI-triggered operations
- **Depends On**:
  * System hardware interfaces
  * Linux utilities and system services
  * Camera drivers and libraries
  * Python runtime environment
  * File system and storage services
  * Network infrastructure
- **Used By**:
  * End users through web interface
  * Automated scheduling system
  * System services (systemd, cron)
  * Remote management tools
  * Mobile applications (via API)
  * Field maintenance tools

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Automated Wildlife Photography**:
   - **Description**: Setting up unattended wildlife monitoring
   - **Example**:
     ```python
     # Configure attraction mode for dawn/dusk (peak wildlife activity)
     import subprocess
     from datetime import datetime
     
     # Determine if we're in morning or evening hours
     current_hour = datetime.now().hour
     
     # Turn on attraction mode with appropriate settings
     if 5 <= current_hour <= 9:  # Morning
         subprocess.run(["python", "/opt/creaturebox/src/software/Attract_On.py", 
                        "--mode=gentle", "--duration=120"])
     elif 17 <= current_hour <= 21:  # Evening
         subprocess.run(["python", "/opt/creaturebox/src/software/Attract_On.py", 
                        "--mode=food-sounds", "--duration=120"])
     
     # Configure camera for current lighting conditions
     if current_hour < 7 or current_hour > 19:  # Low light
         camera_mode = "night"
     else:
         camera_mode = "daylight"
         
     # Start automated photography session
     subprocess.run(["python", "/opt/creaturebox/src/software/TakePhoto.py", 
                    f"--mode={camera_mode}", "--interval=30", "--count=20"])
     ```

2. **Remote System Management**:
   - **Description**: Administering system from a distance
   - **Example**:
     ```python
     # On management server/application
     import requests
     import json
     
     def send_command(device_id, command, parameters):
         """Send remote command to field-deployed CreatureBox"""
         url = f"https://api.creaturebox.net/devices/{device_id}/command"
         payload = {
             "command": command,
             "parameters": parameters,
             "auth_token": "secure-api-token"
         }
         
         response = requests.post(url, json=payload)
         return response.json()
     
     # Check system status
     status = send_command("cb-wildlife-park-05", "system_check", {})
     
     # If battery is low, disable non-essential functions
     if status["battery_level"] < 30:
         send_command("cb-wildlife-park-05", "power_conservation", {"mode": "aggressive"})
         
     # Download recent images
     send_command("cb-wildlife-park-05", "sync_images", 
                 {"since": "2025-03-07T00:00:00", "destination": "central-server"})
     ```

3. **System Maintenance and Diagnostics**:
   - **Description**: Troubleshooting system issues
   - **Example**:
     ```python
     # Enable debug mode for detailed logging
     subprocess.run(["python", "/opt/creaturebox/src/software/DebugMode.py", 
                    "--enable", "--log-level=verbose"])
     
     # Run comprehensive diagnostics
     subprocess.run(["python", "/opt/creaturebox/src/software/scripts/diagnostic.py", 
                    "--full", "--report-file=/var/log/creaturebox/diagnostics.json"])
     
     # Check power systems
     power_status = subprocess.run(
         ["python", "/opt/creaturebox/src/software/Measure_Power.py", "--full-report"],
         capture_output=True, text=True
     )
     
     # Analyze diagnostic results
     import json
     with open('/var/log/creaturebox/diagnostics.json', 'r') as f:
         diagnostic_results = json.load(f)
         
     # Take corrective action based on results
     if diagnostic_results["camera"]["status"] == "failed":
         subprocess.run(["python", "/opt/creaturebox/src/software/TurnEverythingOff.py", 
                        "--restart", "--component=camera"])
     ```

4. **Scheduled Operations Management**:
   - **Description**: Configuring automated system tasks
   - **Example**:
     ```python
     import subprocess
     import json
     
     # Define schedule for system operations
     schedule = [
         {
             "task": "capture",
             "time": "06:00",
             "days": "daily",
             "parameters": {
                 "mode": "morning",
                 "duration": 60,
                 "attraction": True
             }
         },
         {
             "task": "backup",
             "time": "12:00",
             "days": "Monday,Thursday",
             "parameters": {
                 "destination": "usb",
                 "type": "incremental"
             }
         },
         {
             "task": "power_conservation",
             "time": "22:00",
             "days": "daily",
             "parameters": {
                 "level": "maximum",
                 "duration": "8h"
             }
         }
     ]
     
     # Write schedule to configuration file
     with open('/opt/creaturebox/config/schedule.json', 'w') as f:
         json.dump(schedule, f, indent=2)
     
     # Apply the schedule to the system
     subprocess.run(["python", "/opt/creaturebox/src/software/Scheduler.py", 
                    "--load", "--config=/opt/creaturebox/config/schedule.json"])
     
     # Enable scheduled tasks
     subprocess.run(["python", "/opt/creaturebox/src/software/StartCron.py"])
     ```

5. **Battery-Optimized Field Deployment**:
   - **Description**: Configuring system for extended battery operation
   - **Example**:
     ```python
     # Setup power-optimized configuration
     
     # 1. Configure power thresholds
     with open('/opt/creaturebox/config/power_thresholds.conf', 'w') as f:
         f.write("CRITICAL_LEVEL=15\n")
         f.write("LOW_LEVEL=30\n")
         f.write("WIFI_MINIMUM=40\n")
         f.write("CONSERVATION_TRIGGER=50\n")
     
     # 2. Setup battery monitoring
     subprocess.run(["python", "/opt/creaturebox/src/software/Measure_Power.py", 
                    "--daemon", "--interval=300"])
     
     # 3. Configure power-saving scheduler
     power_schedule = [
         "0 9 * * * /opt/creaturebox/src/power/stop_lowpower.sh --temporary",
         "0 10-16 * * * /opt/creaturebox/src/software/TakePhoto.py --mode=eco --interval=1800",
         "0 17 * * * /opt/creaturebox/src/power/lowpower.sh --until='09:00'"
     ]
     
     with open('/tmp/power_crontab', 'w') as f:
         f.write("\n".join(power_schedule) + "\n")
     
     subprocess.run(["crontab", "/tmp/power_crontab"])
     
     # 4. Configure network power saving
     subprocess.run(["bash", "/opt/creaturebox/src/software/RegisterNewWifi.sh", 
                    "--power-save-mode=maximum", "--connect-interval=43200"])
     ```

</div>
</details>

## Best Practices for Script Usage

- Always use scripts through their documented interfaces rather than direct modification
- Maintain consistent error handling by using the error_handling.py utilities
- Check script return codes to verify successful operation
- Use the debug mode for troubleshooting rather than modifying scripts
- Reference the software_utils.py module for common functionality
- Follow the logging conventions for consistent troubleshooting
- Use the scheduler for automated operations rather than custom cron entries
- Test scripts in a safe environment before deploying to production systems
