---
layout: default
title: Deployment
nav_order: 6
permalink: /deployment/
---

# Deployment Module Documentation

{% include navigation.html %}

## Overview

The Deployment Module contains configuration files and service definitions that enable the CreatureBox system to run as a production service with web server configuration, process management, and system service integration.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `deployment` directory contains the configuration files and service definitions necessary to deploy the CreatureBox system in a production environment. This module:

- Defines system service configurations for automatic startup
- Configures the WSGI server for running the web application
- Sets up Nginx as a reverse proxy and static file server
- Creates proper process management for reliability
- Establishes logging and monitoring configurations
- Provides security hardening for production environments

These configuration files transform the development code into a robust, production-ready system that integrates with the Linux system service architecture.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Purpose |
|----------|------|------|---------|
| creaturebox.service | Config | 0.7 KB | Systemd service definition |
| gunicorn.conf.py | Python | 1.2 KB | WSGI server configuration |
| nginx.conf | Config | 1.6 KB | Web server configuration |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### creaturebox.service
- **Primary Purpose**: Systemd service definition for CreatureBox
- **Key Settings**:
  * `Description`: CreatureBox wildlife monitoring system
  * `ExecStart`: Command to start the service
  * `WorkingDirectory`: Application root directory
  * `User/Group`: Service process permissions
  * `Restart`: Automatic restart behavior
  * `Environment`: Environment variables
  * `WantedBy`: Service dependencies
- **Dependencies**:
  * Systemd service manager
- **Technical Notes**: Ensures automatic startup on boot and process monitoring

### gunicorn.conf.py
- **Primary Purpose**: WSGI server configuration
- **Key Settings**:
  * `bind`: Socket or address binding
  * `workers`: Number of worker processes
  * `worker_class`: Worker process type
  * `timeout`: Request timeout
  * `keepalive`: Connection keepalive
  * `accesslog`: Access log location
  * `errorlog`: Error log location
  * `loglevel`: Logging verbosity
  * `reload`: Auto-reload on code changes
  * `limit_request_line`: Request size limits
- **Dependencies**:
  * Gunicorn WSGI server
- **Technical Notes**: Optimized for reliability and performance on embedded hardware

### nginx.conf
- **Primary Purpose**: Web server and reverse proxy
- **Key Settings**:
  * `server_name`: Hostname configuration
  * `root`: Static files directory
  * `location` blocks: URL routing rules
  * `proxy_pass`: Reverse proxy configuration
  * `ssl_certificate`: TLS certificate paths
  * `client_max_body_size`: Upload size limits
  * `gzip` settings: Compression configuration
  * `expires` rules: Browser caching directives
  * Security headers and MIME types
- **Dependencies**:
  * Nginx web server
- **Technical Notes**: Configured for security, performance, and proper static file serving

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Web Interface](./web-interface.md): Serves the web application
  * System initialization scripts
- **Depends On**:
  * Linux systemd service manager
  * Nginx web server
  * Gunicorn WSGI server
  * Python environment
- **Used By**:
  * System boot process
  * Web clients accessing the application
  * System administration tools

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **System Service Installation**:
   - **Description**: Installing CreatureBox as a system service.
   - **Example**: 
     ```bash
     # Copy service definition
     sudo cp deployment/creaturebox.service /etc/systemd/system/
     
     # Reload systemd to recognize the new service
     sudo systemctl daemon-reload
     
     # Enable service to start on boot
     sudo systemctl enable creaturebox.service
     
     # Start the service
     sudo systemctl start creaturebox.service
     ```

2. **Web Server Configuration**:
   - **Description**: Setting up Nginx as a reverse proxy.
   - **Example**: 
     ```bash
     # Copy Nginx configuration
     sudo cp deployment/nginx.conf /etc/nginx/sites-available/creaturebox
     
     # Create symbolic link to enable the site
     sudo ln -s /etc/nginx/sites-available/creaturebox /etc/nginx/sites-enabled/
     
     # Test configuration
     sudo nginx -t
     
     # Reload Nginx to apply changes
     sudo systemctl reload nginx
     ```

3. **Application Performance Tuning**:
   - **Description**: Optimizing Gunicorn worker configuration.
   - **Example**: 
     ```python
     # In gunicorn.conf.py
     
     # Calculate optimal number of workers based on CPU cores
     import multiprocessing
     
     # Use 2-4 workers per core for CPU-bound applications
     workers = multiprocessing.cpu_count() * 2 + 1
     
     # Use gevent for high concurrency if operations are I/O bound
     worker_class = 'gevent'
     
     # Adjust timeout for longer-running operations
     timeout = 60
     
     # Configure logging for production
     accesslog = '/var/log/creaturebox/access.log'
     errorlog = '/var/log/creaturebox/error.log'
     loglevel = 'warning'
     ```

4. **System Service Management**:
   - **Description**: Managing the CreatureBox service lifecycle.
   - **Example**: 
     ```bash
     # Check service status
     sudo systemctl status creaturebox.service
     
     # View service logs
     sudo journalctl -u creaturebox.service
     
     # Restart the service after configuration changes
     sudo systemctl restart creaturebox.service
     
     # Stop the service for maintenance
     sudo systemctl stop creaturebox.service
     ```

</div>
</details>