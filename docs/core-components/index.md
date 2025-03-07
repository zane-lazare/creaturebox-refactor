# Core Components Documentation

{% include navigation.html %}

## Overview

The Core Components module contains the essential building blocks of the CreatureBox system that provide the foundational functionality for wildlife monitoring, including configuration, power management, and operational software.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The core components are the fundamental building blocks of the CreatureBox system, providing essential functionality for:

- System configuration and parameter management
- Power conservation and management for field deployments
- Core operational software for system control
- Critical utility scripts for maintenance and operation

These components work together to ensure reliable operation, efficient power use, and flexible configuration of the wildlife monitoring system. They serve as the foundation upon which the web interface and other higher-level components are built.

</div>
</details>

<details id="component-overview">
<summary><h2>Component Overview</h2></summary>
<div markdown="1">

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| [Configuration](./configuration.md) | System-wide settings management | Parameter definition, configuration storage |
| [Power Management](./power-management.md) | Energy efficiency for field deployments | Low power modes, WiFi control, battery optimization |
| [Software Module](./software-module.md) | Core operational functionality | Camera control, scheduling, system management |

</div>
</details>

<details id="architecture">
<summary><h2>Architecture</h2></summary>
<div markdown="1">

The core components are organized in a modular architecture that enables:

- Clear separation of concerns
- Independent development and testing
- Flexible configuration and deployment
- Scalable system design

### Component Relationships

The core components interact in the following ways:

1. **Configuration** provides parameters to all other components
2. **Power Management** controls system energy states
3. **Software Module** implements operational functionality
4. All components support the **Web Interface** for remote control

### Dependency Flow

```
Configuration ───┬─→ Software Module ───→ Utility Scripts
                 │
                 └─→ Power Management ──→ Low Power Mode
                                        └─→ WiFi Management
```

</div>
</details>

<details id="usage">
<summary><h2>Usage</h2></summary>
<div markdown="1">

### Configuration

The Configuration module defines system-wide settings and parameters that control the behavior of other components:

```python
# Access configuration parameters
from src.config import camera_settings

# Get specific configuration
resolution = camera_settings.get_value('resolution')
```

### Power Management

The Power Management module controls energy usage for field deployments:

```bash
# Enter low power mode
./src/power/lowpower.sh

# Temporarily enable WiFi for data upload
./src/power/powerup_wifi.sh --duration=10
```

### Software Module

The Software Module implements the core operational functionality:

```python
# Capture a photo
from src.software import TakePhoto
TakePhoto.capture_image(save_path="/data/images/")

# Enable attraction mode
from src.software import Attract_On
Attract_On.start_attraction_sequence()
```

</div>
</details>

<details id="integration">
<summary><h2>Integration</h2></summary>
<div markdown="1">

The core components integrate with the [Web Interface](../src-web.md) to provide a complete system:

- **Configuration** is accessed and modified through web settings panels
- **Software** scripts are triggered by web API calls
- **Power Management** is controlled through web power control interface

Key integration points:

1. **API Endpoints**: The web routes call software functions
2. **Settings Forms**: The web interface modifies configuration files
3. **System Control**: The web interface invokes power management scripts

</div>
</details>

## Component Links

<div class="component-grid">
  <div class="component-card">
    <h3>Configuration</h3>
    <p>Defines system-wide settings and parameters for various components.</p>
    <a href="./configuration.md" class="btn">View Documentation</a>
  </div>
  
  <div class="component-card">
    <h3>Power Management</h3>
    <p>Controls power-related operations for field deployments.</p>
    <a href="./power-management.md" class="btn">View Documentation</a>
  </div>
  
  <div class="component-card">
    <h3>Software Module</h3>
    <p>Implements core operational scripts for system functionality.</p>
    <a href="./software-module.md" class="btn">View Documentation</a>
  </div>
</div>

<style>
.component-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-gap: 20px;
  margin: 30px 0;
}

.component-card {
  background: #f8f9fa;
  border-radius: 5px;
  padding: 15px 20px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.component-card h3 {
  margin-top: 0;
  border-bottom: 1px solid #e1e4e8;
  padding-bottom: 10px;
  color: #0366d6;
}

.btn {
  display: inline-block;
  background-color: #0366d6;
  color: white;
  padding: 6px 12px;
  border-radius: 3px;
  text-decoration: none;
  margin-top: 10px;
}

.btn:hover {
  background-color: #0257ba;
}
</style>
