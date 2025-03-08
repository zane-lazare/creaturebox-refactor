---
layout: default
title: CreatureBox Documentation
nav_order: 1
permalink: /
---

# CreatureBox Documentation

{% include navigation.html %}

## Documentation Overview
This repository contains comprehensive documentation for the CreatureBox software system, generated through a systematic, recursive, and methodical documentation process. The documentation has been streamlined to eliminate redundancy while improving navigation and readability.

## Repository Information
- **Repository Name**: creaturebox-refactor
- **Repository Owner**: zane-lazare
- **Primary Branch**: main
- **Documentation Branch**: documentation

## Documentation Structure
Each module's documentation follows this improved structure:

1. **Overview**: Brief summary of the module's purpose
2. **Purpose**: Detailed explanation of the module's role in the system (collapsible)
3. **File Inventory**: Complete listing of all files with properly formatted table (collapsible)
4. **File Descriptions**: In-depth analysis of each file (collapsible)
5. **Relationships**: Dependencies and connections to other components (collapsible)
6. **Use Cases**: Concrete usage examples derived from code implementation (collapsible)

All sections are collapsible for better navigation, and each page includes a horizontal navigation menu to quickly jump to specific sections.

## Navigation Features
- **Collapsible Sections**: Click on any section header to expand/collapse it
- **Horizontal Navigation**: Use the menu below the title to jump directly to sections
- **Consistent Structure**: All documentation pages follow the same format for easy navigation

## Core Documentation Files

### System Components
- [Root Directory](./root.md): Installation scripts, configuration files, project setup
  - [Root Files](./root-files.md): Detailed file inventory
- [Deployment](./deployment.md): Production deployment configurations
  - [Deployment Files](./deployment-files.md): Detailed file inventory
- [Source Directory](./src.md): Main source code container overview

### Core Components
- [Core Components Overview](./core-components/index.md): Core functionality modules
  - [Configuration Module](./core-components/configuration.md): System-wide settings
  - [Power Management](./core-components/power-management.md): Power control scripts
  - [Software Module](./core-components/software-module.md): Operational scripts

### Web Application
- [Web Interface](./web-interface.md): Flask application and web components
  - [Core Web Components](./web-interface/core.md): Main application files
  - [Web Files](./src-web-files.md): Web module file inventory
  - [Routes](./web-interface/routes.md): API endpoints
  - [Services](./web-interface/services.md): Background services
  - [Middleware](./web-interface/middleware.md): Request processing
  - [Middleware Files](./src-web-middleware-files.md): Middleware file inventory
  - [Utilities](./web-interface/utils.md): Helper functions
  - [Static Resources](./web-interface/static.md): Frontend assets
  - [CSS Files](./src-web-static-css.md): CSS stylesheets documentation
  - [JavaScript Files](./src-web-static-js.md): JavaScript modules documentation
  - [Tests](./web-interface/tests.md): Test suite

### Reference Documents
- [Repository Structure](./repository-manifest.md): Complete repository topology
- [Component Map](./component-map.md): Visualization of system components
- [Documentation Error Log](./documentation-error-log.md): Documentation issue tracking
- [Documentation Progress](./documentation-progress.json): Progress tracking dashboard

## Documentation Improvements
This documentation has been enhanced with:

1. **Eliminated Redundancy**: Removed duplicate files and consolidated information
2. **Improved Table Formatting**: Standardized all tables using proper Markdown syntax
3. **Interactive Navigation**: Added collapsible sections and horizontal navigation menu
4. **Streamlined Structure**: Organized documentation into logical, hierarchical sections
5. **Core Components Directory**: Grouped related modules under a dedicated directory
6. **Jekyll Integration**: Added proper front matter for Jekyll site generation
7. **Comprehensive File Inventories**: Detailed file-level documentation for all modules

## Using This Documentation
1. Start with the overview sections for high-level understanding
2. Use collapsible sections to focus on specific information
3. Navigate quickly with the horizontal menu on each page
4. Refer to reference documents for system-wide context
5. See the [Core Components](./core-components/index.md) for central system functionality
6. Explore detailed [Web Interface](./web-interface.md) documentation for the user-facing components

This documentation has been designed to be both comprehensive and accessible, providing valuable information for developers, administrators, and users while enabling easy navigation of complex technical material.

## Documentation Generation Process
The documentation was generated through a systematic process outlined in the [Documentation Generation Instruction Set](./documentation-instructions.md) and follows the remediation plan detailed in [Documentation Remediation Plan](./CreatureBox%20Documentation%20Remediation%20Plan.md).
