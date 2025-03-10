# Configuration

The configuration component manages system settings and user preferences for the CreatureBox Refactored platform.

## Overview

The configuration system provides:
- Centralized management of all system settings
- Default configuration values
- User-specific settings
- Configuration validation
- Configuration persistence

## Architecture

The configuration component is structured around a central `ConfigManager` class that handles all configuration operations:

```python
class ConfigManager:
    """
    Manages system configuration and settings.
    
    Handles loading, saving, and validating configuration values.
    """
    
    def __init__(self, config_path=None):
        """Initialize the configuration manager."""
        self.config_path = config_path or "config/config.ini"
        self.defaults = self._load_defaults()
        self.config = self._load_config()
        
    def _load_defaults(self):
        """Load default configuration values."""
        from src.config.defaults import DEFAULT_CONFIG
        return DEFAULT_CONFIG
        
    def _load_config(self):
        """Load configuration from file."""
        config = self.defaults.copy()
        
        if os.path.exists(self.config_path):
            parser = configparser.ConfigParser()
            parser.read(self.config_path)
            
            # Override defaults with values from config file
            for section in parser.sections():
                if section not in config:
                    config[section] = {}
                    
                for key, value in parser[section].items():
                    config[section][key] = self._parse_value(value)
                    
        return config
        
    def _parse_value(self, value):
        """Parse configuration value into appropriate type."""
        # Try to convert to int, float, boolean, etc.
        # ...
        return parsed_value
        
    def get(self, section, key, default=None):
        """Get a configuration value."""
        try:
            return self.config[section][key]
        except KeyError:
            return default
            
    def set(self, section, key, value):
        """Set a configuration value."""
        if section not in self.config:
            self.config[section] = {}
            
        self.config[section][key] = value
        
    def save(self):
        """Save configuration to file."""
        parser = configparser.ConfigParser()
        
        for section, items in self.config.items():
            parser[section] = {}
            
            for key, value in items.items():
                parser[section][key] = str(value)
                
        with open(self.config_path, 'w') as f:
            parser.write(f)
            
    def validate(self):
        """Validate the current configuration."""
        # Implementation depends on validation rules
        # ...
        return validation_result
```

## Default Configuration

Default configuration values are defined in `src/config/defaults.py`:

```python
DEFAULT_CONFIG = {
    "system": {
        "name": "CreatureBox",
        "debug": False,
        "log_level": "INFO"
    },
    "web": {
        "host": "0.0.0.0",
        "port": 5000,
        "secret_key": "change_this_in_production",
        "session_timeout": 3600
    },
    "database": {
        "type": "sqlite",
        "path": "data/creaturebox.db",
        "backup_interval": 86400
    },
    "power": {
        "default_state": "off",
        "safety_timeout": 3600
    },
    "notification": {
        "enabled": True,
        "default_channel": "email"
    }
}
```

## Configuration File Format

The configuration is stored in an INI file format:

```ini
[system]
name = CreatureBox
debug = False
log_level = INFO

[web]
host = 0.0.0.0
port = 5000
secret_key = my_secure_key
session_timeout = 3600

[database]
type = sqlite
path = data/creaturebox.db
backup_interval = 86400

[power]
default_state = off
safety_timeout = 3600

[notification]
enabled = True
default_channel = email
```

## Configuration Sections

### System Configuration

General system settings:
- `name`: System name displayed in the UI
- `debug`: Enable/disable debug mode
- `log_level`: Logging verbosity level

### Web Configuration

Web interface settings:
- `host`: Interface to bind the web server to
- `port`: Port to run the web server on
- `secret_key`: Secret key for session management
- `session_timeout`: Session timeout in seconds

### Database Configuration

Database settings:
- `type`: Database type (sqlite, mysql, postgresql)
- `path`: Path to the database file (for SQLite)
- `host`: Database host (for MySQL/PostgreSQL)
- `port`: Database port (for MySQL/PostgreSQL)
- `user`: Database username (for MySQL/PostgreSQL)
- `password`: Database password (for MySQL/PostgreSQL)
- `database`: Database name (for MySQL/PostgreSQL)

### Power Configuration

Power management settings:
- `default_state`: Default state for power outlets on startup
- `safety_timeout`: Maximum time a device can be on before safety check

### Notification Configuration

Notification system settings:
- `enabled`: Enable/disable notifications
- `default_channel`: Default notification channel
- Channel-specific settings

## Configuration Validation

The configuration manager validates configuration values to ensure they are within acceptable ranges:

```python
def validate(self):
    """Validate the current configuration."""
    errors = []
    
    # Validate web port
    port = self.get("web", "port")
    if not (1024 <= port <= 65535):
        errors.append("Web port must be between 1024 and 65535")
        
    # Validate log level
    log_level = self.get("system", "log_level")
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if log_level not in valid_levels:
        errors.append(f"Log level must be one of: {', '.join(valid_levels)}")
        
    # Additional validation rules
    # ...
    
    return errors
```

## Web Interface

The configuration can be edited through the web interface:
- Settings page for viewing and editing configuration
- User-specific settings storage
- Configuration backup and restore

## API Endpoints

The configuration component exposes its functionality through the API:

- `GET /api/config` - Get all configuration values
- `GET /api/config/{section}` - Get configuration values for a section
- `PUT /api/config/{section}/{key}` - Update a configuration value
- `POST /api/config/backup` - Create a configuration backup
- `POST /api/config/restore` - Restore from a configuration backup
