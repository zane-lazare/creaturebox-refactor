---
layout: default
title: Web Interface
nav_order: 3
has_children: true
permalink: /web-interface/
---

# Web Interface

The Web Interface is the primary user interaction component of the CreatureBox system. It provides a browser-based control panel for managing the wildlife monitoring system, viewing photos, configuring settings, and monitoring system status.

## Component Architecture

The Web Interface follows a modular architecture pattern:

<div class="mermaid">
graph TD;
    App[Web Application] --> Routes[API Routes];
    App --> Services[Background Services];
    App --> Utils[Utility Functions];
    App --> Middleware[Request Middleware];
    
    Routes --> Camera[Camera Routes];
    Routes --> Gallery[Gallery Routes];
    Routes --> System[System Routes];
    Routes --> Storage[Storage Routes];
    
    Services --> JobQueue[Job Queue];
    Services --> Cache[Caching];
    Services --> StorageMgr[Storage Manager];
    
    Utils --> CameraUtil[Camera Utilities];
    Utils --> FileUtil[File Utilities];
    Utils --> SystemUtil[System Utilities];
    
    Middleware --> Auth[Authentication];
    
    classDef app fill:#bbf,stroke:#333,stroke-width:2px;
    class App app;
</div>

## Key Components

<div class="component-cards">
  <div class="component-card">
    <h3>Core Web Components</h3>
    <p>Foundation of the web application including app setup, configuration, and error handling.</p>
    <div class="links">
      <a href="./core.html">Documentation</a>
    </div>
  </div>

  <div class="component-card">
    <h3>API Routes</h3>
    <p>Defines the REST API endpoints for controlling the system and accessing resources.</p>
    <div class="links">
      <a href="./routes.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Background Services</h3>
    <p>Manages long-running tasks, caching, and storage operations.</p>
    <div class="links">
      <a href="./services.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Middleware</h3>
    <p>Handles authentication, request processing, and cross-cutting concerns.</p>
    <div class="links">
      <a href="./middleware.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Utilities</h3>
    <p>Provides reusable helper functions for camera, file, and system operations.</p>
    <div class="links">
      <a href="./utils.html">Documentation</a>
    </div>
  </div>
  
  <div class="component-card">
    <h3>Tests</h3>
    <p>Comprehensive test suite for web components.</p>
    <div class="links">
      <a href="./tests.html">Documentation</a>
    </div>
  </div>

  <div class="component-card">
    <h3>Static Resources</h3>
    <p>Frontend assets including CSS, JavaScript, and images.</p>
    <div class="links">
      <a href="./static.html">Documentation</a>
    </div>
  </div>
</div>

## API Endpoints

The Web Interface exposes the following main API endpoints:

| Endpoint | Description | Documentation |
|----------|-------------|---------------|
| `/api/system/*` | System status and control | [System Routes](./routes.html#system) |
| `/api/camera/*` | Camera control and settings | [Camera Routes](./routes.html#camera) |
| `/api/gallery/*` | Photo gallery management | [Gallery Routes](./routes.html#gallery) |
| `/api/storage/*` | Storage management | [Storage Routes](./routes.html#storage) |
| `/api/jobs/*` | Background job management | [Job Routes](./routes.html#jobs) |

## Core Files

The main web application is defined in these key files:

<div class="file-listing">
app.py - Application entry point and factory<br>
config.py - Configuration management<br>
error_handlers.py - Centralized error handling<br>
middleware.py - Request processing middleware
</div>

See [Web Core Documentation](./core.html) for detailed information about these files.