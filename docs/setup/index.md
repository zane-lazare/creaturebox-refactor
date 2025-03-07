---
layout: default
title: Setup & Deployment
nav_order: 4
has_children: true
permalink: /setup/
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

## Key Components

<div class="component-cards">
  <div class="component-card">
    <h3>Installation</h3>
    <p>Core installation scripts and configuration files.</p>
    <div class="links">
      <a href="./installation">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Deployment</h3>
    <p>Production deployment configuration files.</p>
    <div class="links">
      <a href="./deployment">Documentation</a>
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

## Deployment Architecture

The production deployment uses a standard web stack:

<div class="mermaid">
graph TD;
    Client[Web Browser] --> Nginx[Nginx Web Server];
    Nginx --> Static[Static Files];
    Nginx --> Gunicorn[Gunicorn WSGI Server];
    Gunicorn --> Flask[Flask Application];
    Flask --> Python[Python Backend];
    Python --> Camera[Camera Hardware];
    Python --> Storage[Storage System];
    
    classDef client fill:#bbf,stroke:#333,stroke-width:1px;
    classDef server fill:#fbb,stroke:#333,stroke-width:1px;
    classDef app fill:#bfb,stroke:#333,stroke-width:1px;
    
    class Client client;
    class Nginx,Gunicorn server;
    class Flask,Python app;
</div>

## Troubleshooting

Common installation issues and solutions:

1. **Permission Issues**: Ensure the installation script is run with sudo
2. **Camera Not Detected**: Enable camera interface with `sudo raspi-config`
3. **Web Interface Not Accessible**: Check nginx and creaturebox service status
4. **Low Storage Space**: Ensure at least 2GB free space for installation