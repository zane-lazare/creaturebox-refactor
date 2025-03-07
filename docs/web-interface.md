---
layout: default
title: Web Interface
nav_order: 3
has_children: true
permalink: /web-interface
---

# Web Interface

The Web Interface is the primary user interaction component of the CreatureBox system. It provides a browser-based control panel for managing the wildlife monitoring system, viewing photos, configuring settings, and monitoring system status.

## Component Architecture

The Web Interface follows a modular architecture pattern:

```mermaid
graph TD
    App[Web Application] --> Routes[API Routes]
    App --> Services[Background Services]
    App --> Utils[Utility Functions]
    App --> Middleware[Request Middleware]
    
    Routes --> Camera[Camera Routes]
    Routes --> Gallery[Gallery Routes]
    Routes --> System[System Routes]
    Routes --> Storage[Storage Routes]
    
    Services --> JobQueue[Job Queue]
    Services --> Cache[Caching]
    Services --> StorageMgr[Storage Manager]
    
    Utils --> CameraUtil[Camera Utilities]
    Utils --> FileUtil[File Utilities]
    Utils --> SystemUtil[System Utilities]
    
    Middleware --> Auth[Authentication]
    
    style App fill:#bbf,stroke:#333,stroke-width:2px
```

## Key Components

<div class="component-cards">
  <div class="component-card">
    <h3>API Routes</h3>
    <p>Defines the REST API endpoints for controlling the system and accessing resources.</p>
    <div class="links">
      <a href="./src-web-routes.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Background Services</h3>
    <p>Manages long-running tasks, caching, and storage operations.</p>
    <div class="links">
      <a href="./src-web-services.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Middleware</h3>
    <p>Handles authentication, request processing, and cross-cutting concerns.</p>
    <div class="links">
      <a href="./src-web-middleware.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Utilities</h3>
    <p>Provides reusable helper functions for camera, file, and system operations.</p>
    <div class="links">
      <a href="./src-web-utils.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Tests</h3>
    <p>Comprehensive test suite for web components.</p>
    <div class="links">
      <a href="./src-web-tests.html">Documentation</a>
    </div>
  </div>
</div>

## API Endpoints

The Web Interface exposes the following main API endpoints:

| Endpoint | Description | Documentation |
|----------|-------------|---------------|
| `/api/system/*` | System status and control | [System Routes](./src-web-routes.html#system) |
| `/api/camera/*` | Camera control and settings | [Camera Routes](./src-web-routes.html#camera) |
| `/api/gallery/*` | Photo gallery management | [Gallery Routes](./src-web-routes.html#gallery) |
| `/api/storage/*` | Storage management | [Storage Routes](./src-web-routes.html#storage) |
| `/api/jobs/*` | Background job management | [Job Routes](./src-web-routes.html#jobs) |

## Configuration

The Web Interface is configured through several mechanisms:

1. **Environment Variables**: Runtime configuration
2. **Config Files**: Settings in `src/config/` directory
3. **Web Settings**: User-configurable settings accessible through the interface

See [Configuration Documentation](./src-config.html) for more details.

## Core Files

The main web application is defined in these key files:

<div class="file-listing">
app.py - Application entry point and factory<br>
config.py - Configuration management<br>
error_handlers.py - Centralized error handling<br>
middleware.py - Request processing middleware
</div>

See [Web Core Documentation](./src-web.html) for detailed information about these files.

## Deployment

For production deployment, the Web Interface is deployed using:

- **Gunicorn**: WSGI server
- **Nginx**: Web server and reverse proxy
- **Systemd**: Service management

See [Deployment Documentation](./deployment.html) for configuration details.