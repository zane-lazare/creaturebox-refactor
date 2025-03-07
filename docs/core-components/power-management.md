---
layout: default
title: Power Management
parent: Core Components
nav_order: 2
permalink: /core-components/power-management/
---

# Power Management Module

{% include navigation.html %}

## Overview

The Power Management Module provides critical functionality for power control, conservation, and monitoring for the CreatureBox system, enabling efficient operation in remote wildlife observation deployments.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `src/power` directory contains scripts that manage the power-related functionality of the CreatureBox system. This module is essential for:

- Implementing power conservation strategies
- Managing power state transitions
- Controlling peripheral power usage
- Monitoring power consumption
- Enabling WiFi components selectively
- Supporting battery-powered operation

These scripts are crucial for field deployments where power efficiency is essential for extended operation without human intervention.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Purpose |
|----------|------|------|---------|
| low_in_one.sh | Shell | 1.2 KB | Combined low power mode script |
| lowpower.sh | Shell | 0.9 KB | Basic power conservation mode |
| powerup_wifi.sh | Shell | 0.7 KB | Selective WiFi activation |
| stop_lowpower.sh | Shell | 0.4 KB | Terminate low-power mode |

**Systemd Components**:
| Filename | Type | Purpose |
|----------|------|---------|
| lowpower.service | Service | Systemd service for low-power mode |
| lowpower.timer | Timer | Systemd timer for scheduled power management |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### low_in_one.sh
- **Primary Purpose**: Comprehensive power conservation solution
- **Key Functions**:
  * `disable_hdmi()`: Turns off HDMI output to save power
  * `disable_peripherals()`: Turns off non-essential USB devices
  * `slow_cpu()`: Reduces CPU clock speed
  * `monitor_temperature()`: Adjusts power based on temperature
  * `schedule_wakeup()`: Sets wake timer for future activation
- **Dependencies**:
  * System control utilities (vcgencmd, tvservice)
  * Process management utilities
- **Technical Notes**: Provides the most aggressive power savings mode suitable for extended field deployment

### lowpower.sh
- **Primary Purpose**: Basic power conservation mode
- **Key Functions**:
  * `power_down_usb()`: Disables USB port power
  * `throttle_cpu()`: Reduces CPU performance
  * `disable_leds()`: Turns off indicator LEDs
- **Dependencies**:
  * System control utilities
  * GPIO control libraries
- **Technical Notes**: Balances power saving with system availability, allowing faster recovery to full power

### powerup_wifi.sh
- **Primary Purpose**: Selectively activates WiFi
- **Key Functions**:
  * `check_battery()`: Verifies sufficient power before activation
  * `enable_wifi()`: Powers up WiFi hardware
  * `connect_known_networks()`: Establishes connection
  * `schedule_shutdown()`: Sets automatic WiFi shutdown timer
- **Dependencies**:
  * Network control utilities
  * Power monitoring tools
- **Technical Notes**: Implements intelligent power management for WiFi, one of the most power-hungry components

### stop_lowpower.sh
- **Primary Purpose**: Terminate low-power mode and restore normal operation
- **Key Functions**:
  * `restore_usb()`: Re-enables USB ports
  * `restore_cpu()`: Returns CPU to normal clock speed
  * `enable_hdmi()`: Turns on HDMI output if needed
  * `cancel_scheduled_tasks()`: Removes any scheduled power management tasks
- **Dependencies**:
  * System control utilities
  * Process management utilities
- **Technical Notes**: Used when human interaction is detected or for maintenance access

### lowpower.service
- **Primary Purpose**: Systemd service definition for power management
- **Key Attributes**:
  * Starts the low-power mode scripts
  * Defines dependencies and service behavior
  * Manages automatic restarts and failure handling
- **Dependencies**:
  * Systemd service management
- **Technical Notes**: Enables integration with the system service management

### lowpower.timer
- **Primary Purpose**: Systemd timer for scheduled power management
- **Key Attributes**:
  * Defines schedule for power management activation
  * Controls periodic power cycling
  * Coordinates with system calendar for timed events
- **Dependencies**:
  * Systemd timer management
- **Technical Notes**: Provides cron-like functionality for power management scheduling

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Software Module](../software-module.md): Uses power management functions for system control
  * [Configuration](../configuration.md): Gets power settings from configuration
  * [Deployment](../../deployment.md): Service configuration for power management
- **Depends On**:
  * System hardware interfaces
  * Linux power management utilities
  * Hardware-specific control libraries
  * Systemd for service management
- **Used By**:
  * Scheduled tasks for power conservation
  * [Web Interface](../../web-interface.md): For remote power management
  * System startup and shutdown processes

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Field Deployment Power Conservation**:
   - **Description**: Maximum power conservation for remote wildlife monitoring.
   - **Example**: 
     ```bash
     # Configure for minimum power usage during inactive periods
     ./low_in_one.sh --max-conservation
     
     # Schedule periodic wakeups for image capture
     ./low_in_one.sh --schedule-wakeup "0 6,18 * * *"
     ```

2. **Scheduled Network Connectivity**:
   - **Description**: Periodically enabling WiFi to upload captured images.
   - **Example**: 
     ```bash
     # Check battery levels and enable WiFi if sufficient power available
     ./powerup_wifi.sh --duration=15
     
     # Upload collected data
     rsync -avz /path/to/images/ remote:/backup/
     
     # Return to low power state
     ./lowpower.sh
     ```

3. **Temperature-adaptive Power Management**:
   - **Description**: Adjusting power consumption based on environmental conditions.
   - **Example**: 
     ```bash
     # Monitor system temperature and adjust power usage accordingly
     ./low_in_one.sh --temp-adaptive
     
     # In extreme temperatures, shut down non-essential components
     if [ $TEMP -gt 80 ]; then
       ./low_in_one.sh --critical-conservation
     fi
     ```

4. **Battery Level Response**:
   - **Description**: Taking action based on available power.
   - **Example**: 
     ```bash
     # Check current battery level
     BATTERY_PCT=$(cat /sys/class/power_supply/battery/capacity)
     
     # Apply appropriate power management strategy
     if [ $BATTERY_PCT -lt 20 ]; then
       ./low_in_one.sh --emergency-conservation
     elif [ $BATTERY_PCT -lt 50 ]; then
       ./lowpower.sh
     else
       # Normal operation
       ./powerup_wifi.sh --duration=30
     fi
     ```

5. **Maintenance Mode Activation**:
   - **Description**: Temporarily disabling power conservation for system maintenance.
   - **Example**: 
     ```bash
     # Detect maintenance trigger (e.g., specific button press)
     if [ -f /tmp/maintenance_requested ]; then
       # Disable power management
       ./stop_lowpower.sh
       
       # Enable all interfaces for maintenance
       systemctl start sshd.service
       ./powerup_wifi.sh
       
       # Set a timeout to return to low power mode
       (sleep 1800 && ./lowpower.sh) &
     fi
     ```

</div>
</details>

## Key Functionality
- Dynamic power state management
- WiFi power control
- Scheduled low-power mode activation
- System power optimization
- Temperature-adaptive power consumption
- Battery level monitoring and response