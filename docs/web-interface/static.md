---
layout: default
title: Static Resources
parent: Web Interface
nav_order: 6
---

# Static Resources

{% include navigation.html %}

## Overview

The Web Static Resources module contains front-end assets including CSS stylesheets, JavaScript files, images, and fonts used by the CreatureBox web interface to create a responsive, user-friendly control panel.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `src/web/static` directory contains all static assets that are served by the web application to create the user interface. This module provides:

- CSS stylesheets for visual styling
- JavaScript files for client-side interactivity
- Image assets for UI elements and branding
- Font files for typography
- Favicon and icon assets
- Third-party dependencies for the web interface

These resources enable the creation of a responsive, modern web interface that provides an intuitive control panel for managing the CreatureBox system.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Purpose |
|----------|------|------|---------|
| (No files directly in static directory) | - | - | - |

**Subdirectories:**

| Subdirectory | Description |
|--------------|-------------|
| css/ | Stylesheet files |
| js/ | JavaScript files |
| images/ | UI images and icons |
| fonts/ | Typography assets |
| lib/ | Third-party libraries |

### CSS Files

| Filename | Size | Purpose |
|----------|------|---------|
| style.css | 24 KB | Main stylesheet |
| components.css | 15 KB | UI component styles |
| responsive.css | 8 KB | Mobile-responsive styles |
| dark-mode.css | 6 KB | Dark theme styles |

### JavaScript Files

| Filename | Size | Purpose |
|----------|------|---------|
| main.js | 18 KB | Core application logic |
| camera.js | 12 KB | Camera control interface |
| gallery.js | 14 KB | Photo gallery management |
| settings.js | 10 KB | Settings panel functionality |
| charts.js | 8 KB | Data visualization |
| utils.js | 6 KB | Utility functions |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### CSS Files

#### style.css
- **Primary Purpose**: Main stylesheet for the application
- **Key Components**:
  * Base typography and color definitions
  * Layout grid system
  * Main navigation styling
  * Form element styling
  * Utility classes
- **Technical Notes**: Uses CSS variables for theming and consistent styling

#### components.css
- **Primary Purpose**: Component-specific styling
- **Key Components**:
  * Button styles and variations
  * Card and panel designs
  * Modal dialogs
  * Alerts and notifications
  * Tabs and accordions
- **Technical Notes**: Modular design for reusable components

#### responsive.css
- **Primary Purpose**: Mobile-responsive design rules
- **Key Components**:
  * Media queries for different screen sizes
  * Mobile navigation styles
  * Responsive grid adjustments
  * Touch-friendly element sizing
- **Technical Notes**: Mobile-first approach with breakpoints for larger screens

#### dark-mode.css
- **Primary Purpose**: Dark theme styling
- **Key Components**:
  * Dark color palette
  * Reduced brightness for night usage
  * Contrast adjustments
  * Theme transition effects
- **Technical Notes**: Toggled via data-theme attribute on root element

### JavaScript Files

#### main.js
- **Primary Purpose**: Core application functionality
- **Key Functions**:
  * Application initialization
  * Route handling
  * Global event listeners
  * Authentication management
  * State management
- **Technical Notes**: Modular structure with namespacing

#### camera.js
- **Primary Purpose**: Camera control interface
- **Key Functions**:
  * Live preview management
  * Camera settings controls
  * Capture button functionality
  * Image review and editing
  * Attraction mode toggle
- **Technical Notes**: Uses fetch API for camera control endpoints

#### gallery.js
- **Primary Purpose**: Photo gallery management
- **Key Functions**:
  * Image loading and pagination
  * Thumbnail generation
  * Lightbox viewer
  * Image organization (favorites, filtering)
  * Image download and sharing
- **Technical Notes**: Lazy loading for performance optimization

#### settings.js
- **Primary Purpose**: Settings management interface
- **Key Functions**:
  * Load configuration settings
  * Settings form validation
  * Save configuration changes
  * Restore defaults
  * Import/export configuration
- **Technical Notes**: Form validation with appropriate feedback

#### charts.js
- **Primary Purpose**: Data visualization
- **Key Functions**:
  * Power usage charts
  * Activity timeline
  * Storage usage visualization
  * Temperature monitoring
  * Schedule visualization
- **Technical Notes**: Uses Chart.js for visualization

#### utils.js
- **Primary Purpose**: Utility functions
- **Key Functions**:
  * Date formatting
  * File size formatting
  * Input validation
  * API request helpers
  * Browser storage management
- **Technical Notes**: Shared helper functions used across modules

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Core Web Components](./core.md): Serves static files to web clients
  * [API Routes](./routes.md): UI components correspond to API endpoints
- **Depends On**:
  * Browser web standards (HTML5, CSS3, ES6+)
  * Third-party libraries (if any)
  * Static file serving configuration in web server
- **Used By**:
  * Web browser clients
  * Mobile browser access
  * Web application components

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Web Interface Styling**:
   - **Description**: Consistent visual styling across the web application.
   - **Example**: 
     ```html
     <!-- In HTML templates -->
     <link rel="stylesheet" href="/static/css/style.css">
     <link rel="stylesheet" href="/static/css/components.css">
     <link rel="stylesheet" href="/static/css/responsive.css">
     
     <!-- Dark mode toggle in UI -->
     <button onclick="toggleDarkMode()" class="theme-toggle">
       Switch Theme
     </button>
     
     <script>
     function toggleDarkMode() {
       document.documentElement.toggleAttribute('data-theme-dark');
     }
     </script>
     ```

2. **Camera Control Interface**:
   - **Description**: Interactive camera control through the web interface.
   - **Example**: 
     ```html
     <!-- Camera control panel -->
     <div class="camera-panel">
       <div id="preview-container"></div>
       <div class="camera-controls">
         <button id="capture-btn" class="btn-primary">Capture</button>
         <div class="settings-panel"><!-- Camera settings --></div>
       </div>
     </div>
     
     <script src="/static/js/camera.js"></script>
     <script>
     document.addEventListener('DOMContentLoaded', () => {
       // Initialize camera interface
       CreatureBox.Camera.init({
         previewElement: document.getElementById('preview-container'),
         captureButton: document.getElementById('capture-btn')
       });
     });
     </script>
     ```

3. **Photo Gallery Management**:
   - **Description**: Browsing and managing captured photos.
   - **Example**: 
     ```html
     <!-- Gallery component -->
     <div class="gallery-container" id="photo-gallery" 
          data-page="1" data-filter="all">
       <div class="gallery-toolbar">
         <select id="filter-select">
           <option value="all">All Photos</option>
           <option value="favorites">Favorites</option>
         </select>
       </div>
       <div class="gallery-grid"></div>
       <div class="pagination"></div>
     </div>
     
     <script src="/static/js/gallery.js"></script>
     <script>
     document.addEventListener('DOMContentLoaded', () => {
       // Initialize gallery
       CreatureBox.Gallery.init({
         container: document.getElementById('photo-gallery'),
         itemsPerPage: 20
       });
       
       // Handle filter changes
       document.getElementById('filter-select')
         .addEventListener('change', (e) => {
           CreatureBox.Gallery.filter(e.target.value);
         });
     });
     </script>
     ```

4. **Mobile-Responsive Design**:
   - **Description**: Adapting the interface for various device sizes.
   - **Example**: 
     ```css
     /* In responsive.css */
     /* Base styles for mobile devices */
     .camera-panel {
       display: flex;
       flex-direction: column;
     }
     
     /* Adjust for tablets */
     @media (min-width: 768px) {
       .camera-panel {
         flex-direction: row;
       }
       
       .preview-container {
         width: 60%;
       }
       
       .camera-controls {
         width: 40%;
       }
     }
     
     /* Adjust for desktop */
     @media (min-width: 1200px) {
       .camera-panel {
         gap: 2rem;
       }
       
       .settings-panel {
         display: grid;
         grid-template-columns: repeat(2, 1fr);
       }
     }
     ```

</div>
</details>

## Frontend Architecture

The frontend assets follow a modular architecture with separation of concerns:

- **Stylesheets**: Organized by function (base, components, responsive, themes)
- **JavaScript**: Modular files with specific responsibilities
- **Asset Organization**: Subdirectories for different asset types
- **Responsive Design**: Mobile-first approach with progressive enhancement
- **Theme Support**: Light and dark mode with CSS variables

This organization ensures maintainability, performance, and a consistent user experience across different devices and screen sizes.