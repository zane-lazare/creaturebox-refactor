---
layout: default
title: Core Components
nav_order: 2
has_children: true
permalink: /core-components/
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
      <a href="./configuration">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Power Management</h3>
    <p>Controls power-related operations for field deployments.</p>
    <div class="links">
      <a href="./power">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Software</h3>
    <p>Implements core operational scripts for system functionality.</p>
    <div class="links">
      <a href="./software">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Software Scripts</h3>
    <p>Provides specialized utility scripts for additional functionality.</p>
    <div class="links">
      <a href="./software-scripts">Documentation</a>
    </div>
  </div>
</div>

## Integration

The core components integrate with the web interface to provide a complete system:

- Configuration is accessed through the web interface
- Software scripts are triggered by web API calls
- Power management is controlled through the web interface

See the [Web Interface](/docs/web-interface/) documentation for details on these integrations.