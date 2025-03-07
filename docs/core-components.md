---
layout: default
title: Core Components
nav_order: 2
has_children: true
permalink: /core-components
---

# Core Components

The CreatureBox system relies on several core components that provide the foundational functionality for the wildlife monitoring system. These components manage configuration, power, and operational software.

## Component Architecture

The core components work together to provide system functionality:

<div class="mermaid">
graph TD;
    Config[Configuration] --> Software[Software];
    Config --> Power[Power Management];
    Software --> Scripts[Utility Scripts];
    Power --> LowPower[Low Power Mode];
    Power --> WiFi[WiFi Management];
    
    classDef config fill:#fbb,stroke:#333,stroke-width:2px;
    classDef software fill:#bfb,stroke:#333,stroke-width:2px;
    classDef power fill:#bbf,stroke:#333,stroke-width:2px;
    
    class Config config;
    class Software software;
    class Power power;
</div>

## Key Components

<div class="component-cards">
  <div class="component-card">
    <h3>Configuration</h3>
    <p>Defines system-wide settings and parameters for various components.</p>
    <div class="links">
      <a href="./src-config.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Power Management</h3>
    <p>Controls power-related operations for field deployments.</p>
    <div class="links">
      <a href="./src-power.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Software</h3>
    <p>Implements core operational scripts for system functionality.</p>
    <div class="links">
      <a href="./src-software.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Software Scripts</h3>
    <p>Provides specialized utility scripts for additional functionality.</p>
    <div class="links">
      <a href="./src-software-scripts.html">Documentation</a>
    </div>
  </div>
</div>

## Configuration Files

The configuration system manages several key file types:

| File | Purpose | Format |
|------|---------|--------|
| camera_settings.csv | Camera configuration parameters | CSV |
| controls.txt | System control settings | Text |
| schedule_settings.csv | Automated schedule configuration | CSV |

See [Configuration Documentation](./src-config.html) for detailed information.

## Power Management

The power management system includes scripts for optimizing battery usage:

<div class="file-listing">
low_in_one.sh - Combined low power mode script<br>
lowpower.sh - Basic low power mode<br>
powerup_wifi.sh - Re-enable WiFi after power saving
</div>

These scripts are crucial for field deployments where power conservation is important.

## Software Components

The software component includes scripts for various system operations:

<div class="file-listing">
Attract_On.py - Attraction light control<br>
Take_Photo.py - Photo capture controller<br>
Backup_Files.py - File backup utility<br>
Shut_Down.py - System shutdown handler<br>
Upload_Photo.py - Photo upload handler<br>
WiFi_Setup.py - Wireless configuration
</div>

## Use Cases

<div class="use-case">
  <h4>Field Deployment Power Management</h4>
  <p>Conserve battery power during periods of inactivity while ensuring the system can wake up for scheduled operations.</p>
  <p><strong>Example:</strong> The system enters low power mode overnight and wakes up at dawn to capture morning wildlife activity.</p>
</div>

<div class="use-case">
  <h4>Scheduled Photography</h4>
  <p>Automate photo capture based on configured schedules.</p>
  <p><strong>Example:</strong> Configure the system to take photos every hour during daylight hours.</p>
</div>

<div class="use-case">
  <h4>Wildlife Attraction</h4>
  <p>Use light patterns to attract wildlife for better photography opportunities.</p>
  <p><strong>Example:</strong> Activate attraction lights for 30 minutes at dusk to draw in nocturnal wildlife.</p>
</div>

## Integration

The core components integrate with the web interface to provide a complete system:

- Configuration is accessed through the web interface
- Software scripts are triggered by web API calls
- Power management is controlled through the web interface

See the [Web Interface](./web-interface.html) documentation for details on these integrations.