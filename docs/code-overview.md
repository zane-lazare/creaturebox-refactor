# Code Overview

This page provides a high-level overview of the CreatureBox Refactored codebase structure and architecture.

## Architecture

CreatureBox Refactored follows a modular architecture with clear separation of concerns:

```
/src
│── /web             # Web interface components
│── /power           # Power management components
│── /software        # Software components
│── /config          # Configuration components
```

## Key Components

### Web Interface

The web interface provides a user-friendly dashboard for monitoring and controlling the system. It is built using Flask for the backend and a combination of HTML, CSS, and JavaScript for the frontend.

Key files:
- `src/web/app.py`: Flask application factory
- `src/web/routes.py`: API and web routes
- `src/web/templates/`: HTML templates

See [Web Interface](components/web.md) for more details.

### Power Management

The power management module controls and monitors the power outlets connected to the system. It allows for scheduled operations and power usage tracking.

Key files:
- `src/power/controller.py`: Main power control logic
- `src/power/outlets.py`: Outlet management
- `src/power/scheduler.py`: Scheduled power operations

See [Power Management](components/power.md) for more details.

### Software Components

The software components handle the core functionality of the system, including data collection, storage, and analysis.

Key files:
- `src/software/data_collector.py`: Sensor data collection
- `src/software/database.py`: Data storage and retrieval
- `src/software/analyzer.py`: Data analysis and alerts

See [Software Components](components/software.md) for more details.

### Configuration

The configuration module handles system settings and user preferences.

Key files:
- `src/config/manager.py`: Configuration management
- `src/config/defaults.py`: Default configuration values

See [Configuration](components/config.md) for more details.

## Data Flow

1. Sensors collect environmental data
2. Data is processed and stored in the database
3. The analyzer checks for conditions that require action
4. The power controller manages power outlets based on analyzed data
5. The web interface displays current status and allows user control

## Extension Points

The system is designed to be extensible in the following areas:

- Adding new sensor types
- Implementing additional power control methods
- Creating custom analysis rules
- Extending the web interface with new features
