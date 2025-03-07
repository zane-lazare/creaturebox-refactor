# Software Module Documentation

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

These scripts form the functional core of the CreatureBox system, connecting the hardware components with the user interface and automation systems.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

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

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Configuration Module](./configuration.md): System settings used by software scripts
  * [Power Management Module](./power-management.md): Power management integrated with software control
  * [Source Directory](../src.md): Part of the source code structure
- **Depends On**:
  * System hardware interfaces
  * Linux system services (cron, systemd)
  * Camera hardware drivers
- **Used By**:
  * [Web Interface](../src-web.md): Web application calls these scripts
  * System automation and scheduling services
  * User-initiated operations

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

</div>
</details>
