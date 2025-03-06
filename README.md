# CreatureBox Web Interface

A modular web interface for controlling and monitoring CreatureBox wildlife monitoring systems.

## Features

- **System monitoring and control**: View system status, reboot, shutdown
- **Camera control**: Configure settings, take photos, calibrate
- **Photo gallery**: View, download, and delete photos
- **Scheduling**: Set up automatic photo schedules
- **Storage management**: Backups, cleanup, and monitoring
- **Background processing**: Async operations for long-running tasks
- **Caching**: Enhanced performance with local or Redis cache

## Installation

### Requirements

- Python 3.7+
- Raspberry Pi (tested on Pi 4 and Pi 5)

### Base Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/creaturebox-refactor.git
cd creaturebox-refactor

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m src.web.app
```

### Optional Dependencies

```bash
# Install optional dependencies (Redis cache, OpenCV for image processing)
pip install "redis>=4.4.0" "opencv-python-headless>=4.5.0"

# For Raspberry Pi with PiJuice power management
pip install pijuice>=1.6
```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt[dev]

# Run tests
pytest
```

## Architecture

The CreatureBox web interface uses a modular architecture:

- **Routes**: API endpoints in `src/web/routes/`
- **Utils**: Utility functions in `src/web/utils/`
- **Services**: Background services in `src/web/services/`
- **Tests**: Test suite in `src/web/tests/`

### Key Components

- **Job Queue**: Background processing for long-running tasks
- **Caching**: Performance optimization with Redis/in-memory caching
- **Storage Manager**: Photo backup and cleanup

## API Endpoints

### System

- `GET /api/system/status`: Get system status information
- `POST /api/system/reboot`: Reboot the system
- `POST /api/system/shutdown`: Shut down the system
- `POST /api/system/toggle-lights`: Toggle attraction lights

### Camera

- `GET /api/camera/settings`: Get camera settings
- `POST /api/camera/settings`: Update camera settings
- `POST /api/camera/calibrate`: Calibrate camera
- `POST /api/camera/capture`: Capture a photo
- `GET /api/camera/stream`: Stream camera feed

### Gallery

- `GET /api/gallery/dates`: Get list of dates with photos
- `GET /api/gallery/photos`: Get list of photos
- `GET /api/gallery/photos/view/<date>/<filename>`: View a photo
- `GET /api/gallery/photos/thumbnail/<date>/<filename>`: View a photo thumbnail
- `DELETE /api/gallery/photos/<filename>`: Delete a photo

### Jobs

- `GET /api/jobs/`: List background jobs
- `GET /api/jobs/<job_id>`: Get job status
- `POST /api/jobs/<job_id>/cancel`: Cancel a job
- `POST /api/jobs/cleanup`: Clean up old completed jobs

### Storage

- `GET /api/storage/stats`: Get storage statistics
- `POST /api/storage/backup`: Start a photo backup
- `POST /api/storage/backup/external`: Backup to external storage
- `POST /api/storage/clean`: Clean up old photos

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src

# Run specific test
pytest src/web/tests/test_job_queue.py
```

### Code Structure

```
src/
├── web/
│   ├── routes/        # API endpoints
│   ├── utils/         # Utility functions
│   ├── services/      # Background services
│   ├── tests/         # Tests
│   ├── app.py         # Application factory
│   ├── config.py      # Configuration
│   ├── error_handlers.py # Error handling
│   └── middleware.py  # Request middleware
```

## Deployment

### Development

```bash
python -m src.web.app
```

### Production

For production deployment, we recommend using Gunicorn with Nginx:

```bash
gunicorn -w 4 -b 127.0.0.1:5000 'src.web.app:create_app()'
```

## License

MIT
