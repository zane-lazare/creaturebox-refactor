# Software Components

The software components form the core functionality of the CreatureBox Refactored platform, handling data collection, storage, analysis, and business logic.

## Overview

The software components are organized into several key modules:

- **Data Collector**: Interfaces with sensors to gather environmental data
- **Database**: Manages data storage and retrieval
- **Analyzer**: Processes data to identify patterns and trigger actions
- **Notification System**: Sends alerts based on system events
- **Scheduler**: Manages timed operations across the system

## Data Collector

The data collector interfaces with various sensors to gather environmental data:

```python
class DataCollector:
    """
    Collects data from connected sensors.
    
    Supports various sensor types and communication protocols.
    """
    
    def __init__(self, config):
        """Initialize the data collector with configuration."""
        self.config = config
        self.sensors = self._initialize_sensors()
        
    def _initialize_sensors(self):
        """Initialize all configured sensors."""
        sensors = {}
        for sensor_config in self.config.get_sensors():
            sensor_type = sensor_config['type']
            sensor_class = self._get_sensor_class(sensor_type)
            sensors[sensor_config['id']] = sensor_class(sensor_config)
        return sensors
        
    def _get_sensor_class(self, sensor_type):
        """Get the appropriate sensor class for the given type."""
        sensor_classes = {
            'temperature': TemperatureSensor,
            'humidity': HumiditySensor,
            'light': LightSensor,
            # Add more sensor types as needed
        }
        return sensor_classes.get(sensor_type)
        
    def collect_data(self):
        """Collect data from all sensors."""
        data = {}
        for sensor_id, sensor in self.sensors.items():
            data[sensor_id] = sensor.read()
        return data
```

### Sensor Types

Each sensor type has its own class that handles the specific requirements for reading and interpreting data:

```python
class TemperatureSensor:
    """Temperature sensor implementation."""
    
    def __init__(self, config):
        """Initialize the temperature sensor with configuration."""
        self.id = config['id']
        self.name = config['name']
        self.pin = config.get('pin')
        self.address = config.get('address')
        self.protocol = config.get('protocol', 'i2c')
        
    def read(self):
        """Read the current temperature value."""
        # Implementation depends on hardware
        # ...
        return {
            'value': temperature,
            'unit': 'celsius',
            'timestamp': datetime.now().isoformat()
        }
```

## Database

The database component handles data storage and retrieval:

```python
class Database:
    """
    Manages data storage and retrieval.
    
    Supports both real-time and historical data access.
    """
    
    def __init__(self, config):
        """Initialize the database with configuration."""
        self.config = config
        self.connection = self._create_connection()
        
    def _create_connection(self):
        """Create a connection to the database."""
        # Connection logic depends on database type
        # ...
        return connection
        
    def store_sensor_data(self, data):
        """Store sensor data in the database."""
        # Implementation depends on database
        # ...
        
    def get_sensor_data(self, sensor_id, start_time=None, end_time=None):
        """Retrieve sensor data for a specific time range."""
        # Implementation depends on database
        # ...
        
    def get_latest_sensor_data(self, sensor_id=None):
        """Get the latest sensor data for one or all sensors."""
        # Implementation depends on database
        # ...
```

## Analyzer

The analyzer processes data to identify patterns and trigger actions:

```python
class Analyzer:
    """
    Analyzes sensor data to identify patterns and trigger actions.
    
    Supports rule-based analysis and can trigger notifications or power actions.
    """
    
    def __init__(self, config, database, notification_system, power_controller):
        """Initialize the analyzer with dependencies."""
        self.config = config
        self.database = database
        self.notification_system = notification_system
        self.power_controller = power_controller
        self.rules = self._load_rules()
        
    def _load_rules(self):
        """Load analysis rules from configuration."""
        return self.config.get_rules()
        
    def analyze_data(self, data):
        """Analyze the provided data against defined rules."""
        results = []
        for rule in self.rules:
            if self._check_rule(rule, data):
                results.append(self._execute_rule_action(rule))
        return results
        
    def _check_rule(self, rule, data):
        """Check if a rule's conditions are met."""
        # Implementation depends on rule structure
        # ...
        
    def _execute_rule_action(self, rule):
        """Execute the action defined by a rule."""
        action_type = rule['action']['type']
        
        if action_type == 'notification':
            return self.notification_system.send_notification(
                rule['action']['message']
            )
        elif action_type == 'power':
            return self.power_controller.set_outlet_status(
                rule['action']['outlet_id'],
                rule['action']['status']
            )
```

## Notification System

The notification system sends alerts based on system events:

```python
class NotificationSystem:
    """
    Sends notifications to users based on system events.
    
    Supports multiple notification channels (email, SMS, push).
    """
    
    def __init__(self, config):
        """Initialize the notification system with configuration."""
        self.config = config
        self.channels = self._initialize_channels()
        
    def _initialize_channels(self):
        """Initialize all configured notification channels."""
        channels = {}
        for channel_config in self.config.get_notification_channels():
            channel_type = channel_config['type']
            channel_class = self._get_channel_class(channel_type)
            channels[channel_config['id']] = channel_class(channel_config)
        return channels
        
    def _get_channel_class(self, channel_type):
        """Get the appropriate channel class for the given type."""
        channel_classes = {
            'email': EmailChannel,
            'sms': SMSChannel,
            'push': PushNotificationChannel,
            # Add more channel types as needed
        }
        return channel_classes.get(channel_type)
        
    def send_notification(self, message, channel_id=None):
        """Send a notification through specific or all channels."""
        results = {}
        
        if channel_id is not None:
            results[channel_id] = self.channels[channel_id].send(message)
        else:
            for id, channel in self.channels.items():
                results[id] = channel.send(message)
                
        return results
```

## Integration Points

The software components integrate with other parts of the system:

- **Web Interface**: Displays collected data and analysis results
- **Power Management**: Executes power-related actions based on analysis
- **Configuration**: Provides settings for all software components

## API Endpoints

The software components expose functionality through the API:

- `GET /api/sensors` - List all sensors
- `GET /api/sensors/{id}` - Get specific sensor data
- `GET /api/environment/current` - Get current environmental data
- `GET /api/environment/history` - Get historical environmental data
- `GET /api/notifications` - Get recent notifications
- `POST /api/rules` - Create a new analysis rule
