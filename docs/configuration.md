# System Configuration

## Configuration Overview

CreatureBox uses a centralized configuration system to customize your habitat management platform.

## Configuration File

The primary configuration file is located at `config/config.ini`.

### Basic Configuration Sections

#### System Settings
```ini
[system]
debug = false
log_level = INFO
timezone = UTC
```

#### Sensor Configuration
```ini
[sensors]
temperature_unit = celsius
humidity_threshold = 65
update_interval = 300  # seconds
```

#### Power Management
```ini
[power]
default_outlet_state = off
emergency_shutdown = true
```

## Environment Variables

You can also use environment variables to override configuration settings:

```bash
export CREATUREBOX_DEBUG=true
export CREATUREBOX_TIMEZONE=America/New_York
```

## Configuration Validation

The system performs automatic configuration validation on startup:
- Checks for required parameters
- Validates sensor thresholds
- Ensures compatibility between settings

## Customization Best Practices

- Always use a configuration management tool
- Keep sensitive information out of version control
- Use environment-specific configurations

## Troubleshooting

- **Misconfiguration**: Check system logs
- **Missing Parameters**: Review default values
- **Conflicts**: Resolve environment variable overrides

## Next Steps

- [Explore Web Interface Components](components/web-interface.md)
- [Learn About Power Management](components/power-management.md)
