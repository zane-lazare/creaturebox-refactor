---
layout: default
title: API Routes
parent: Web Interface
nav_order: 2
---

# API Routes

The API routes define the REST endpoints for controlling the CreatureBox system and accessing its resources.

## Directory Purpose
The `src/web/routes` directory contains the API endpoint definitions for the CreatureBox web interface. Each file in this directory implements a specific set of related routes using Flask Blueprints to organize the application's URL structure. These routes handle HTTP requests, process user input, interact with the underlying system components, and return appropriate responses. Together, they form the complete API that enables control and monitoring of the CreatureBox system through the web interface.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| __init__.py | Python | 0.3 KB | Package initialization and blueprint registration |
| camera.py | Python | 1.8 KB | Camera control and configuration routes |
| gallery.py | Python | 2.1 KB | Photo gallery management routes |
| jobs.py | Python | 1.2 KB | Background job management routes |
| settings.py | Python | 1.0 KB | System settings configuration routes |
| storage.py | Python | 1.5 KB | Storage management routes |
| system.py | Python | 1.3 KB | System control and monitoring routes |

## API Endpoints Overview

### Camera API {#camera}

The camera API provides endpoints for controlling the camera hardware:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/camera/settings` | GET | Retrieve camera settings |
| `/api/camera/settings` | POST | Update camera settings |
| `/api/camera/calibrate` | POST | Calibrate camera |
| `/api/camera/capture` | POST | Capture a photo |
| `/api/camera/stream` | GET | Stream camera feed |

### Gallery API {#gallery}

The gallery API enables photo management:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/gallery/dates` | GET | List dates with photos |
| `/api/gallery/photos` | GET | List photos with optional filtering |
| `/api/gallery/photos/view/<date>/<filename>` | GET | Retrieve specific photo |
| `/api/gallery/photos/thumbnail/<date>/<filename>` | GET | Retrieve photo thumbnail |
| `/api/gallery/photos/<filename>` | DELETE | Delete a photo |

### System API {#system}

The system API provides control over the hardware system:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/system/status` | GET | Get system status information |
| `/api/system/reboot` | POST | Reboot the system |
| `/api/system/shutdown` | POST | Shut down the system |
| `/api/system/toggle-lights` | POST | Toggle attraction lights |

### Jobs API {#jobs}

The jobs API manages background processing:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/jobs/` | GET | List background jobs |
| `/api/jobs/<job_id>` | GET | Get job status |
| `/api/jobs/<job_id>/cancel` | POST | Cancel a job |
| `/api/jobs/cleanup` | POST | Clean up old jobs |

### Storage API {#storage}

The storage API handles file storage operations:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/storage/stats` | GET | Get storage statistics |
| `/api/storage/backup` | POST | Start a photo backup |
| `/api/storage/backup/external` | POST | Backup to external storage |
| `/api/storage/clean` | POST | Clean up old photos |

## Use Cases

### Remote Photo Capture
```python
# API call from client application
import requests

def capture_photo(server_url, settings=None):
    """Capture a photo via the API"""
    endpoint = f"{server_url}/api/camera/capture"
    response = requests.post(endpoint, json=settings or {})
    
    if response.status_code == 202:
        # Accepted, async job started
        job_id = response.json()['job_id']
        print(f"Photo capture started with job ID: {job_id}")
        return job_id
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage
job_id = capture_photo("http://creaturebox.local", {
    "resolution": "high",
    "save_path": "custom/location"
})
```

### System Monitoring
```python
# API call to check system status
import requests

def get_system_status(server_url):
    """Get system status via the API"""
    endpoint = f"{server_url}/api/system/status"
    response = requests.get(endpoint)
    
    if response.status_code == 200:
        status = response.json()
        print(f"CPU Temperature: {status['cpu_temp']}°C")
        print(f"Storage: {status['storage_used']} / {status['storage_total']} GB")
        print(f"Uptime: {status['uptime']}")
        return status
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
```

## Relationship Documentation
- **Related To**:
  * src/web/app.py (application that registers these routes)
  * src/web/middleware/ (processes requests before reaching routes)
- **Depends On**:
  * src/web/utils/ (utility functions called from routes)
  * src/web/services/ (background services used by routes)
  * src/software/ (system scripts called by routes)
  * src/config/ (configuration files accessed by routes)
- **Used By**:
  * Web frontend
  * External API clients
  * Testing suite