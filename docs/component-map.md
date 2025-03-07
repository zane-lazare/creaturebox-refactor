---
layout: default
title: Component Reference Map
nav_order: 9
permalink: /component-map
---

# Component Reference Map

This page provides a reference guide to navigate between related components in the CreatureBox system.

## System Overview

The CreatureBox system is organized into several interconnected modules:

<div class="mermaid">
graph TD;
    Root[Installation and Setup] --> Deployment[Production Deployment];
    Root --> Source[Source Code];
    
    Source --> Config[Configuration];
    Source --> Power[Power Management];
    Source --> Software[Software];
    Source --> Web[Web Interface];
    
    Web --> Routes[API Routes];
    Web --> Services[Background Services];
    Web --> Middleware[Middleware];
    Web --> Utils[Utilities];
    Web --> Tests[Tests];
    
    Software --> Scripts[Scripts];
</div>

## Component Dependencies

| Component | Depends On | Used By |
|-----------|------------|---------|
| [Configuration](./src-config.md) | - | [Software](./src-software.md), [Web](./src-web.md) |
| [Power Management](./src-power.md) | Hardware | [Software](./src-software.md), [Web Routes](./src-web-routes.md) |
| [Software](./src-software.md) | [Configuration](./src-config.md), [Power](./src-power.md) | [Web Routes](./src-web-routes.md), [Web Services](./src-web-services.md) |
| [Software Scripts](./src-software-scripts.md) | [Software](./src-software.md) | [Web Services](./src-web-services.md) |
| [Web Core](./src-web.md) | Flask | [Web Routes](./src-web-routes.md), [Web Services](./src-web-services.md) |
| [Web Routes](./src-web-routes.md) | [Web Core](./src-web.md), [Web Utils](./src-web-utils.md) | Web UI, API Clients |
| [Web Services](./src-web-services.md) | [Web Core](./src-web.md), [Software](./src-software.md) | [Web Routes](./src-web-routes.md) |
| [Web Middleware](./src-web-middleware.md) | [Web Core](./src-web.md) | [Web Routes](./src-web-routes.md) |
| [Web Utils](./src-web-utils.md) | [Software](./src-software.md) | [Web Routes](./src-web-routes.md), [Web Services](./src-web-services.md) |
| [Web Tests](./src-web-tests.md) | All Components | - |

## Common Workflows

### Photo Capture Workflow

1. **User Interface**: Initiates photo capture through the web interface
2. **Web Route**: `/api/camera/capture` endpoint in [Web Routes](./src-web-routes.md)
3. **Web Utility**: `capture_photo()` in [Web Utils](./src-web-utils.md)
4. **Software**: `Take_Photo.py` in [Software](./src-software.md)
5. **Configuration**: Camera settings in [Configuration](./src-config.md)

### Power Management Workflow

1. **Scheduler**: Initiates low power mode at scheduled times
2. **Web Route**: `/api/system/power` endpoint in [Web Routes](./src-web-routes.md)
3. **Web Service**: Job queue in [Web Services](./src-web-services.md)
4. **Software Script**: System check in [Software Scripts](./src-software-scripts.md)
5. **Power**: Low power scripts in [Power Management](./src-power.md)

### Data Storage Workflow

1. **Photo Capture**: Saves photo to local storage
2. **Web Route**: `/api/storage/backup` endpoint in [Web Routes](./src-web-routes.md)
3. **Web Service**: Storage service in [Web Services](./src-web-services.md)
4. **Software**: `Backup_Files.py` in [Software](./src-software.md)

## File Location Reference

| File Type | Location | Documentation |
|-----------|----------|---------------|
| Installation Scripts | Root directory | [Root Documentation](./root.md) |
| Deployment Configs | `/deployment` | [Deployment Documentation](./deployment.md) |
| Configuration Files | `/src/config` | [Configuration Documentation](./src-config.md) |
| Power Scripts | `/src/power` | [Power Documentation](./src-power.md) |
| Software Scripts | `/src/software` | [Software Documentation](./src-software.md) |
| Utility Scripts | `/src/software/scripts` | [Scripts Documentation](./src-software-scripts.md) |
| Web Application | `/src/web` | [Web Documentation](./src-web.md) |
| API Routes | `/src/web/routes` | [Routes Documentation](./src-web-routes.md) |
| Background Services | `/src/web/services` | [Services Documentation](./src-web-services.md) |
| Request Middleware | `/src/web/middleware` | [Middleware Documentation](./src-web-middleware.md) |
| Utility Functions | `/src/web/utils` | [Utils Documentation](./src-web-utils.md) |
| Test Suite | `/src/web/tests` | [Tests Documentation](./src-web-tests.md) |