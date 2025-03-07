# src Directory Documentation

## Directory Purpose
The `src` directory is the primary source code container for the CreatureBox system, housing all application components, modules, and subsystems. This directory organizes the codebase into logical modules according to functionality, creating a clear separation of concerns and enabling modular development. The src directory implements a structured architecture that divides the system into configuration management, power control, software utilities, and web interface components, allowing for independent development, testing, and maintenance of each subsystem while ensuring they work together cohesively.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| (No files directly in src directory) | - | - | - |

## Detailed File Descriptions
The src directory contains no files directly; it serves as a container for subdirectories.

## Subdirectories
| Subdirectory | Description |
|--------------|-------------|
| config/ | System configuration files and parameters |
| power/ | Power management scripts and utilities |
| software/ | Core operational scripts and utilities |
| web/ | Web interface and API components |

### config/
- **Purpose**: Contains configuration files for various system components
- **Key Files**:
  * camera_settings.csv: Camera configuration parameters
  * controls.txt: System control settings
  * schedule_settings.csv: Automated schedule configuration
- See [src/config Documentation](./src-config.md) for detailed information

### power/
- **Purpose**: Manages power-related operations for field deployments
- **Key Files**:
  * low_in_one.sh: Combined low power mode script
  * lowpower.sh: Basic low power mode
  * powerup_wifi.sh: Re-enable WiFi after power saving
- See [src/power Documentation](./src-power.md) for detailed information

### software/
- **Purpose**: Contains core operational scripts for system functionality
- **Key Files**:
  * Various .py files for system operations (Attract_On.py, Take_Photo.py, etc.)
  * scripts/ subdirectory with additional utility scripts
- See [src/software Documentation](./src-software.md) for detailed information

### web/
- **Purpose**: Implements the web interface and API for system control
- **Key Files**:
  * app.py: Flask application entry point
  * Various subdirectories for routes, services, utilities, etc.
- See [src/web Documentation](./src-web.md) for detailed information

## Relationship Documentation
- **Related To**:
  * deployment/ (deployment configurations use source code)
  * Root directory installation scripts
- **Depends On**:
  * External Python libraries (specified in requirements.txt)
  * System services and hardware
- **Used By**:
  * End users through web interface
  * System administrators
  * Deployment scripts

## Use Cases
1. **Modular System Development**:
   - **Implementation**: The src directory structure enables modular development of different system components.
   - **Example**:
     ```
     # Development of a new feature can be isolated to appropriate module
     # For example, adding a new camera feature:
     
     # 1. Update configuration
     # Edit src/config/camera_settings.csv to add new setting
     
     # 2. Implement camera functionality
     # Edit src/software/Take_Photo.py to support new feature
     
     # 3. Add web API support
     # Edit src/web/routes/camera.py to expose feature through API
     
     # 4. Add tests
     # Create test in src/web/tests/test_routes.py for new API endpoint
     ```
     This modular approach allows for clear organization and separation of concerns.

2. **System Deployment**:
   - **Implementation**: The src directory structure supports clean deployment processes.
   - **Example**:
     ```bash
     # Deployment script can target specific components
     deploy_creaturebox() {
       # Copy source code
       cp -r src/ /opt/creaturebox/
       
       # Configure services
       cp deployment/creaturebox.service /etc/systemd/system/
       
       # Install dependencies
       pip install -r requirements.txt
       
       # Start services
       systemctl daemon-reload
       systemctl enable creaturebox.service
       systemctl start creaturebox.service
     }
     ```

3. **Component Integration**:
   - **Implementation**: The src directory organizes code to enable clean integration between components.
   - **Example**:
     ```python
     # Web interface calling software utilities:
     from src.software.Take_Photo import capture_photo
     from src.config.camera_settings import get_camera_settings
     
     def api_capture_photo():
         # Get configuration
         settings = get_camera_settings()
         
         # Execute photo capture
         result = capture_photo(settings)
         
         return result
     ```
     This organization allows different components to work together while maintaining separation.

4. **System Maintenance and Updates**:
   - **Implementation**: The src structure allows targeted updates to specific components.
   - **Example**:
     ```bash
     # Update just the web interface without affecting other components
     update_web_interface() {
       # Stop service
       systemctl stop creaturebox.service
       
       # Backup current version
       cp -r /opt/creaturebox/src/web /opt/creaturebox/src/web.bak
       
       # Install new version
       cp -r src/web/ /opt/creaturebox/src/
       
       # Restart service
       systemctl start creaturebox.service
       
       # Verify update
       curl http://localhost:5000/api/system/status
     }
     ```
