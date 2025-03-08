---
layout: default
title: Setup & Deployment
nav_order: 4
has_children: true
permalink: /setup/
---

# Setup & Deployment Documentation

{% include navigation.html %}

## Overview

The Setup & Deployment module provides the installation, configuration, and deployment procedures for the CreatureBox system, enabling users to properly set up the hardware and software components for wildlife monitoring.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The Setup & Deployment documentation provides comprehensive guidance for:

- Installing the CreatureBox system on Raspberry Pi hardware
- Configuring system components for optimal performance
- Deploying the system as reliable production services
- Verifying successful installation and operation
- Troubleshooting common setup issues
- Supporting both standard and custom deployment scenarios

These procedures ensure consistent, reliable installation across different environments and hardware configurations.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| install.sh | Shell | 2.5 KB | Main installation script |
| pre_install_check.py | Python | 1.8 KB | System requirements verification |
| verify_installation.py | Python | 1.5 KB | Post-installation validation |
| creaturebox.service | Config | 0.7 KB | Systemd service definition |
| gunicorn.conf.py | Python | 1.2 KB | WSGI server configuration |
| nginx.conf | Config | 1.6 KB | Web server configuration |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### Installation Scripts

#### install.sh
- **Primary Purpose**: Automates system installation process
- **Key Functions**:
  * Installs required dependencies
  * Configures system components
  * Sets up services
  * Initializes databases
  * Configures permissions
- **Dependencies**: Bash shell, system utilities
- **Technical Notes**: Must be run with root privileges

#### pre_install_check.py
- **Primary Purpose**: Validates system compatibility
- **Key Functions**:
  * Checks hardware compatibility
  * Verifies available disk space
  * Validates Python version
  * Checks for required system utilities
  * Tests camera connectivity
- **Dependencies**: Python 3.7+
- **Technical Notes**: Returns non-zero exit code if requirements not met

#### verify_installation.py
- **Primary Purpose**: Confirms successful installation
- **Key Functions**:
  * Tests system services
  * Verifies database connections
  * Checks camera functionality
  * Tests web server configuration
  * Validates user permissions
- **Dependencies**: Installed CreatureBox components
- **Technical Notes**: Generates detailed report of system status

### Deployment Configuration

#### creaturebox.service
- **Primary Purpose**: Systemd service definition
- **Key Settings**:
  * Service description
  * Execution command
  * Working directory
  * User/group permissions
  * Restart behavior
  * Dependencies
- **Dependencies**: Systemd
- **Technical Notes**: Installed to /etc/systemd/system/

#### gunicorn.conf.py
- **Primary Purpose**: WSGI server configuration
- **Key Settings**:
  * Worker processes
  * Socket binding
  * Timeouts
  * Logging settings
  * Process management
- **Dependencies**: Gunicorn package
- **Technical Notes**: Optimized for Raspberry Pi performance

#### nginx.conf
- **Primary Purpose**: Web server configuration
- **Key Settings**:
  * Virtual host configuration
  * Proxy settings
  * Static file serving
  * Security headers
  * SSL configuration
- **Dependencies**: Nginx web server
- **Technical Notes**: Configured for security and performance

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Root Directory](./root.md): Core installation files
  * [Deployment](./deployment.md): Deployment configuration
  * [Web Interface](./web-interface.md): Web application being deployed
  * [Core Components](./core-components.md): Software being installed
- **Depends On**:
  * Raspberry Pi hardware
  * Linux operating system
  * System utilities
  * Network infrastructure
- **Used By**:
  * System administrators
  * Initial deployment process
  * System maintenance procedures
  * Recovery operations

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Standard Installation**:
   - **Description**: Basic installation on Raspberry Pi hardware
   - **Example**: 
     ```bash
     # Update the system
     sudo apt update
     sudo apt upgrade -y
     
     # Install required system dependencies
     sudo apt install -y python3-pip python3-dev nginx git
     
     # Clone the repository
     git clone https://github.com/zane-lazare/creaturebox-refactor.git
     cd creaturebox-refactor
     
     # Run installation with default settings
     sudo ./install.sh
     
     # Verify installation
     python verify_installation.py
     ```

2. **Custom Installation**:
   - **Description**: Installation with custom settings
   - **Example**: 
     ```bash
     # Run with custom installation location and configuration
     sudo ./install.sh --target=/opt/custom-location --config=configs/custom.conf
     
     # For non-interactive installation
     sudo ./install.sh --non-interactive --accept-defaults
     ```

3. **Production Deployment**:
   - **Description**: Setting up system services for production
   - **Example**: 
     ```bash
     # Copy service file
     sudo cp deployment/creaturebox.service /etc/systemd/system/
     
     # Configure nginx
     sudo cp deployment/nginx.conf /etc/nginx/sites-available/creaturebox
     sudo ln -s /etc/nginx/sites-available/creaturebox /etc/nginx/sites-enabled/
     sudo rm /etc/nginx/sites-enabled/default
     
     # Reload and start services
     sudo systemctl daemon-reload
     sudo systemctl enable creaturebox
     sudo systemctl start creaturebox
     sudo systemctl restart nginx
     ```

4. **System Validation**:
   - **Description**: Verifying successful installation
   - **Example**: 
     ```bash
     # Run verification script
     python verify_installation.py --verbose
     
     # Check service status
     sudo systemctl status creaturebox
     sudo systemctl status nginx
     
     # Test web interface
     curl http://localhost/api/system/status
     ```

</div>
</details>

## System Requirements

The CreatureBox system has the following requirements:

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Raspberry Pi | Pi 3 Model B | Pi 4 Model B (4GB) |
| Storage | 16GB SD Card | 32GB SD Card |
| Camera | Raspberry Pi Camera v2 | HQ Camera |
| Power | 5V 2.5A | 5V 3A + Battery Backup |
| OS | Raspberry Pi OS Lite | Raspberry Pi OS (32-bit) |
| Python | 3.7+ | 3.9+ |

## Troubleshooting

Common installation issues and solutions:

1. **Permission Issues**: Ensure the installation script is run with sudo
2. **Camera Not Detected**: Enable camera interface with `sudo raspi-config`
3. **Web Interface Not Accessible**: Check nginx and creaturebox service status
4. **Low Storage Space**: Ensure at least 2GB free space for installation

For detailed installation information, refer to [Root Documentation](./root.html) and [Deployment Documentation](./deployment.html).
