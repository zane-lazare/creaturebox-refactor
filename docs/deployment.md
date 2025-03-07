# Deployment Configuration

## Overview
Deployment directory contains critical configuration files for service management and web server setup.

## Configuration Files

### 1. creaturebox.service
- **Purpose**: Systemd service configuration
- **Key Features**:
  * Defines service startup behavior
  * Manages application process lifecycle

### 2. gunicorn.conf.py
- **Purpose**: Gunicorn WSGI HTTP server configuration
- **Configuration Highlights**:
  * Worker process management
  * Performance and scaling settings
  * Logging configuration

### 3. nginx.conf
- **Purpose**: Nginx web server configuration
- **Key Components**:
  * Reverse proxy settings
  * SSL/TLS configuration
  * Request routing
  * Performance optimizations

## Deployment Strategy
- Utilizes systemd for service management
- Uses Gunicorn as WSGI server
- Nginx acts as reverse proxy and load balancer
