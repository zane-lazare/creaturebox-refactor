---
layout: default
title: Web Static JavaScript
parent: Web Interface
nav_order: 7
permalink: /src/web/static/js/
---

# Web Static JavaScript Documentation

{% include navigation.html %}

## Overview

The Web Static JavaScript documentation provides a detailed inventory and analysis of the JavaScript files that enable client-side functionality for the CreatureBox web interface, including interactive controls, data visualization, and dynamic content.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

This document catalogs the JavaScript files within the `src/web/static/js` directory that provide client-side functionality for the CreatureBox web interface. These scripts enable:

- Interactive camera controls
- Photo gallery management
- Settings configuration interface
- Data visualization
- Form validation and processing
- Dynamic content loading
- User interface enhancements
- Real-time monitoring

The JavaScript architecture follows a modular approach with namespaced components to maintain code organization and facilitate maintenance.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Size | Description |
|----------|------|-------------|
| main.js | 18 KB | Core application initialization |
| camera.js | 12 KB | Camera control interface |
| gallery.js | 14 KB | Photo gallery management |
| settings.js | 10 KB | Settings panel functionality |
| charts.js | 8 KB | Data visualization |
| utils.js | 6 KB | Utility functions |
| api.js | 5 KB | API client for backend communication |
| forms.js | 7 KB | Form validation and processing |
| ui.js | 9 KB | UI components and effects |
| storage.js | 4 KB | Local storage management |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### main.js
- **Primary Purpose**: Core application initialization
- **Key Functions**:
  * `CreatureBox.init()`: Application initialization
  * `CreatureBox.Router.init()`: Client-side routing
  * `CreatureBox.Auth.checkSession()`: Session validation
  * `CreatureBox.Nav.init()`: Navigation setup
  * `CreatureBox.EventBus.subscribe()`: Event subscription system
  * `CreatureBox.Theme.init()`: Theme management
- **Dependencies**: utils.js, api.js
- **Technical Notes**: Sets up namespaced application structure and initializes components

### camera.js
- **Primary Purpose**: Camera control interface
- **Key Functions**:
  * `CreatureBox.Camera.init()`: Initialize camera interface
  * `CreatureBox.Camera.startPreview()`: Start camera preview
  * `CreatureBox.Camera.stopPreview()`: Stop camera preview
  * `CreatureBox.Camera.capture()`: Capture photo
  * `CreatureBox.Camera.updateSettings()`: Update camera settings
  * `CreatureBox.Camera.toggleAttraction()`: Toggle attraction mode
  * `CreatureBox.Camera.getStatus()`: Get camera status
- **Dependencies**: api.js, utils.js
- **Technical Notes**: Uses fetch API for camera control endpoints and WebSockets for live preview when available

### gallery.js
- **Primary Purpose**: Photo gallery management
- **Key Functions**:
  * `CreatureBox.Gallery.init()`: Initialize gallery component
  * `CreatureBox.Gallery.loadImages()`: Load images with pagination
  * `CreatureBox.Gallery.renderThumbnails()`: Render image thumbnails
  * `CreatureBox.Gallery.showLightbox()`: Display full-size image viewer
  * `CreatureBox.Gallery.filter()`: Filter images by criteria
  * `CreatureBox.Gallery.deleteImage()`: Delete selected image
  * `CreatureBox.Gallery.downloadImage()`: Download image to device
  * `CreatureBox.Gallery.bulkActions()`: Perform actions on multiple images
- **Dependencies**: api.js, ui.js, storage.js
- **Technical Notes**: Implements lazy loading for performance and optimized image loading

### settings.js
- **Primary Purpose**: Settings panel functionality
- **Key Functions**:
  * `CreatureBox.Settings.init()`: Initialize settings interface
  * `CreatureBox.Settings.loadConfig()`: Load configuration from server
  * `CreatureBox.Settings.saveConfig()`: Save configuration to server
  * `CreatureBox.Settings.validateForm()`: Validate settings form inputs
  * `CreatureBox.Settings.restoreDefaults()`: Restore default settings
  * `CreatureBox.Settings.exportConfig()`: Export configuration to file
  * `CreatureBox.Settings.importConfig()`: Import configuration from file
  * `CreatureBox.Settings.applyChanges()`: Apply settings without saving
- **Dependencies**: api.js, forms.js, utils.js
- **Technical Notes**: Implements form validation with feedback and configuration version tracking

### charts.js
- **Primary Purpose**: Data visualization
- **Key Functions**:
  * `CreatureBox.Charts.init()`: Initialize charts module
  * `CreatureBox.Charts.renderPowerUsage()`: Render power usage chart
  * `CreatureBox.Charts.renderActivityTimeline()`: Render activity timeline
  * `CreatureBox.Charts.renderStorageUsage()`: Render storage usage chart
  * `CreatureBox.Charts.renderTemperature()`: Render temperature monitoring
  * `CreatureBox.Charts.renderSchedule()`: Render schedule visualization
  * `CreatureBox.Charts.updateCharts()`: Update all charts with new data
- **Dependencies**: Chart.js library, api.js, utils.js
- **Technical Notes**: Uses Chart.js for visualization with custom styling to match application theme

### utils.js
- **Primary Purpose**: Utility functions
- **Key Functions**:
  * `CreatureBox.Utils.formatDate()`: Format date/time values
  * `CreatureBox.Utils.formatBytes()`: Format file sizes
  * `CreatureBox.Utils.validateInput()`: Input validation helpers
  * `CreatureBox.Utils.debounce()`: Debounce function calls
  * `CreatureBox.Utils.throttle()`: Throttle function calls
  * `CreatureBox.Utils.parseQueryString()`: Parse URL query parameters
  * `CreatureBox.Utils.generateId()`: Generate unique IDs
  * `CreatureBox.Utils.deepClone()`: Deep clone objects
- **Dependencies**: None
- **Technical Notes**: Shared helper functions used across multiple modules

### api.js
- **Primary Purpose**: API client for backend communication
- **Key Functions**:
  * `CreatureBox.API.init()`: Initialize API client
  * `CreatureBox.API.request()`: Generic request method
  * `CreatureBox.API.get()`: GET request
  * `CreatureBox.API.post()`: POST request
  * `CreatureBox.API.put()`: PUT request
  * `CreatureBox.API.delete()`: DELETE request
  * `CreatureBox.API.handleError()`: Error handling
  * `CreatureBox.API.setAuthToken()`: Set authentication token
- **Dependencies**: utils.js
- **Technical Notes**: Wraps fetch API with authentication, error handling, and request/response processing

### forms.js
- **Primary Purpose**: Form validation and processing
- **Key Functions**:
  * `CreatureBox.Forms.init()`: Initialize forms module
  * `CreatureBox.Forms.validate()`: Validate form inputs
  * `CreatureBox.Forms.serializeForm()`: Serialize form data
  * `CreatureBox.Forms.deserializeForm()`: Populate form with data
  * `CreatureBox.Forms.showValidationMessage()`: Display validation messages
  * `CreatureBox.Forms.clearValidation()`: Clear validation messages
  * `CreatureBox.Forms.handleSubmit()`: Handle form submission
  * `CreatureBox.Forms.autoSave()`: Auto-save form changes
- **Dependencies**: utils.js
- **Technical Notes**: Implements client-side validation with custom rules and error messages

### ui.js
- **Primary Purpose**: UI components and effects
- **Key Functions**:
  * `CreatureBox.UI.init()`: Initialize UI components
  * `CreatureBox.UI.showModal()`: Display modal dialog
  * `CreatureBox.UI.hideModal()`: Hide modal dialog
  * `CreatureBox.UI.showNotification()`: Show notification
  * `CreatureBox.UI.toggleElement()`: Toggle element visibility
  * `CreatureBox.UI.createLoader()`: Create loading indicator
  * `CreatureBox.UI.accordions()`: Initialize accordion components
  * `CreatureBox.UI.tabs()`: Initialize tab components
  * `CreatureBox.UI.dropdowns()`: Initialize dropdown menus
- **Dependencies**: utils.js
- **Technical Notes**: Provides reusable UI components with accessibility features

### storage.js
- **Primary Purpose**: Local storage management
- **Key Functions**:
  * `CreatureBox.Storage.init()`: Initialize storage module
  * `CreatureBox.Storage.get()`: Get value from storage
  * `CreatureBox.Storage.set()`: Set value in storage
  * `CreatureBox.Storage.remove()`: Remove value from storage
  * `CreatureBox.Storage.clear()`: Clear all storage
  * `CreatureBox.Storage.getJSON()`: Get and parse JSON value
  * `CreatureBox.Storage.setJSON()`: Stringify and store JSON value
  * `CreatureBox.Storage.migrateData()`: Migrate data between versions
- **Dependencies**: utils.js
- **Technical Notes**: Abstracts browser storage with fallbacks and handles data versioning

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Web Static](../web-interface/static.md): Parent module
  * [Web Static CSS](./src-web-static-css.md): Styling for elements controlled by JavaScript
  * [Web Templates](../web-interface/templates.md): HTML templates with script references
- **Depends On**:
  * Browser JavaScript API
  * Optional third-party libraries (e.g., Chart.js)
  * Backend API endpoints
  * HTML DOM structure
- **Used By**:
  * Web interface pages
  * User interactions
  * Dynamic content updates

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Camera Control Interface**:
   - **Description**: Controlling the camera remotely through the web interface.
   - **Example**: 
     ```javascript
     // In camera.js
     CreatureBox.Camera = (function() {
       let previewElement;
       let captureButton;
       let previewActive = false;
       
       function init(options) {
         previewElement = options.previewElement;
         captureButton = options.captureButton;
         
         // Attach event listeners
         captureButton.addEventListener('click', capture);
         
         // Initialize preview
         getStatus().then(status => {
           if (status.available) {
             enableControls();
           } else {
             disableControls('Camera not available');
           }
         });
       }
       
       function startPreview() {
         if (previewActive) return;
         
         return CreatureBox.API.post('/api/camera/preview/start')
           .then(response => {
             if (response.success) {
               previewActive = true;
               // Setup preview stream or polling
               setupPreviewStream();
               return true;
             }
             return false;
           })
           .catch(error => {
             CreatureBox.UI.showNotification('Failed to start preview', 'error');
             console.error('Preview error:', error);
             return false;
           });
       }
       
       function capture() {
         CreatureBox.UI.showLoader(previewElement);
         
         return CreatureBox.API.post('/api/camera/capture')
           .then(response => {
             CreatureBox.UI.hideLoader(previewElement);
             if (response.success) {
               CreatureBox.UI.showNotification('Image captured successfully');
               // Show the captured image
               showCapturedImage(response.data.imagePath);
               
               // Refresh gallery if open
               CreatureBox.EventBus.publish('gallery:refresh');
               return response.data;
             } else {
               throw new Error(response.message || 'Capture failed');
             }
           })
           .catch(error => {
             CreatureBox.UI.hideLoader(previewElement);
             CreatureBox.UI.showNotification('Failed to capture image', 'error');
             console.error('Capture error:', error);
             return null;
           });
       }
       
       // Additional methods...
       
       return {
         init: init,
         startPreview: startPreview,
         stopPreview: stopPreview,
         capture: capture,
         updateSettings: updateSettings,
         toggleAttraction: toggleAttraction,
         getStatus: getStatus
       };
     })();
     ```

2. **Photo Gallery Implementation**:
   - **Description**: Browsing and managing captured photos with lazy loading.
   - **Example**: 
     ```javascript
     // In gallery.js
     CreatureBox.Gallery = (function() {
       let container;
       let gridContainer;
       let currentPage = 1;
       let totalPages = 1;
       let itemsPerPage = 20;
       let currentFilter = 'all';
       
       function init(options) {
         container = options.container;
         gridContainer = container.querySelector('.gallery-grid');
         itemsPerPage = options.itemsPerPage || itemsPerPage;
         
         // Set up pagination controls
         setupPagination();
         
         // Initial load
         loadImages(currentPage, currentFilter);
         
         // Set up infinite scroll if enabled
         if (options.infiniteScroll) {
           setupInfiniteScroll();
         }
         
         // Listen for events
         CreatureBox.EventBus.subscribe('gallery:refresh', () => {
           loadImages(1, currentFilter, true);
         });
       }
       
       function loadImages(page, filter, forceRefresh = false) {
         currentPage = page || 1;
         currentFilter = filter || currentFilter;
         
         // Check cache unless forced refresh
         if (!forceRefresh) {
           const cachedData = CreatureBox.Storage.getJSON(`gallery_${currentFilter}_${currentPage}`);
           if (cachedData && cachedData.timestamp > Date.now() - 300000) { // 5 min cache
             renderThumbnails(cachedData.images);
             updatePagination(cachedData.currentPage, cachedData.totalPages);
             return Promise.resolve(cachedData);
           }
         }
         
         // Show loading state
         CreatureBox.UI.showLoader(gridContainer);
         
         // Fetch from API
         return CreatureBox.API.get('/api/images', {
           page: currentPage, 
           limit: itemsPerPage,
           filter: currentFilter
         }).then(response => {
           CreatureBox.UI.hideLoader(gridContainer);
           
           if (response.success) {
             const data = {
               images: response.data.images,
               currentPage: response.data.page,
               totalPages: response.data.totalPages,
               timestamp: Date.now()
             };
             
             // Cache the results
             CreatureBox.Storage.setJSON(`gallery_${currentFilter}_${currentPage}`, data);
             
             // Render the images
             renderThumbnails(data.images);
             updatePagination(data.currentPage, data.totalPages);
             
             return data;
           } else {
             CreatureBox.UI.showNotification('Failed to load images', 'error');
             return null;
           }
         }).catch(error => {
           CreatureBox.UI.hideLoader(gridContainer);
           CreatureBox.UI.showNotification('Error loading gallery', 'error');
           console.error('Gallery error:', error);
           return null;
         });
       }
       
       function renderThumbnails(images) {
         // Clear existing content
         gridContainer.innerHTML = '';
         
         if (images.length === 0) {
           gridContainer.innerHTML = '<div class="empty-state">No images found</div>';
           return;
         }
         
         // Create image elements
         images.forEach(image => {
           const thumbnail = document.createElement('div');
           thumbnail.className = 'thumbnail';
           thumbnail.dataset.id = image.id;
           
           thumbnail.innerHTML = `
             <div class="thumbnail-img">
               <img src="${image.thumbnailUrl}" alt="${image.filename}" loading="lazy">
             </div>
             <div class="thumbnail-info">
               <span class="filename">${image.filename}</span>
               <span class="date">${CreatureBox.Utils.formatDate(image.createdAt)}</span>
             </div>
           `;
           
           // Add click handler
           thumbnail.addEventListener('click', () => {
             showLightbox(image);
           });
           
           gridContainer.appendChild(thumbnail);
         });
       }
       
       // Additional methods...
       
       return {
         init: init,
         loadImages: loadImages,
         renderThumbnails: renderThumbnails,
         showLightbox: showLightbox,
         filter: filter,
         deleteImage: deleteImage,
         downloadImage: downloadImage,
         bulkActions: bulkActions
       };
     })();
     ```

3. **Settings Management**:
   - **Description**: Configuring system settings through the web interface.
   - **Example**: 
     ```javascript
     // In settings.js
     CreatureBox.Settings = (function() {
       let form;
       let saveButton;
       let resetButton;
       let lastSavedConfig = null;
       
       function init(options) {
         form = options.form;
         saveButton = form.querySelector('.save-button');
         resetButton = form.querySelector('.reset-button');
         
         // Attach event listeners
         form.addEventListener('submit', handleSubmit);
         resetButton.addEventListener('click', restoreDefaults);
         
         // Setup change tracking
         setupChangeTracking();
         
         // Load initial config
         loadConfig();
       }
       
       function loadConfig() {
         return CreatureBox.API.get('/api/settings')
           .then(response => {
             if (response.success) {
               lastSavedConfig = response.data;
               
               // Populate form with settings
               CreatureBox.Forms.deserializeForm(form, response.data);
               
               // Enable form
               enableForm();
               
               return response.data;
             } else {
               throw new Error(response.message || 'Failed to load settings');
             }
           })
           .catch(error => {
             CreatureBox.UI.showNotification('Failed to load settings', 'error');
             console.error('Settings load error:', error);
             return null;
           });
       }
       
       function saveConfig(config) {
         // Show saving indicator
         setSaveButtonSaving(true);
         
         return CreatureBox.API.put('/api/settings', config)
           .then(response => {
             setSaveButtonSaving(false);
             
             if (response.success) {
               lastSavedConfig = response.data;
               CreatureBox.UI.showNotification('Settings saved successfully');
               
               // Update form with any server-modified values
               CreatureBox.Forms.deserializeForm(form, response.data);
               
               // Broadcast settings change event
               CreatureBox.EventBus.publish('settings:updated', response.data);
               
               return response.data;
             } else {
               throw new Error(response.message || 'Failed to save settings');
             }
           })
           .catch(error => {
             setSaveButtonSaving(false);
             CreatureBox.UI.showNotification('Failed to save settings', 'error');
             console.error('Settings save error:', error);
             return null;
           });
       }
       
       // Additional methods...
       
       return {
         init: init,
         loadConfig: loadConfig,
         saveConfig: saveConfig,
         validateForm: validateForm,
         restoreDefaults: restoreDefaults,
         exportConfig: exportConfig,
         importConfig: importConfig,
         applyChanges: applyChanges
       };
     })();
     ```

4. **Data Visualization**:
   - **Description**: Visualizing system data with interactive charts.
   - **Example**: 
     ```javascript
     // In charts.js
     CreatureBox.Charts = (function() {
       let container;
       let charts = {};
       let updateInterval;
       
       function init(options) {
         container = options.container;
         
         // Create chart containers if needed
         setupChartContainers();
         
         // Create initial charts
         createCharts();
         
         // Set up periodic updates if requested
         if (options.autoUpdate) {
           startAutoUpdates(options.updateInterval || 60000);
         }
       }
       
       function renderPowerUsage() {
         return CreatureBox.API.get('/api/metrics/power')
           .then(response => {
             if (response.success) {
               const data = response.data;
               
               if (!charts.powerUsage) {
                 // Create new chart
                 const ctx = document.getElementById('power-usage-chart').getContext('2d');
                 charts.powerUsage = new Chart(ctx, {
                   type: 'line',
                   data: {
                     labels: data.labels,
                     datasets: [{
                       label: 'Power Usage (mA)',
                       data: data.values,
                       borderColor: '#3e95cd',
                       fill: true,
                       backgroundColor: 'rgba(62, 149, 205, 0.1)',
                       tension: 0.3
                     }]
                   },
                   options: {
                     responsive: true,
                     maintainAspectRatio: false,
                     plugins: {
                       legend: {
                         display: true,
                         position: 'top'
                       },
                       tooltip: {
                         mode: 'index',
                         intersect: false
                       }
                     },
                     scales: {
                       x: {
                         display: true,
                         title: {
                           display: true,
                           text: 'Time'
                         }
                       },
                       y: {
                         display: true,
                         title: {
                           display: true,
                           text: 'Power (mA)'
                         },
                         suggestedMin: 0
                       }
                     }
                   }
                 });
               } else {
                 // Update existing chart
                 charts.powerUsage.data.labels = data.labels;
                 charts.powerUsage.data.datasets[0].data = data.values;
                 charts.powerUsage.update();
               }
               
               return charts.powerUsage;
             } else {
               throw new Error(response.message || 'Failed to load power usage data');
             }
           })
           .catch(error => {
             console.error('Power usage chart error:', error);
             return null;
           });
       }
       
       // Additional methods...
       
       return {
         init: init,
         renderPowerUsage: renderPowerUsage,
         renderActivityTimeline: renderActivityTimeline,
         renderStorageUsage: renderStorageUsage,
         renderTemperature: renderTemperature,
         renderSchedule: renderSchedule,
         updateCharts: updateCharts
       };
     })();
     ```

</div>
</details>
