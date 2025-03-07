---
layout: default
title: Component Reference Map
nav_order: 9
permalink: /component-map/
---

# Component Reference Map

{% include navigation.html %}

## Overview

This page provides a reference guide to navigate between related components in the CreatureBox system.

<details id="system-overview">
<summary><h2>System Overview</h2></summary>
<div markdown="1">

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

</div>
</details>

<details id="component-dependencies">
<summary><h2>Component Dependencies</h2></summary>
<div markdown="1">

| Component | Depends On | Used By |
|-----------|------------|---------|
| [Configuration](./core-components/configuration.md) | - | [Software](./core-components/software-module.md), [Web Interface](./web-interface.md) |
| [Power Management](./core-components/power-management.md) | Hardware | [Software](./core-components/software-module.md), [Web Routes](./web-interface/routes.md) |
| [Software](./core-components/software-module.md) | [Configuration](./core-components/configuration.md), [Power](./core-components/power-management.md) | [Web Routes](./web-interface/routes.md), [Web Services](./web-interface/services.md) |
| [Web Core](./web-interface/core.md) | Flask | [Web Routes](./web-interface/routes.md), [Web Services](./web-interface/services.md) |
| [Web Routes](./web-interface/routes.md) | [Web Core](./web-interface/core.md), [Web Utils](./web-interface/utils.md) | Web UI, API Clients |
| [Web Services](./web-interface/services.md) | [Web Core](./web-interface/core.md), [Software](./core-components/software-module.md) | [Web Routes](./web-interface/routes.md) |
| [Web Middleware](./web-interface/middleware.md) | [Web Core](./web-interface/core.md) | [Web Routes](./web-interface/routes.md) |
| [Web Utils](./web-interface/utils.md) | [Software](./core-components/software-module.md) | [Web Routes](./web-interface/routes.md), [Web Services](./web-interface/services.md) |
| [Web Tests](./web-interface/tests.md) | All Components | - |

</div>
</details>

<details id="common-workflows">
<summary><h2>Common Workflows</h2></summary>
<div markdown="1">

### Photo Capture Workflow

1. **User Interface**: Initiates photo capture through the web interface
2. **Web Route**: `/api/camera/capture` endpoint in [Web Routes](./web-interface/routes.md)
3. **Web Utility**: `capture_photo()` in [Web Utils](./web-interface/utils.md)
4. **Software**: `Take_Photo.py` in [Software Module](./core-components/software-module.md)
5. **Configuration**: Camera settings in [Configuration](./core-components/configuration.md)

### Power Management Workflow

1. **Scheduler**: Initiates low power mode at scheduled times
2. **Web Route**: `/api/system/power` endpoint in [Web Routes](./web-interface/routes.md)
3. **Web Service**: Job queue in [Web Services](./web-interface/services.md)
4. **Software Script**: System check in [Software Module](./core-components/software-module.md)
5. **Power**: Low power scripts in [Power Management](./core-components/power-management.md)

### Data Storage Workflow

1. **Photo Capture**: Saves photo to local storage
2. **Web Route**: `/api/storage/backup` endpoint in [Web Routes](./web-interface/routes.md)
3. **Web Service**: Storage service in [Web Services](./web-interface/services.md)
4. **Software**: `Backup_Files.py` in [Software Module](./core-components/software-module.md)

</div>
</details>

<details id="file-location-reference">
<summary><h2>File Location Reference</h2></summary>
<div markdown="1">

| File Type | Location | Documentation |
|-----------|----------|---------------|
| Installation Scripts | Root directory | [Root Documentation](./root.md) |
| Deployment Configs | `/deployment` | [Deployment Documentation](./deployment.md) |
| Configuration Files | `/src/config` | [Configuration Documentation](./core-components/configuration.md) |
| Power Scripts | `/src/power` | [Power Documentation](./core-components/power-management.md) |
| Software Scripts | `/src/software` | [Software Documentation](./core-components/software-module.md) |
| Web Application | `/src/web` | [Web Documentation](./web-interface.md) |
| API Routes | `/src/web/routes` | [Routes Documentation](./web-interface/routes.md) |
| Background Services | `/src/web/services` | [Services Documentation](./web-interface/services.md) |
| Request Middleware | `/src/web/middleware` | [Middleware Documentation](./web-interface/middleware.md) |
| Utility Functions | `/src/web/utils` | [Utils Documentation](./web-interface/utils.md) |
| Test Suite | `/src/web/tests` | [Tests Documentation](./web-interface/tests.md) |

</div>
</details>

## Navigation Guide

The documentation is organized into these main sections:

1. **[Core Components](./core-components/index.md)** - Central system modules:
   - [Configuration](./core-components/configuration.md)
   - [Power Management](./core-components/power-management.md)
   - [Software Module](./core-components/software-module.md)

2. **[Web Interface](./web-interface.md)** - Web application components:
   - [Core Web Components](./web-interface/core.md)
   - [API Routes](./web-interface/routes.md)
   - [Middleware](./web-interface/middleware.md)
   - [Services](./web-interface/services.md)
   - [Utilities](./web-interface/utils.md)
   - [Static Resources](./web-interface/static.md)
   - [Tests](./web-interface/tests.md)

3. **[Setup & Deployment](./setup.md)** - Installation and configuration:
   - [Root Scripts](./root.md)
   - [Deployment Configuration](./deployment.md)