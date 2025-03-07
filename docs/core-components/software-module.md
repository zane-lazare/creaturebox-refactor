---
layout: default
title: Software Module
parent: Core Components
nav_order: 3
permalink: /core-components/software-module/
---

# Software Module

{% include navigation.html %}

## Overview

The Software Module contains the core operational scripts that control the CreatureBox hardware, including the camera system, scheduling, and system management utilities.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `src/software` directory houses the primary operational scripts that drive the CreatureBox system functionality. This module is responsible for:

- Controlling the attraction mode for wildlife photography
- Managing the camera capture process
- Scheduling system operations
- Providing debugging and diagnostic capabilities
- Managing power consumption monitoring
- Implementing system backup functionality
- Controlling scheduled shutdown operations
- Network configuration and management
- System-wide power control

These scripts form the functional core of the CreatureBox system, connecting the hardware components with the user interface and automation systems.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

### Main Scripts

| Filename | Type | Size | Purpose |
|----------|------|------|---------|
| Attract_On.py | Python | 2.3 KB | Enables attraction mode |
| Attract_Off.py | Python | 1.8 KB | Disables attraction mode |
| Backup_Files.py | Python | 3.1 KB | System data backup utility |
| DebugMode.py | Python | 2.5 KB | Diagnostic functionality |
| Measure_Power.py | Python | 1.7 KB | Power monitoring |
| Scheduler.py | Python | 4.2 KB | Task scheduling system |
| TakePhoto.py | Python | 3.8 KB | Camera control interface |
| StartCron.py | Python | 0.9 KB | Enables scheduled tasks |
| StopCron.py | Python | 0.7 KB | Disables scheduled tasks |
| StopScheduledShutdown.py | Python | 1.1 KB | Cancels pending shutdown |
| TurnEverythingOff.py | Python | 1.5 KB | Complete system shutdown |
| RegisterNewWifi.sh | Shell | 1.2 KB | WiFi configuration |
| readme.md | Markdown | 0.5 KB | Module documentation |

### Scripts Subdirectory

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| auto_capture.py | Python | 1.1 KB | Automated photo capture scheduler |
| diagnostic.py | Python | 1.4 KB | System diagnostic utility |
| monitor_disk.py | Python | 0.8 KB | Storage usage monitoring |
| remote_control.py | Python | 1.2 KB | Remote command interface |
| system_check.py | Python | 0.9 KB | System health validation |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### Attraction Mode Control

#### Attract_On.py / Attract_Off.py
- **Primary Purpose**: Control the attraction mechanisms (lights, sounds, etc.)
- **Key Functions**:
  * `start_attraction_sequence()`: Activates lights and sounds in sequence
  * `stop_attraction_sequence()`: Deactivates attraction mechanisms
  * `check_attraction_status()`: Verifies current state
- **Dependencies**:
  * Hardware control libraries
  * Configuration settings from src/config
- **Technical Notes**: Uses PWM for LED control and audio libraries for sound playback

### System Management

#### Backup_Files.py
- **Primary Purpose**: Creates backups of critical system data
- **Key Functions**:
  * `backup_configuration()`: Copies configuration files
  * `backup_images()`: Archives captured images
  * `schedule_backup()`: Sets up recurring backup
- **Dependencies**:
  * File system access
  * Storage service from web module
- **Technical Notes**: Supports both local and remote backup locations

#### DebugMode.py
- **Primary Purpose**: Enables detailed system diagnostics
- **Key Functions**:
  * `enable_debug_logging()`: Increases log verbosity
  * `run_diagnostics()`: Performs hardware tests
  * `generate_debug_report()`: Creates diagnostic summary
- **Dependencies**:
  * System utilities
  * Logging framework
- **Technical Notes**: Can significantly increase log file size when enabled

### Measurement and Monitoring

#### Measure_Power.py
- **Primary Purpose**: Monitors system power consumption
- **Key Functions**:
  * `read_power_sensors()`: Gets current power readings
  * `log_power_usage()`: Records power data
  * `check_battery_levels()`: Verifies battery status
- **Dependencies**:
  * Hardware sensor interfaces
  * Data logging services
- **Technical Notes**: Calibrated for specific power monitoring hardware

### Task Scheduling

#### Scheduler.py
- **Primary Purpose**: Controls timed operations
- **Key Functions**:
  * `load_schedule()`: Reads schedule configuration
  * `add_task()`: Creates new scheduled task
  * `remove_task()`: Cancels scheduled task
  * `run_pending()`: Executes due tasks
- **Dependencies**:
  * System cron service
  * Configuration module
- **Technical Notes**: Uses both cron for persistence and in-memory scheduling for precision

### Camera Control

#### TakePhoto.py
- **Primary Purpose**: Interface to camera hardware
- **Key Functions**:
  * `initialize_camera()`: Sets up camera with parameters
  * `capture_image()`: Takes single photo
  * `capture_sequence()`: Takes series of photos
  * `adjust_settings()`: Changes camera parameters
- **Dependencies**:
  * Camera hardware drivers
  * Configuration settings
  * Storage services
- **Technical Notes**: Supports multiple camera models through abstraction layer

### System Control

#### StartCron.py / StopCron.py
- **Primary Purpose**: Manage system scheduled tasks
- **Key Functions**:
  * `enable_cron_jobs()`: Activates all scheduled tasks
  * `disable_cron_jobs()`: Deactivates all scheduled tasks
- **Dependencies**:
  * System cron service
- **Technical Notes**: Requires root privileges to modify cron

#### StopScheduledShutdown.py
- **Primary Purpose**: Prevents automated system shutdown
- **Key Functions**:
  * `cancel_shutdown()`: Removes pending shutdown commands
  * `notify_cancelled()`: Logs and notifies of cancellation
- **Dependencies**:
  * System shutdown service
- **Technical Notes**: Works by identifying and killing shutdown timer processes

#### TurnEverythingOff.py
- **Primary Purpose**: Safe system shutdown
- **Key Functions**:
  * `save_state()`: Preserves current system state
  * `stop_services()`: Gracefully terminates services
  * `power_down()`: Initiates hardware shutdown
- **Dependencies**:
  * All system services
  * Power control module
- **Technical Notes**: Ensures data integrity before power off

### Network Configuration

#### RegisterNewWifi.sh
- **Primary Purpose**: Configure WiFi connectivity
- **Key Functions**:
  * `scan_networks()`: Identifies available networks
  * `save_credentials()`: Stores network authentication
  * `connect_network()`: Establishes connection
- **Dependencies**:
  * Network interfaces
  * wpa_supplicant service
- **Technical Notes**: Can operate in headless mode with predefined credentials

### Specialized Utility Scripts

#### auto_capture.py
- **Primary Purpose**: Implements a flexible scheduling system for automated photo capture
- **Key Functions**:
  * `load_schedule()`: Loads capture schedule from configuration
  * `run_scheduler()`: Main loop that checks schedule and triggers captures
  * `perform_scheduled_capture(settings)`: Executes scheduled photo capture
  * `update_last_run(schedule_id)`: Updates schedule execution history
- **Dependencies**:
  * Python datetime, time modules
  * src/config/schedule_settings.csv
  * src/software/Take_Photo.py
- **Technical Notes**: 
  * Uses non-blocking design to handle multiple schedules
  * Supports complex scheduling patterns (daily, weekday, specific days)
  * Logs all activity for audit trail

#### diagnostic.py
- **Primary Purpose**: Performs comprehensive system diagnostics to identify issues
- **Key Functions**:
  * `run_full_diagnostic()`: Executes all diagnostic checks
  * `check_camera_functionality()`: Validates camera operation
  * `check_storage_health()`: Tests storage subsystem
  * `check_network_connectivity()`: Validates network connections
  * `check_power_status()`: Monitors power system health
  * `generate_diagnostic_report(output_path)`: Creates detailed report
- **Dependencies**:
  * Python os, sys, subprocess modules
  * picamera (for camera diagnostics)
  * RPi.GPIO (for hardware checks)
- **Technical Notes**: 
  * Can run as standalone utility or called by web interface
  * Captures detailed system information for troubleshooting

#### monitor_disk.py
- **Primary Purpose**: Monitors storage usage and triggers cleanup when necessary
- **Key Functions**:
  * `check_disk_usage()`: Gets current storage utilization
  * `get_threshold_settings()`: Loads threshold configuration
  * `trigger_cleanup(level)`: Initiates appropriate cleanup action
  * `send_storage_alert(level, details)`: Sends notification about storage issues
- **Dependencies**:
  * Python os, shutil modules
  * src/software/Backup_Files.py
  * src/web/services/storage.py
- **Technical Notes**: 
  * Implements multi-level thresholds (warning, critical)
  * Supports automatic cleanup policies

#### remote_control.py
- **Primary Purpose**: Provides a secure remote command interface for field-deployed systems
- **Key Functions**:
  * `start_control_server(port)`: Starts secure command listener
  * `authenticate_client(client_id, token)`: Validates remote client
  * `execute_command(command, params)`: Safely executes remote commands
  * `log_command(client_id, command, result)`: Records command execution
- **Dependencies**:
  * Python socket, ssl, json modules
  * paramiko (for SSH functionality)
  * src/config/controls.txt (for permissions)
- **Technical Notes**: 
  * Implements strong authentication and encryption
  * Provides restricted command set for security

#### system_check.py
- **Primary Purpose**: Performs regular system health validation for reliable operation
- **Key Functions**:
  * `perform_system_check()`: Runs basic system validation
  * `check_temperature()`: Monitors system temperature
  * `check_processes()`: Verifies critical processes are running
  * `check_memory_usage()`: Monitors memory utilization
  * `perform_corrective_action(issue)`: Attempts to resolve identified issues
- **Dependencies**:
  * Python psutil, os, subprocess modules
  * logging module
  * src/software/Shut_Down.py (for critical issues)
- **Technical Notes**: 
  * Designed to run as a periodic background task
  * Implements self-healing capabilities for common issues

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Configuration Module](./configuration.md): System settings used by software scripts
  * [Power Management Module](./power-management.md): Power management integrated with software control
  * [Web Interface](../../web-interface.md): Web application calls these scripts
- **Depends On**:
  * System hardware interfaces
  * Linux system services (cron, systemd)
  * Camera hardware drivers
  * Hardware-specific functionality
  * Storage and file system services
- **Used By**:
  * Web interface for remote control
  * System automation and scheduling services
  * User-initiated operations
  * Scheduled tasks (cron)
  * System maintenance processes

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Wildlife Photography Session**:
   - **Description**: Setting up the system for automated wildlife photography.
   - **Example**: 
     ```python
     # First enable attraction mode
     subprocess.run(["python", "/path/to/Attract_On.py"])
     
     # Schedule automated photo captures
     with open('/etc/crontab', 'a') as cron:
         cron.write("0 * * * * python /path/to/TakePhoto.py")
     
     # Enable scheduled tasks
     subprocess.run(["python", "/path/to/StartCron.py"])
     ```

2. **System Maintenance**:
   - **Description**: Performing system backup and diagnostics.
   - **Example**: 
     ```python
     # Run diagnostics 
     subprocess.run(["python", "/path/to/DebugMode.py", "--diagnose"])
     
     # Backup critical data
     subprocess.run(["python", "/path/to/Backup_Files.py", "--full"])
     ```

3. **Power Management**:
   - **Description**: Monitoring and managing system power consumption.
   - **Example**: 
     ```python
     # Check current power usage
     result = subprocess.run(["python", "/path/to/Measure_Power.py"], 
                            capture_output=True, text=True)
     
     # If power is low, shutdown non-essential services
     if "LOW BATTERY" in result.stdout:
         subprocess.run(["python", "/path/to/TurnEverythingOff.py", "--except-core"])
     ```

4. **Network Configuration**:
   - **Description**: Setting up new network connection.
   - **Example**: 
     ```bash
     # Configure new WiFi network
     ./RegisterNewWifi.sh --ssid "WildlifeNetwork" --password "secure-password"
     ```

5. **Automated Wildlife Photography**:
   - **Description**: Configuring unattended photo capture based on schedules.
   - **Example**:
     ```
     # Schedule configuration in schedule_settings.csv:
     schedule_id,operation,time,days,parameters,enabled,description,last_run
     morning,photo,06:30,daily,{"resolution":"high","count":5},true,"Morning wildlife activity",2025-03-07T06:30:00
     evening,photo,19:45,weekday,{"resolution":"high","night_mode":true},true,"Evening feeding time",2025-03-07T19:45:00
     ```
     The auto_capture.py script, when run as a background service, will automatically take photos at the configured times.

6. **Remote Field System Management**:
   - **Description**: Managing deployed systems remotely.
   - **Example**: 
     ```python
     # From a management system:
     import json
     import requests
     
     def send_remote_command(device_id, command, params):
         url = f"https://{device_id}.field-systems.org:8443/command"
         data = {
             "command": command,
             "parameters": params,
             "auth_token": "secure_token_here"
         }
         response = requests.post(url, json=data, verify=True)
         return response.json()
     
     # Trigger a diagnostic check remotely
     result = send_remote_command(
         "creaturebox-42", 
         "run_diagnostic", 
         {"generate_report": True}
     )
     ```

</div>
</details>

## Core Functionalities
- System scheduling and automation
- Power management and monitoring
- Backup and recovery operations
- Debug and diagnostic tools
- Network configuration
- Camera control and imaging capabilities
- Remote system management
- Health monitoring and self-healing
- Storage management