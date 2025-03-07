# src/web/routes Directory Documentation

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

## Detailed File Descriptions

### __init__.py
- **Primary Purpose**: Initializes the routes package and provides functions to register all blueprints
- **Key Functions**:
  * `register_blueprints(app)`: Registers all blueprint modules with the Flask app
- **Dependencies**: Flask, all other route modules
- **Technical Notes**: Simplifies blueprint registration in the main app.py file

### camera.py
- **Primary Purpose**: Provides routes for camera control and configuration
- **Key Functions**:
  * `GET /api/camera/settings`: Retrieves current camera settings
  * `POST /api/camera/settings`: Updates camera settings
  * `POST /api/camera/calibrate`: Calibrates the camera
  * `POST /api/camera/capture`: Captures a photo
  * `GET /api/camera/stream`: Streams camera feed
- **Dependencies**:
  * Flask
  * src/web/utils/camera.py
  * src/web/services/job_queue.py
- **Technical Notes**: Some operations (like capture) are run asynchronously through the job queue

### gallery.py
- **Primary Purpose**: Manages photo gallery viewing and operations
- **Key Functions**:
  * `GET /api/gallery/dates`: Lists dates with photos
  * `GET /api/gallery/photos`: Lists photos with optional filtering
  * `GET /api/gallery/photos/view/<date>/<filename>`: Retrieves specific photo
  * `GET /api/gallery/photos/thumbnail/<date>/<filename>`: Retrieves photo thumbnail
  * `DELETE /api/gallery/photos/<filename>`: Deletes a photo
- **Dependencies**:
  * Flask
  * src/web/utils/files.py
  * src/web/services/storage.py
- **Technical Notes**: Implements pagination for efficiently loading large galleries

### jobs.py
- **Primary Purpose**: Manages background processing jobs
- **Key Functions**:
  * `GET /api/jobs/`: Lists all background jobs
  * `GET /api/jobs/<job_id>`: Gets status of specific job
  * `POST /api/jobs/<job_id>/cancel`: Cancels a running job
  * `POST /api/jobs/cleanup`: Cleans up completed jobs
- **Dependencies**:
  * Flask
  * src/web/services/job_queue.py
- **Technical Notes**: Provides real-time status updates for long-running operations

### settings.py
- **Primary Purpose**: Manages system configuration settings
- **Key Functions**:
  * `GET /api/settings/`: Retrieves all system settings
  * `GET /api/settings/<section>`: Retrieves settings for specific section
  * `POST /api/settings/<section>`: Updates settings for specific section
  * `POST /api/settings/reset`: Resets settings to defaults
- **Dependencies**:
  * Flask
  * src/config/*.csv files
- **Technical Notes**: Implements validation for each setting type

### storage.py
- **Primary Purpose**: Manages photo storage and backup operations
- **Key Functions**:
  * `GET /api/storage/stats`: Gets storage usage statistics
  * `POST /api/storage/backup`: Initiates photo backup
  * `POST /api/storage/backup/external`: Backs up to external device
  * `POST /api/storage/clean`: Cleans up old photos
- **Dependencies**:
  * Flask
  * src/web/services/storage.py
  * src/web/services/job_queue.py
- **Technical Notes**: Long-running storage operations are executed as background jobs

### system.py
- **Primary Purpose**: Provides system control and monitoring functionality
- **Key Functions**:
  * `GET /api/system/status`: Gets system status information
  * `POST /api/system/reboot`: Reboots the system
  * `POST /api/system/shutdown`: Shuts down the system
  * `POST /api/system/toggle-lights`: Toggles attraction lights
- **Dependencies**:
  * Flask
  * src/web/utils/system.py
  * src/software/Attract_On.py
  * src/software/Shut_Down.py
- **Technical Notes**: Implements confirmation requirements for critical operations

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

## Use Cases
1. **Camera Photo Capture**:
   - **Implementation**: The camera.py route file implements a POST endpoint that triggers the camera to take a photo.
   - **Example**:
     ```
     POST /api/camera/capture
     Content-Type: application/json
     
     {
       "resolution": "high",
       "save_path": "custom/location",
       "file_prefix": "wildlife_"
     }
     ```
     This request schedules a photo capture job and returns a job ID for tracking.

2. **Gallery Photo Browsing**:
   - **Implementation**: The gallery.py route file provides endpoints to browse and view photos.
   - **Example**:
     ```
     GET /api/gallery/photos?date=2025-03-01&page=2&limit=20
     ```
     Returns paginated list of photos from specified date.

3. **System Control**:
   - **Implementation**: The system.py route file enables system control operations.
   - **Example**:
     ```
     POST /api/system/toggle-lights
     Content-Type: application/json
     
     {
       "state": "on",
       "duration_minutes": 30
     }
     ```
     Turns on attraction lights for specified duration.

4. **Background Job Management**:
   - **Implementation**: The jobs.py route file manages long-running tasks.
   - **Example**:
     ```
     GET /api/jobs/a1b2c3d4-5678
     ```
     Returns the status of a specific job, such as a photo backup operation.
