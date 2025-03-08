---
layout: default
title: Power Management Files
parent: Power Management
nav_order: 1
permalink: /src/power/files/
---

# Power Management Files Documentation

{% include navigation.html %}

## Overview

The Power Management Files in the `src/power` directory provide essential functionality for controlling power usage, implementing conservation strategies, and managing power states for the CreatureBox system, which is crucial for field deployments with limited power availability.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The power management files serve critical functions for the CreatureBox system's operation in resource-constrained environments:

- Enable operation on battery power for extended periods
- Implement intelligent power conservation strategies
- Provide selective activation of power-hungry components
- Monitor and respond to system power state and battery levels
- Schedule power-related operations to optimize energy usage
- Support field deployments where power availability is limited
- Extend operational longevity in remote wildlife observation scenarios

These scripts are the foundation of the system's ability to operate autonomously in the field without frequent battery replacement or recharging.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| low_in_one.sh | Shell | 1.2 KB | Comprehensive power conservation script |
| lowpower.sh | Shell | 0.9 KB | Basic power conservation implementation |
| powerup_wifi.sh | Shell | 0.7 KB | Selective WiFi activation control |
| stop_lowpower.sh | Shell | 0.4 KB | Power conservation mode termination |
| power_monitor.py | Python | 2.1 KB | Battery and power monitoring utility |
| power_scheduler.py | Python | 1.8 KB | Power event scheduling system |
| lowpower.service | Config | 0.5 KB | Systemd service definition |
| lowpower.timer | Config | 0.3 KB | Systemd timer configuration |
| battery_threshold.conf | Config | 0.4 KB | Battery level threshold settings |
| peripheral_power.py | Python | 1.4 KB | Peripheral device power control |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### Shell Scripts

#### low_in_one.sh
- **Primary Purpose**: Comprehensive power conservation solution
- **Key Functions**:
  * `disable_hdmi()`: Turns off HDMI output
  * `disable_peripherals()`: Powers down non-essential USB devices
  * `slow_cpu()`: Reduces CPU clock speed
  * `monitor_temperature()`: Temperature-based power adjustments
  * `schedule_wakeup()`: Sets system wake timer
  * `enable_power_led_heartbeat()`: Configures LED for heartbeat pattern
- **Usage Examples**:
  * `./low_in_one.sh --max-conservation`: Maximum power saving
  * `./low_in_one.sh --schedule-wakeup "0 6,18 * * *"`: Schedule wake times
  * `./low_in_one.sh --temp-adaptive`: Temperature-based conservation
- **Technical Notes**:
  * Most comprehensive power saving implementation
  * Uses hardware-specific optimization techniques
  * Suitable for long-term field deployment

#### lowpower.sh
- **Primary Purpose**: Basic power conservation mode
- **Key Functions**:
  * `power_down_usb()`: Disables USB port power
  * `throttle_cpu()`: Reduces CPU performance
  * `disable_leds()`: Turns off indicator LEDs
  * `configure_sleep_timer()`: Sets sleep parameters
- **Usage Examples**:
  * `./lowpower.sh`: Apply standard power saving
  * `./lowpower.sh --moderate`: Apply moderate conservation
  * `./lowpower.sh --duration=3600`: Conserve for specific period
- **Technical Notes**:
  * Lighter implementation of power saving
  * Faster return to operational state
  * Good balance of conservation and availability

#### powerup_wifi.sh
- **Primary Purpose**: Selective WiFi activation
- **Key Functions**:
  * `check_battery()`: Verifies sufficient power
  * `enable_wifi()`: Powers up WiFi hardware
  * `connect_known_networks()`: Establishes connection
  * `schedule_shutdown()`: Sets automatic WiFi shutdown timer
- **Usage Examples**:
  * `./powerup_wifi.sh --duration=15`: Enable WiFi for 15 minutes
  * `./powerup_wifi.sh --min-battery=30`: Only enable if battery above 30%
  * `./powerup_wifi.sh --force`: Enable regardless of battery level
- **Technical Notes**:
  * WiFi is one of the most power-hungry components
  * Implements intelligent power management for connectivity
  * Includes safeguards against battery depletion

#### stop_lowpower.sh
- **Primary Purpose**: Terminate power conservation mode
- **Key Functions**:
  * `restore_usb()`: Re-enables USB ports
  * `restore_cpu()`: Returns CPU to normal clock speed
  * `enable_hdmi()`: Turns on HDMI output if needed
  * `cancel_scheduled_tasks()`: Removes power management tasks
- **Usage Examples**:
  * `./stop_lowpower.sh`: Return to normal power state
  * `./stop_lowpower.sh --keep-scheduled`: Maintain scheduled tasks
  * `./stop_lowpower.sh --gradual`: Gradually ramp up power usage
- **Technical Notes**:
  * Used when human interaction is detected
  * Provides full system capabilities for maintenance
  * Can be triggered remotely or by physical interaction

### Python Utilities

#### power_monitor.py
- **Primary Purpose**: Power and battery status monitoring
- **Key Functions**:
  * Real-time battery level monitoring
  * Power consumption tracking
  * Alert generation for critical levels
  * Data logging for power usage patterns
  * Health assessment of power system
- **Usage Examples**:
  * `python power_monitor.py --daemon`: Run as background service
  * `python power_monitor.py --alert-threshold=20`: Set custom alert level
  * `python power_monitor.py --log-file=/var/log/power.log`: Custom logging
- **Technical Notes**:
  * Interfaces with hardware monitoring circuits
  * Provides data for power-related decisions
  * Compatible with various battery monitoring systems

#### power_scheduler.py
- **Primary Purpose**: Schedule power-related events
- **Key Functions**:
  * Time-based power state transitions
  * Conditional power event scheduling
  * Sunrise/sunset-aware power management
  * Coordination with system activity
- **Usage Examples**:
  * `python power_scheduler.py --add-schedule "0 22 * * * lowpower.sh"` 
  * `python power_scheduler.py --sunset-action "lowpower.sh --max"`
  * `python power_scheduler.py --list-schedules`
- **Technical Notes**:
  * More sophisticated than cron for power events
  * Considers system state when executing actions
  * Integrates with system calendar for optimization

#### peripheral_power.py
- **Primary Purpose**: Control power to peripheral devices
- **Key Functions**:
  * Selective peripheral activation
  * Power sequencing for peripherals
  * Device-specific power optimization
  * USB device power management
- **Usage Examples**:
  * `python peripheral_power.py --enable=camera`
  * `python peripheral_power.py --disable=all`
  * `python peripheral_power.py --status`
- **Technical Notes**:
  * Manages devices via GPIO control lines
  * Supports USB hub power control
  * Provides fine-grained device power management

### Configuration Files

#### lowpower.service
- **Primary Purpose**: Systemd service definition
- **Key Settings**:
  * `ExecStart`: Command to execute
  * `Restart`: Restart behavior
  * `Type`: Service type
  * `User`: Execution context
  * Dependencies and ordering requirements
- **Technical Notes**:
  * Enables integration with system service management
  * Provides automatic startup capability
  * Supports proper dependency handling

#### lowpower.timer
- **Primary Purpose**: Systemd timer for scheduled activation
- **Key Settings**:
  * `OnCalendar`: Scheduled activation times
  * `AccuracySec`: Timing precision
  * `Persistent`: Behavior on missed events
  * `Unit`: Service to trigger
- **Technical Notes**:
  * Provides cron-like functionality
  * Coordinates with system calendar for timed events
  * Handles system sleep and wake coordination

#### battery_threshold.conf
- **Primary Purpose**: Battery level threshold configuration
- **Key Settings**:
  * `CRITICAL_LEVEL`: Emergency power conservation trigger
  * `LOW_LEVEL`: Activate power saving measures
  * `WIFI_MINIMUM`: Minimum to allow WiFi activation
  * `NORMAL_OPERATION`: Resume standard operation level
- **Technical Notes**:
  * Read by multiple power management components
  * Simple key-value format
  * Customizable for different battery capacities

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Power Management Module](../core-components/power-management.md): Comprehensive documentation
  * [Software Module](../core-components/software-module.md): Uses power management
  * [Web Interface](../web-interface/core.md): UI for power management
  * [Configuration](../core-components/configuration.md): Power-related settings
- **Depends On**:
  * System hardware capabilities
  * Linux power management subsystems
  * Hardware-specific control utilities (vcgencmd, tvservice)
  * Battery monitoring hardware
  * Systemd for service management
- **Used By**:
  * System scheduler for power state transitions
  * Camera control system for power optimization
  * Web interface for remote power management
  * Automated operations for energy efficiency
  * System startup and shutdown sequences

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Long-term Field Deployment**:
   - **Description**: Setting up for extended operation on battery power
   - **Example**:
     ```bash
     # Install power management components
     sudo cp lowpower.service /etc/systemd/system/
     sudo cp lowpower.timer /etc/systemd/system/
     sudo systemctl daemon-reload
     
     # Configure for maximum conservation
     sudo cp battery_threshold.conf /etc/creaturebox/
     
     # Enable power management scheduling
     sudo systemctl enable lowpower.timer
     sudo systemctl start lowpower.timer
     
     # Configure activity schedule
     python power_scheduler.py --add-schedule "0 6 * * * powerup_wifi.sh --duration=30"
     python power_scheduler.py --add-schedule "0 18 * * * powerup_wifi.sh --duration=30"
     ```

2. **Solar-powered Operation**:
   - **Description**: Adapting power usage to available solar energy
   - **Example**:
     ```bash
     # Monitor battery and adjust power usage
     python power_monitor.py --daemon --log-file=/var/log/power.log
     
     # Set up conditional power management
     cat > /etc/cron.hourly/solar_power_management << EOF
     #!/bin/bash
     
     BATTERY_LEVEL=$(python -c "import power_monitor; print(power_monitor.get_battery_level())")
     SOLAR_OUTPUT=$(python -c "import power_monitor; print(power_monitor.get_solar_output())")
     
     if [ $SOLAR_OUTPUT -lt 500 ] && [ $BATTERY_LEVEL -lt 50 ]; then
       /opt/creaturebox/src/power/lowpower.sh --max-conservation
     elif [ $SOLAR_OUTPUT -gt 2000 ] && [ $BATTERY_LEVEL -gt 80 ]; then
       /opt/creaturebox/src/power/stop_lowpower.sh
     fi
     EOF
     chmod +x /etc/cron.hourly/solar_power_management
     ```

3. **Remote Power Management**:
   - **Description**: Managing power states via web interface
   - **Example**:
     ```python
     # In web interface route implementation
     @app.route('/api/power/state', methods=['POST'])
     def set_power_state():
         state = request.json.get('state')
         duration = request.json.get('duration', 0)
         
         if state == 'low':
             subprocess.run(['/opt/creaturebox/src/power/lowpower.sh'])
             return jsonify({"status": "Power conservation mode activated"})
         elif state == 'normal':
             subprocess.run(['/opt/creaturebox/src/power/stop_lowpower.sh'])
             return jsonify({"status": "Normal power mode activated"})
         elif state == 'wifi':
             subprocess.run(['/opt/creaturebox/src/power/powerup_wifi.sh', 
                            f'--duration={duration}'])
             return jsonify({"status": f"WiFi activated for {duration} minutes"})
     ```

4. **Temperature-adaptive Power Management**:
   - **Description**: Adjusting power usage based on environmental conditions
   - **Example**:
     ```bash
     #!/bin/bash
     # In low_in_one.sh implementation
     
     monitor_temperature() {
         while true; do
             TEMP=$(vcgencmd measure_temp | cut -d= -f2 | cut -d\' -f1)
             
             if (( $(echo "$TEMP > 75" | bc -l) )); then
                 # Critical temperature - maximum conservation
                 disable_hdmi
                 slow_cpu 600
                 disable_peripherals
             elif (( $(echo "$TEMP > 65" | bc -l) )); then
                 # High temperature - moderate conservation
                 slow_cpu 800
                 disable_non_essential_peripherals
             elif (( $(echo "$TEMP < 45" | bc -l) )); then
                 # Normal temperature - standard operation
                 restore_cpu
             fi
             
             sleep 300
         done
     }
     ```

5. **Peripheral Power Sequencing**:
   - **Description**: Efficiently managing power to peripheral devices
   - **Example**:
     ```python
     # In peripheral_power.py
     def camera_capture_sequence():
         """Power sequence for taking an image with minimal power use"""
         try:
             # Power up camera
             enable_device('camera')
             time.sleep(2)  # Allow camera to initialize
             
             # Take photo
             capture_image()
             
             # Power down camera
             disable_device('camera')
             
             # Briefly power up WiFi if battery sufficient
             battery_level = get_battery_level()
             if battery_level > 40:
                 enable_device('wifi')
                 upload_image()
                 disable_device('wifi')
             
             return True
         except Exception as e:
             logging.error(f"Camera sequence failed: {e}")
             # Ensure devices are powered down on error
             disable_device('camera')
             disable_device('wifi')
             return False
     ```

</div>
</details>

## Power Management Best Practices

- Implement graceful shutdown procedures to prevent data corruption
- Use sensor data to adapt power management to environmental conditions
- Prioritize critical system functions when power is limited
- Consider time-of-day power usage patterns for scheduling
- Implement proper error handling for power-related operations
- Test power management strategies in controlled environment before field deployment
- Use power monitoring to validate the effectiveness of conservation strategies
- Maintain detailed logs of power state transitions for troubleshooting
