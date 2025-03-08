# CreatureBox Documentation

Welcome to the documentation for the CreatureBox Web Interface, a modular system for controlling and monitoring CreatureBox wildlife monitoring systems.

## Documentation Navigation

For a complete list of all documentation files, see the [Documentation Index](./index.md).

## System Overview

The CreatureBox web interface provides a comprehensive set of features for managing wildlife monitoring systems:

- **System monitoring and control**: View system status, reboot, shutdown
- **Camera control**: Configure settings, take photos, calibrate
- **Photo gallery**: View, download, and delete photos
- **Scheduling**: Set up automatic photo schedules
- **Storage management**: Backups, cleanup, and monitoring
- **Background processing**: Async operations for long-running tasks
- **Caching**: Enhanced performance with local or Redis cache

## Documentation Structure

### Core Components
- [System Overview](./core-components/system-overview.md): Overall architecture and system design
- [Web Interface](./core-components/web-interface.md): Main web application

### API Routes
- [Routes Overview](./routes/index.md): API endpoints overview
- [System Routes](./routes/system.md): System control API endpoints
- [Camera Routes](./routes/camera.md): Camera control API endpoints
- [Gallery Routes](./routes/gallery.md): Photo gallery API endpoints
- [Jobs Routes](./routes/jobs.md): Background jobs API endpoints
- [Storage Routes](./routes/storage.md): Storage management API endpoints

### Utilities
- [Utilities Overview](./utils/index.md): Utility functions overview
- [Configuration](./utils/config.md): Configuration management
- [Authentication](./utils/auth.md): Authentication utilities
- [Error Handling](./utils/errors.md): Error handling utilities
- [Logging](./utils/logging.md): Logging utilities

### Background Services
- [Services Overview](./services/index.md): Background services overview
- [Job Queue](./services/job-queue.md): Background job processing
- [Camera Service](./services/camera.md): Camera control service
- [Storage Service](./services/storage.md): Storage management service

## Getting Started

To get started with CreatureBox:

1. See the [Installation Guide](./development/installation.md) for setup instructions
2. Read the [Architecture Overview](./core-components/system-overview.md) to understand the system design
3. Check out the [API Documentation](./routes/index.md) for available endpoints

## Contributing

Contributions to both the codebase and documentation are welcome! See the [Contributing Guide](./development/contributing.md) for more information.
