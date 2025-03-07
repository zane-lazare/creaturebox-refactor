# src/software/scripts Directory Documentation

## Directory Purpose
The `src/software/scripts` directory contains specialized utility scripts that extend the core functionality of the CreatureBox system. These scripts provide automated photo capture scheduling, system diagnostics, storage monitoring, remote control capabilities, and system health checks. They are designed to run as standalone utilities, scheduled tasks, or supporting components for the main application, enhancing the system's reliability, maintainability, and feature set.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| auto_capture.py | Python | 1.1 KB | Automated photo capture scheduler |
| diagnostic.py | Python | 1.4 KB | System diagnostic utility |
| monitor_disk.py | Python | 0.8 KB | Storage usage monitoring |
| remote_control.py | Python | 1.2 KB | Remote command interface |
| system_check.py | Python | 0.9 KB | System health validation |

## Detailed File Descriptions

### auto_capture.py
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
  * Handles schedule conflicts and prioritization

### diagnostic.py
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
  * Includes severity ratings for identified issues
  * Suggests remediation steps for common problems

### monitor_disk.py
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
  * Ensures critical system operation by maintaining free space
  * Uses space prediction algorithm to anticipate storage needs

### remote_control.py
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
  * Includes timeout and rate limiting for protection
  * Enables remote administration of deployed systems

### system_check.py
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
  * Escalates unresolvable problems appropriately
  * Maintains system health log for trend analysis

## Relationship Documentation
- **Related To**:
  * src/software/*.py (core software components)
  * src/web/services/ (background services)
- **Depends On**:
  * src/config/ (configuration files)
  * System utilities and Python libraries
  * Hardware-specific functionality
- **Used By**:
  * Scheduled tasks (cron)
  * Web interface indirectly
  * System maintenance processes

## Use Cases
1. **Automated Wildlife Photography**:
   - **Implementation**: The auto_capture.py script enables unattended photo capture based on configurable schedules.
   - **Example**:
     ```
     # Schedule configuration in schedule_settings.csv:
     schedule_id,operation,time,days,parameters,enabled,description,last_run
     morning,photo,06:30,daily,{"resolution":"high","count":5},true,"Morning wildlife activity",2025-03-07T06:30:00
     evening,photo,19:45,weekday,{"resolution":"high","night_mode":true},true,"Evening feeding time",2025-03-07T19:45:00
     ```
     The auto_capture.py script, when run as a background service, will automatically take photos at the configured times.

2. **Preventative System Maintenance**:
   - **Implementation**: The system_check.py and monitor_disk.py scripts work together to ensure the system remains healthy.
   - **Example**:
     ```python
     # In crontab:
     # Run system check every hour
     0 * * * * /usr/bin/python3 /opt/creaturebox/src/software/scripts/system_check.py
     
     # Run disk monitoring every 6 hours
     0 */6 * * * /usr/bin/python3 /opt/creaturebox/src/software/scripts/monitor_disk.py
     ```
     These scheduled checks identify and address issues before they impact system operation.

3. **Remote Field System Management**:
   - **Implementation**: The remote_control.py script enables secure remote management of deployed systems.
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
     print(f"Diagnostic status: {result['status']}")
     ```

4. **System Troubleshooting**:
   - **Implementation**: The diagnostic.py script provides comprehensive system analysis for troubleshooting.
   - **Example**:
     ```bash
     # Run by field technician to diagnose issues
     $ python3 /opt/creaturebox/src/software/scripts/diagnostic.py --full --report=/tmp/diagnostic_report.html
     
     Running full system diagnostic...
     Checking camera functionality... PASS
     Checking storage health... WARNING (90% full)
     Checking network connectivity... PASS
     Checking power status... PASS
     
     Diagnostic complete. Report saved to /tmp/diagnostic_report.html
     Recommended actions:
     - Run storage cleanup to free space
     ```
     The generated report provides detailed information for resolving the identified issues.
