---
layout: default
title: Documentation Index
nav_order: 2
permalink: /index/
---

# CreatureBox Documentation Index

{% include navigation.html %}

Welcome to the CreatureBox documentation index. This page provides a comprehensive listing of all documentation files organized by category.

## Documentation Improvements

The documentation has been systematically improved following the [Documentation Remediation Plan](./CreatureBox%20Documentation%20Remediation%20Plan.md):
- **Standardized format** with consistent structure across all files
- **Collapsible sections** for better navigation
- **Jekyll integration** with proper front matter
- **Consolidated content** to eliminate redundancy
- **Improved cross-references** between related documentation

## Documentation Structure

<details id="system-components">
<summary><h2>System Components</h2></summary>
<div markdown="1">

### Root Level
- [README](./README.md) - Main documentation entry point
- [Root Directory](./root.md) - Root directory documentation
  - [Root Files](./root-files.md) - Detailed file inventory
- [Deployment](./deployment.md) - Deployment configuration documentation
  - [Deployment Files](./deployment-files.md) - Detailed file inventory
- [Source Directory](./src.md) - Source directory overview
- [Setup Guide](./setup.md) - Installation and setup instructions

### Reference Documents
- [Component Map](./component-map.md) - Visual representation of system components
- [Repository Structure Manifest](./repository-manifest.md) - Complete file hierarchy
- [Repository Structure JSON](./repository-structure-manifest.json) - Machine-readable structure
- [Documentation Error Log](./documentation-error-log.md) - Documentation issue tracking
- [Documentation Progress](./documentation-progress.json) - Progress tracking dashboard
- [Comprehensive File Manifest](./comprehensive-file-manifest.md) - Complete file listing

</div>
</details>

<details id="core-components">
<summary><h2>Core Components</h2></summary>
<div markdown="1">

### Core Components Directory
- [Core Components Overview](./core-components/index.md) - Core functionality modules
- [Configuration Module](./core-components/configuration.md) - System-wide settings management
- [Power Management](./core-components/power-management.md) - Power control system
- [Software Module](./core-components/software-module.md) - Operational scripts and logic

### Legacy Component Documentation
*Note: These files have been consolidated into the core components directory*
- [Configuration (Legacy)](./config.md) - Legacy configuration documentation
- [Power Management (Legacy)](./power.md) - Legacy power management documentation
- [Software Module (Legacy)](./software.md) - Legacy software module documentation
- [Source Configuration (Legacy)](./src-config.md) - Legacy source configuration documentation
  - [Config Files](./src-config-files.md) - Configuration files inventory
- [Source Power Management (Legacy)](./src-power.md) - Legacy source power documentation
  - [Power Files](./src-power-files.md) - Power management files inventory
- [Source Software (Legacy)](./src-software.md) - Legacy source software documentation
  - [Software Files](./src-software-files.md) - Software files inventory
- [Software Scripts (Legacy)](./src-software-scripts.md) - Legacy scripts documentation

</div>
</details>

<details id="web-interface">
<summary><h2>Web Interface Components</h2></summary>
<div markdown="1">

### Web Interface Directory
- [Web Interface Overview](./web-interface.md) - Web application overview
- [Core Web Components](./web-interface/core.md) - Main application files
- [Routes](./web-interface/routes.md) - API endpoints
- [Services](./web-interface/services.md) - Background services
- [Middleware](./web-interface/middleware.md) - Request processing
- [Static Resources](./web-interface/static.md) - Frontend assets

### Web Module Documentation
- [Web Core](./src-web.md) - Web module core components
  - [Web Files](./src-web-files.md) - Web module file inventory
- [Web Middleware](./src-web-middleware.md) - Web middleware components
  - [Middleware Files](./src-web-middleware-files.md) - Middleware file inventory
- [Web Routes](./src-web-routes.md) - API routing components
- [Web Services](./src-web-services.md) - Background service components
- [Web Static Resources](./src-web-static.md) - Static asset components
  - [CSS Files](./src-web-static-css.md) - CSS stylesheets documentation
  - [JavaScript Files](./src-web-static-js.md) - JavaScript modules documentation
- [Web Tests](./src-web-tests.md) - Test suite documentation
- [Web Utilities](./src-web-utils.md) - Utility functions

</div>
</details>

<details id="documentation-structure">
<summary><h2>Documentation Resources</h2></summary>
<div markdown="1">

### Templates and Guidelines
- [Document Template](./templates/document-template.md) - Standard documentation template
- [Documentation Instructions](./documentation-instructions.md) - Documentation generation guide
- [Documentation Cleanup Plan](./documentation-cleanup-plan.md) - Original cleanup plan
- [Documentation Remediation Plan](./CreatureBox%20Documentation%20Remediation%20Plan.md) - Comprehensive remediation plan
- [Documentation Progress Update](./CreatureBox%20Documentation%20Remediation%20Plan%20-%20Progress%20Update.md) - Status updates

### Configuration Files
- [Jekyll Configuration](./\_config.yml) - Jekyll site configuration
- [Include Directory](./\_includes/) - Jekyll include files
- [Assets Directory](./assets/) - Documentation assets

</div>
</details>

## Documentation Map

<div class="documentation-map">
  <div class="section system">
    <h3>System Level</h3>
    <div class="files">
      <div class="file">README.md</div>
      <div class="file">index.md</div>
      <div class="file">root.md</div>
      <div class="file">deployment.md</div>
      <div class="file">setup.md</div>
    </div>
  </div>
  
  <div class="section core">
    <h3>Core Components</h3>
    <div class="files">
      <div class="file main">core-components/index.md</div>
      <div class="file">core-components/configuration.md</div>
      <div class="file">core-components/power-management.md</div>
      <div class="file">core-components/software-module.md</div>
    </div>
  </div>
  
  <div class="section web">
    <h3>Web Interface</h3>
    <div class="files">
      <div class="file main">web-interface.md</div>
      <div class="file">web-interface/core.md</div>
      <div class="file">web-interface/routes.md</div>
      <div class="file">web-interface/middleware.md</div>
      <div class="file">web-interface/services.md</div>
      <div class="file">web-interface/static.md</div>
    </div>
  </div>
  
  <div class="section ref">
    <h3>Reference</h3>
    <div class="files">
      <div class="file">component-map.md</div>
      <div class="file">repository-manifest.md</div>
      <div class="file">documentation-error-log.md</div>
      <div class="file">documentation-progress.json</div>
    </div>
  </div>
</div>

## How to Navigate this Documentation

1. **Start with [README](./README.md)** for a high-level overview
2. **Use collapsible sections** to focus on specific information
3. **Follow cross-references** to explore related components
4. **Check the [Core Components](./core-components/index.md)** for essential functionality
5. **Explore the [Web Interface](./web-interface.md)** for user interface components

The documentation has a consistent structure with these sections in each file:
- **Overview**: Brief introduction to the component
- **Purpose**: Detailed explanation of the component's role
- **File Inventory**: Listing of files with metadata
- **File Descriptions**: In-depth analysis of each file
- **Relationships**: Dependencies and connections
- **Use Cases**: Concrete examples of implementation

<style>
.documentation-map {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-gap: 20px;
  margin: 30px 0;
}

.section {
  background: #f8f9fa;
  border-radius: 5px;
  padding: 15px 20px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.section h3 {
  margin-top: 0;
  border-bottom: 1px solid #e1e4e8;
  padding-bottom: 10px;
}

.section.system h3 { color: #0366d6; }
.section.core h3 { color: #28a745; }
.section.web h3 { color: #6f42c1; }
.section.ref h3 { color: #d73a49; }

.files {
  display: flex;
  flex-direction: column;
}

.file {
  margin: 5px 0;
  padding: 5px 10px;
  background: white;
  border-radius: 3px;
  font-family: monospace;
  font-size: 0.9em;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.file.main {
  background: #fffbdd;
  font-weight: bold;
}
</style>
