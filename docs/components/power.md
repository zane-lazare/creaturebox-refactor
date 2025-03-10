# Power Management

The power management component is responsible for controlling and monitoring power outlets connected to the CreatureBox system.

## Overview

The power management system allows for:
- Manual control of outlets via the web interface
- Scheduled power operations based on time or environmental conditions
- Power usage monitoring and reporting
- Fail-safe operations in case of system failures

## Architecture

The power management component consists of several key modules:

### Power Controller

The power controller is the central component that manages all power-related operations:

```python
class PowerController:
    """
    Main controller for power management operations.
    
    Handles communication with physical power outlets and manages
    scheduled operations.
    """
    
    def __init__(self, config):
        """Initialize the power controller with configuration."""
        self.config = config
        self.outlets = self._initialize_outlets()
        self.scheduler = PowerScheduler(self)
        
    def _initialize_outlets(self):
        """Initialize all configured power outlets."""
        outlets = {}
        for outlet_config in self.config.get_outlets():
            outlets[outlet_config['id']] = PowerOutlet(outlet_config)
        return outlets
        
    def get_outlet_status(self, outlet_id=None):
        """Get the status of a specific outlet or all outlets."""
        if outlet_id is not None:
            return self.outlets[outlet_id].get_status()
        
        return {id: outlet.get_status() for id, outlet in self.outlets.items()}
        
    def set_outlet_status(self, outlet_id, status):
        """Set the status of a specific outlet."""
        if outlet_id not in self.outlets:
            raise ValueError(f"Outlet {outlet_id} not found")
            
        self.outlets[outlet_id].set_status(status)
        return self.outlets[outlet_id].get_status()
```

### Power Outlets

The `PowerOutlet` class represents a physical power outlet:

```python
class PowerOutlet:
    """
    Represents a physical power outlet connected to the system.
    
    Handles direct communication with the outlet hardware.
    """
    
    def __init__(self, config):
        """Initialize the power outlet with configuration."""
        self.id = config['id']
        self.name = config['name']
        self.type = config['type']
        self.status = "unknown"
        self.power_usage = 0
        
    def get_status(self):
        """Get the current status of the outlet."""
        self._update_status()
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "power_usage": self.power_usage
        }
        
    def set_status(self, status):
        """Set the status of the outlet (on/off)."""
        # Communicate with physical device
        # ...
        self.status = status
```

### Power Scheduler

The scheduler manages timed operations:

```python
class PowerScheduler:
    """
    Manages scheduled power operations.
    
    Schedules can be based on time or triggered by environmental conditions.
    """
    
    def __init__(self, controller):
        """Initialize the scheduler with a reference to the controller."""
        self.controller = controller
        self.schedules = []
        
    def add_schedule(self, schedule):
        """Add a new schedule."""
        self.schedules.append(schedule)
        
    def remove_schedule(self, schedule_id):
        """Remove a schedule by ID."""
        self.schedules = [s for s in self.schedules if s.id != schedule_id]
        
    def check_schedules(self):
        """Check all schedules and execute if conditions are met."""
        for schedule in self.schedules:
            if schedule.should_execute():
                self.execute_schedule(schedule)
                
    def execute_schedule(self, schedule):
        """Execute a schedule by setting outlet status."""
        self.controller.set_outlet_status(
            schedule.outlet_id, 
            schedule.target_status
        )
```

## Hardware Integration

The power management component supports several types of power control hardware:

- Smart power strips via WiFi
- Relay-based controllers via GPIO
- USB-controlled power hubs

Each hardware type has a specific driver implementation in the `src/power/drivers/` directory.

## Scheduling

### Time-Based Scheduling

Time-based schedules execute at specific times or intervals:

```python
# Turn on lights at 8:00 AM every day
schedule = TimeSchedule(
    outlet_id=1,
    target_status="on",
    time="08:00:00",
    days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
)
```

### Condition-Based Scheduling

Condition-based schedules execute when environmental conditions meet certain criteria:

```python
# Turn on heater when temperature drops below 24°C
schedule = ConditionSchedule(
    outlet_id=2,
    target_status="on",
    condition={
        "sensor": "temperature",
        "operator": "<",
        "value": 24
    }
)
```

## API Integration

The power management component exposes its functionality through the API:

- `GET /api/power/status` - Get all outlet statuses
- `GET /api/power/outlet/{id}` - Get specific outlet status
- `PUT /api/power/outlet/{id}` - Control outlet
- `GET /api/power/schedules` - Get all schedules
- `POST /api/power/schedules` - Create a new schedule
- `DELETE /api/power/schedules/{id}` - Delete a schedule
