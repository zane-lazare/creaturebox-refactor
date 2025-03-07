---
layout: default
title: Setup & Deployment
nav_order: 4
has_children: true
permalink: /setup
---

# Setup & Deployment

This section covers the installation, configuration, and deployment of the CreatureBox system.

## Installation Overview

The CreatureBox system is designed to be installed on Raspberry Pi hardware running Raspberry Pi OS. The installation process includes:

1. Hardware setup
2. Software installation
3. System configuration
4. Service deployment

## Quick Start

```bash
# Check system compatibility
python pre_install_check.py

# Run installation script
sudo ./install.sh

# Verify installation
python verify_installation.py
```

## Installation Files

<div class="component-cards">
  <div class="component-card">
    <h3>Root Files</h3>
    <p>Core installation scripts and configuration files.</p>
    <div class="links">
      <a href="./root.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Deployment</h3>
    <p>Production deployment configuration files.</p>
    <div class="links">
      <a href="./deployment.html">Documentation</a>
    </div>
  </div>
</div>

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

## Installation Steps

### 1. Base System Setup

```bash
# Update the system
sudo apt update
sudo apt upgrade -y

# Install required system dependencies
sudo apt install -y python3-pip python3-dev nginx git

# Clone the repository
git clone https://github.com/zane-lazare/creaturebox-refactor.git
cd creaturebox-refactor
```

### 2. Run Installation Script

The installation script automates the setup process:

```bash
# Run installation with default settings
sudo ./install.sh

# For custom installation location
sudo ./install.sh --target=/opt/custom-location

# For non-interactive installation
sudo ./install.sh --non-interactive
```

### 3. Production Deployment

For production deployments, the system uses:

- **Gunicorn**: WSGI server for running the Flask application
- **Nginx**: Web server for handling HTTP requests and serving static files
- **Systemd**: Service management for automatic startup and monitoring

Configuration files are provided in the `deployment/` directory:

<div class="file-listing">
creaturebox.service - Systemd service configuration<br>
gunicorn.conf.py - WSGI server configuration<br>
nginx.conf - Web server configuration
</div>

The deployment process configures these services:

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

### 4. Verification

After installation, verify the system is working correctly:

```bash
# Run verification script
python verify_installation.py

# Check service status
sudo systemctl status creaturebox
sudo systemctl status nginx

# Test web interface
curl http://localhost/api/system/status
```

## Troubleshooting

Common installation issues and solutions:

1. **Permission Issues**: Ensure the installation script is run with sudo
2. **Camera Not Detected**: Enable camera interface with `sudo raspi-config`
3. **Web Interface Not Accessible**: Check nginx and creaturebox service status
4. **Low Storage Space**: Ensure at least 2GB free space for installation

For detailed installation information, refer to [Root Documentation](./root.html) and [Deployment Documentation](./deployment.html).