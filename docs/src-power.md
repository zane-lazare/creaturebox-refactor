# src/power Directory Documentation

## Directory Purpose
The `src/power` directory contains shell scripts and utilities for managing power-related operations in the CreatureBox system. These scripts enable efficient power management, which is critical for field deployments where the system may operate on battery power or in energy-constrained environments. The power management capabilities help extend battery life, enable graceful recovery from power loss, and provide features for scheduled power cycling to conserve energy during periods of inactivity.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| low_in_one.sh | Shell Script | 0.7 KB | Combined low power mode script |
| lowpower.sh | Shell Script | 0.5 KB | Basic low power mode |
| powerup_wifi.sh | Shell Script | 0.3 KB | Re-enable WiFi after power saving |

## Detailed File Descriptions

### low_in_one.sh
- **Primary Purpose**: Provides a comprehensive power-saving mode that combines multiple power reduction techniques
- **Key Functions**:
  * Disables unnecessary system services
  * Configures CPU governor for power efficiency
  * Turns off WiFi and Bluetooth
  * Disables HDMI output
  * Reduces LED activity
- **Dependencies**:
  * Raspberry Pi OS
  * systemd
  * rfkill (for wireless control)
- **Technical Notes**: 
  * Requires sudo/root access to modify system settings
  * Designed for maximum battery conservation
  * Logs all actions to system journal
  * Includes safety checks before disabling components

### lowpower.sh
- **Primary Purpose**: Implements basic power-saving mode with minimal impact on functionality
- **Key Functions**:
  * Configures CPU to run at lower frequency
  * Disables HDMI output
  * Reduces LED activity
  * Maintains network connectivity
- **Dependencies**:
  * Raspberry Pi OS
  * systemd
- **Technical Notes**: 
  * Balanced approach between power saving and functionality
  * Can be run as part of scheduled operations
  * Designed for temporary power reduction

### powerup_wifi.sh
- **Primary Purpose**: Restores WiFi connectivity after it has been disabled for power saving
- **Key Functions**:
  * Re-enables WiFi hardware via rfkill
  * Restarts networking services
  * Verifies connectivity
- **Dependencies**:
  * rfkill
  * systemd
  * Raspberry Pi OS networking
- **Technical Notes**: 
  * Used primarily after low_in_one.sh has disabled WiFi
  * Includes retry mechanism for reliable recovery
  * Times out if WiFi cannot be restored to prevent power drain

## Relationship Documentation
- **Related To**:
  * src/software/Shut_Down.py (system shutdown process)
  * src/web/utils/system.py (system control utilities)
- **Depends On**:
  * System utilities (rfkill, systemctl)
  * Hardware-specific features (Raspberry Pi power management)
- **Used By**:
  * src/web/routes/system.py (API endpoints for power control)
  * Scheduler for automatic power management
  * Installation scripts for system configuration

## Use Cases
1. **Extended Field Deployment**:
   - **Implementation**: The low_in_one.sh script provides maximum power saving for battery-powered installations.
   - **Example**:
     ```bash
     # Schedule aggressive power saving during nighttime hours
     # in crontab:
     0 20 * * * /opt/creaturebox/src/power/low_in_one.sh
     0 6 * * * /opt/creaturebox/src/power/powerup_wifi.sh
     ```
     This setup reduces power consumption at night and restores full functionality in the morning.

2. **Battery Conservation During Inactivity**:
   - **Implementation**: The lowpower.sh script provides moderate power saving while maintaining essential functionality.
   - **Example**:
     ```python
     # In system control API:
     def activate_low_power_mode():
         if battery_level < 30:
             subprocess.call(['/opt/creaturebox/src/power/lowpower.sh'])
             return {"status": "low power mode activated", "reason": "low battery"}
         return {"status": "normal power mode maintained"}
     ```

3. **Network Recovery After Power Saving**:
   - **Implementation**: The powerup_wifi.sh script enables restoration of connectivity for remote management.
   - **Example**:
     ```bash
     # After a period of power saving, restore connectivity for data upload
     /opt/creaturebox/src/power/powerup_wifi.sh && \
     /opt/creaturebox/src/software/Upload_Photo.py
     ```

4. **Scheduled Power Management**:
   - **Implementation**: Combined usage of scripts for automated power management.
   - **Example**:
     ```python
     # In scheduled task handler:
     def manage_power_schedule():
         current_hour = datetime.now().hour
         if 22 <= current_hour or current_hour < 5:
             # Nighttime - aggressive power saving
             os.system('/opt/creaturebox/src/power/low_in_one.sh')
         elif 5 <= current_hour < 7:
             # Early morning - moderate power with network
             os.system('/opt/creaturebox/src/power/powerup_wifi.sh')
             os.system('/opt/creaturebox/src/power/lowpower.sh')
         else:
             # Daytime - full power
             os.system('sudo systemctl start creaturebox_full_power.service')
     ```
