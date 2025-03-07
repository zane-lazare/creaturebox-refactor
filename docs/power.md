# Power Management Module Documentation

## Overview
The `power` directory contains scripts and services for power management in the CreatureBox system.

## File Inventory

### Shell Scripts
- `low_in_one.sh`: Low-power mode initialization
- `lowpower.sh`: Core low-power mode script
- `powerup_wifi.sh`: WiFi power management
- `stop_lowpower.sh`: Terminate low-power mode

### Systemd Components
- `lowpower.service`: Systemd service for low-power mode
- `lowpower.timer`: Systemd timer for scheduled power management

### Supplementary Files
- `power.md`: Power management documentation

## Key Functionality
- Dynamic power state management
- WiFi power control
- Scheduled low-power mode activation
- System power optimization

## Relationships
- Systemd services coordinate power management
- Scripts provide modular power control mechanisms
