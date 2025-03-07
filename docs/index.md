---
layout: default
title: Home
nav_order: 1
description: "CreatureBox Documentation"
permalink: /
---

# CreatureBox Documentation

CreatureBox is a modular web interface for controlling and monitoring wildlife monitoring systems. This documentation provides comprehensive information about the system architecture, components, and usage.

## System Architecture

The CreatureBox system consists of several interconnected components:

<div class="mermaid">
graph TD;
    Web[Web Interface] --> Routes[API Routes];
    Web --> Services[Background Services];
    Web --> WebUtils[Web Utilities];
    Services --> Software[Software Components];
    Routes --> WebUtils;
    Routes --> Software;
    Software --> Config[Configuration];
    Software --> Power[Power Management];
    Software --> Scripts[Software Scripts];
    
    classDef core fill:#f9f,stroke:#333,stroke-width:2px;
    classDef web fill:#bbf,stroke:#333,stroke-width:1px;
    classDef util fill:#bfb,stroke:#333,stroke-width:1px;
    
    class Config,Software core;
    class Web,Routes,Services,WebUtils web;
    class Scripts util;
</div>

## Quick Navigation

| Category | Section |
|----------|---------|
| **Core Components** | [Overview](/core-components/) · [Configuration](/core-components/configuration) · [Power](/core-components/power) · [Software](/core-components/software) |
| **Web Interface** | [Overview](/web-interface/) · [Core](/web-interface/core) · [Routes](/web-interface/routes) · [Services](/web-interface/services) |
| **Setup & Deployment** | [Overview](/setup/) · [Installation](/setup/installation) · [Deployment](/setup/deployment) |

## Key Features

- **System monitoring and control**: View system status, reboot, shutdown
- **Camera control**: Configure settings, take photos, calibrate
- **Photo gallery**: View, download, and delete photos
- **Scheduling**: Set up automatic photo schedules
- **Storage management**: Backups, cleanup, and monitoring
- **Background processing**: Async operations for long-running tasks
- **Caching**: Enhanced performance with local or Redis cache

## Documentation Organization

This documentation is organized into three main sections:

1. **[Core Components](/core-components/)**: The fundamental building blocks of the system
   - [Configuration](/core-components/configuration): System-wide settings and parameters
   - [Power Management](/core-components/power): Power-related operations and utilities
   - [Software](/core-components/software): Core operational scripts

2. **[Web Interface](/web-interface/)**: The browser-based control panel
   - [Core](/web-interface/core): Main web application components
   - [Routes](/web-interface/routes): API endpoints for system control
   - [Services](/web-interface/services): Background processing services

3. **[Setup & Deployment](/setup/)**: Getting the system running
   - [Installation](/setup/installation): Setting up the system
   - [Deployment](/setup/deployment): Production deployment configuration

## Installation Overview

To set up CreatureBox, follow these steps:

1. Install hardware prerequisites
2. Clone the repository
3. Run the installation script
4. Configure system settings
5. Deploy services

See the [Setup & Deployment](/setup/) section for detailed instructions.