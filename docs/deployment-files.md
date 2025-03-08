---
layout: default
title: Deployment Files
parent: Deployment
nav_order: 1
permalink: /deployment/files/
---

# Deployment Files Documentation

{% include navigation.html %}

## Overview

The deployment files directory contains the specific configuration files required to install and run the CreatureBox system as a production service with proper web server configuration, process management, and system service integration.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The deployment files serve as the bridge between the CreatureBox application code and the operating system's service infrastructure. These files:

- Enable the application to run as a system service with proper process management
- Configure web servers and reverse proxies for secure and efficient request handling
- Set up appropriate permissions, file paths, and environment variables
- Establish proper logging, monitoring, and error handling for production use

These files are essential for transforming the CreatureBox from development code into a production-ready, resilient system.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| creaturebox.service | Systemd Unit | 0.7 KB | System service definition |
| gunicorn.conf.py | Python | 1.2 KB | WSGI server configuration |
| nginx.conf | Config | 1.6 KB | Web server configuration |
| supervisor.conf | Config | 0.9 KB | Process supervisor config (alternative to systemd) |
| .env.template | Template | 0.5 KB | Environment variables template |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### creaturebox.service
- **Primary Purpose**: Defines the CreatureBox system service for systemd
- **Key Settings**:
  * `Description`: Service description for system tools
  * `ExecStart`: Command to launch the application
  * `WorkingDirectory`: Application root directory
  * `User/Group`: Security permissions
  * `Restart`: Automatic restart policy
  * `Environment`: Configuration variables
- **Dependencies**: Systemd service manager
- **Technical Notes**: Must be installed in /etc/systemd/system/ and enabled

### gunicorn.conf.py
- **Primary Purpose**: Configures the WSGI application server
- **Key Settings**:
  * `bind`: Network interface binding
  * `workers`: Process count for parallelism
  * `worker_class`: Async model selection
  * `timeout`: Request timeout threshold
  * `accesslog`/`errorlog`: Log file locations
  * `capture_output`: Error capturing configuration
- **Dependencies**: Gunicorn package
- **Technical Notes**: Optimized for Raspberry Pi hardware constraints

### nginx.conf
- **Primary Purpose**: Web server and reverse proxy configuration
- **Key Settings**:
  * `server_name`: Domain/hostname configuration
  * `location` blocks: URL routing rules
  * `proxy_pass`: Backend service connection
  * `client_max_body_size`: Upload size limits
  * Static file serving rules
  * Caching and compression directives
- **Dependencies**: Nginx web server
- **Technical Notes**: Provides TLS termination and static asset optimization

### supervisor.conf
- **Primary Purpose**: Alternative process management for systems without systemd
- **Key Settings**:
  * `command`: Application start command
  * `directory`: Working directory
  * `user`: Security context
  * `autostart`/`autorestart`: Process management flags
  * `stdout_logfile`/`stderr_logfile`: Log locations
- **Dependencies**: Supervisor package
- **Technical Notes**: Use when systemd is unavailable or not preferred

### .env.template
- **Primary Purpose**: Template for environment configuration
- **Key Settings**:
  * `DEBUG`: Development mode flag
  * `SECRET_KEY`: Security secret
  * `DATABASE_URL`: Database connection string
  * `CAMERA_TYPE`: Hardware configuration
  * `STORAGE_PATH`: File storage location
- **Dependencies**: None (template only)
- **Technical Notes**: Must be copied to .env and populated with actual values

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Deployment](../deployment.md): Parent deployment documentation
  * [Web Interface](../web-interface/core.md): Web application being served
  * [Configuration](../core-components/configuration.md): Environment settings
- **Depends On**:
  * Linux system services (systemd/supervisor)
  * Web server packages (Nginx)
  * WSGI server packages (Gunicorn)
- **Used By**:
  * System administrators during installation
  * System startup processes
  * Deployment automation scripts

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Standard System Service Installation**:
   - **Description**: Installing CreatureBox as a systemd service
   - **Example**:
     ```bash
     # Copy and install the service definition
     sudo cp deployment/creaturebox.service /etc/systemd/system/
     sudo systemctl daemon-reload
     sudo systemctl enable creaturebox
     sudo systemctl start creaturebox
     
     # Verify service status
     sudo systemctl status creaturebox
     ```

2. **Web Server Integration**:
   - **Description**: Configuring Nginx as a reverse proxy
   - **Example**:
     ```bash
     # Install Nginx if needed
     sudo apt install nginx
     
     # Copy configuration
     sudo cp deployment/nginx.conf /etc/nginx/sites-available/creaturebox
     sudo ln -s /etc/nginx/sites-available/creaturebox /etc/nginx/sites-enabled/
     
     # Test and apply configuration
     sudo nginx -t
     sudo systemctl reload nginx
     ```

3. **Environment Configuration**:
   - **Description**: Setting up production environment variables
   - **Example**:
     ```bash
     # Create environment file from template
     cp deployment/.env.template .env
     
     # Edit with appropriate values
     nano .env
     
     # Set production database URL
     echo "DATABASE_URL=sqlite:///data/creaturebox.db" >> .env
     
     # Set unique secret key
     echo "SECRET_KEY=$(openssl rand -base64 32)" >> .env
     ```

4. **Legacy System Deployment (No systemd)**:
   - **Description**: Using supervisor for process management on older systems
   - **Example**:
     ```bash
     # Install supervisor
     sudo apt install supervisor
     
     # Copy configuration
     sudo cp deployment/supervisor.conf /etc/supervisor/conf.d/creaturebox.conf
     
     # Apply configuration
     sudo supervisorctl reread
     sudo supervisorctl update
     
     # Check status
     sudo supervisorctl status creaturebox
     ```

</div>
</details>
