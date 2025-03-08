---
layout: default
title: Web Static CSS
parent: Web Interface
nav_order: 6
permalink: /src/web/static/css/
---

# Web Static CSS Documentation

{% include navigation.html %}

## Overview

The Web Static CSS documentation provides a detailed inventory and analysis of the CSS stylesheets that create the visual styling and responsive design for the CreatureBox web interface.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

This document catalogs the CSS files within the `src/web/static/css` directory that create the visual styling for the CreatureBox web interface. These stylesheets provide:

- Consistent visual appearance across the application
- Responsive design for different screen sizes
- Component styling for UI elements
- Dark mode/light mode theming
- Visual feedback for user interactions
- Accessibility features

The CSS architecture follows a modular approach, with separate files for different concerns to maintain code organization and facilitate maintenance.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Size | Description |
|----------|------|-------------|
| style.css | 24 KB | Main stylesheet with global styles |
| components.css | 15 KB | UI component styles |
| responsive.css | 8 KB | Mobile-responsive styles |
| dark-mode.css | 6 KB | Dark theme styles |
| forms.css | 10 KB | Form element styling |
| tables.css | 8 KB | Table and data display styling |
| animations.css | 4 KB | CSS animations and transitions |
| utilities.css | 6 KB | Utility classes for common adjustments |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### style.css
- **Primary Purpose**: Main stylesheet with global styles
- **Key Components**:
  * CSS reset and normalization
  * Typography definitions
  * Color variables and theme
  * Base element styling
  * Layout grid system
  * Main navigation styling
- **Dependencies**: None (root stylesheet)
- **Technical Notes**: Uses CSS variables for theming and consistent styling

### components.css
- **Primary Purpose**: Component-specific styling
- **Key Components**:
  * Button styles and variations
  * Card and panel components
  * Modal dialog styling
  * Alert and notification components
  * Tabs and accordion components
  * Dropdown menus
  * Badges and labels
- **Dependencies**: style.css
- **Technical Notes**: Follows BEM (Block Element Modifier) naming convention

### responsive.css
- **Primary Purpose**: Mobile-responsive design rules
- **Key Components**:
  * Media queries for different screen sizes
  * Mobile navigation menu
  * Responsive grid adjustments
  * Touch-friendly element sizing
  * Layout changes for small screens
  * Print styles
- **Dependencies**: style.css, components.css
- **Technical Notes**: Mobile-first approach with breakpoints for larger screens

### dark-mode.css
- **Primary Purpose**: Dark theme styling
- **Key Components**:
  * Dark color palette overrides
  * Reduced brightness for night usage
  * Contrast adjustments
  * Dark mode for code blocks and syntax highlighting
  * Theme transition effects
- **Dependencies**: style.css
- **Technical Notes**: Toggled via data-theme attribute on root element

### forms.css
- **Primary Purpose**: Form element styling
- **Key Components**:
  * Input field styling
  * Form layout and grouping
  * Validation styling
  * Checkbox and radio button styling
  * Select dropdowns
  * Range sliders
  * Date and time pickers
- **Dependencies**: style.css, components.css
- **Technical Notes**: Includes accessibility enhancements for form elements

### tables.css
- **Primary Purpose**: Table and data display styling
- **Key Components**:
  * Basic table styling
  * Responsive tables
  * Sortable table headers
  * Alternate row styling
  * Data grids
  * Row highlighting
  * Pagination controls
- **Dependencies**: style.css
- **Technical Notes**: Includes responsive behavior for tables on small screens

### animations.css
- **Primary Purpose**: CSS animations and transitions
- **Key Components**:
  * Fade in/out effects
  * Slide transitions
  * Loading indicators
  * Button click effects
  * Hover state animations
  * Page transition effects
- **Dependencies**: style.css
- **Technical Notes**: Designed to degrade gracefully when animations are disabled

### utilities.css
- **Primary Purpose**: Utility classes for common adjustments
- **Key Components**:
  * Spacing utilities (margin, padding)
  * Text alignment classes
  * Display and visibility helpers
  * Flexbox utilities
  * Border and shadow utilities
  * Color and background utilities
- **Dependencies**: style.css
- **Technical Notes**: Single-purpose utility classes following a functional CSS approach

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Web Static](../web-interface/static.md): Parent module
  * [Web Static JS](./src-web-static-js.md): JavaScript that interacts with styled elements
  * [Web Templates](../web-interface/templates.md): HTML templates where styles are applied
- **Depends On**:
  * HTML structure
  * Media query support in browsers
  * CSS Variables (custom properties)
  * Browser rendering engines
- **Used By**:
  * Web interface pages
  * HTML templates
  * Dynamic content rendered by JavaScript

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Responsive Layout**:
   - **Description**: Adapting the interface layout for different screen sizes.
   - **Example**: 
     ```css
     /* In responsive.css */
     /* Base mobile styles */
     .container {
       padding: 1rem;
     }
     
     /* Tablet styles */
     @media (min-width: 768px) {
       .container {
         padding: 2rem;
       }
       
       .grid {
         display: grid;
         grid-template-columns: repeat(2, 1fr);
         gap: 1rem;
       }
     }
     
     /* Desktop styles */
     @media (min-width: 1200px) {
       .container {
         max-width: 1140px;
         margin: 0 auto;
       }
       
       .grid {
         grid-template-columns: repeat(3, 1fr);
         gap: 2rem;
       }
     }
     ```

2. **Component Styling**:
   - **Description**: Styling reusable UI components with variations.
   - **Example**: 
     ```css
     /* In components.css */
     /* Button base styles */
     .btn {
       display: inline-block;
       padding: 0.5rem 1rem;
       border-radius: 4px;
       font-weight: 500;
       text-align: center;
       cursor: pointer;
       transition: all 0.3s ease;
     }
     
     /* Button variations */
     .btn--primary {
       background-color: var(--color-primary);
       color: white;
       border: 1px solid var(--color-primary);
     }
     
     .btn--secondary {
       background-color: var(--color-secondary);
       color: white;
       border: 1px solid var(--color-secondary);
     }
     
     .btn--outline {
       background-color: transparent;
       color: var(--color-primary);
       border: 1px solid var(--color-primary);
     }
     
     /* Button sizes */
     .btn--small {
       padding: 0.25rem 0.5rem;
       font-size: 0.875rem;
     }
     
     .btn--large {
       padding: 0.75rem 1.5rem;
       font-size: 1.125rem;
     }
     ```

3. **Dark Mode Implementation**:
   - **Description**: Implementing a dark color scheme for low-light environments.
   - **Example**: 
     ```css
     /* In dark-mode.css */
     /* Light mode (default) variables */
     :root {
       --bg-color: #ffffff;
       --text-color: #333333;
       --card-bg: #f5f5f5;
       --border-color: #e0e0e0;
       --shadow: 0 2px 4px rgba(0,0,0,0.1);
     }
     
     /* Dark mode variables */
     [data-theme="dark"] {
       --bg-color: #1a1a1a;
       --text-color: #f0f0f0;
       --card-bg: #2a2a2a;
       --border-color: #444444;
       --shadow: 0 2px 4px rgba(0,0,0,0.3);
     }
     
     /* Base elements using variables */
     body {
       background-color: var(--bg-color);
       color: var(--text-color);
       transition: background-color 0.3s ease, color 0.3s ease;
     }
     
     .card {
       background-color: var(--card-bg);
       border: 1px solid var(--border-color);
       box-shadow: var(--shadow);
     }
     ```

4. **Form Styling and Validation**:
   - **Description**: Styling form elements with validation feedback.
   - **Example**: 
     ```css
     /* In forms.css */
     /* Input base styling */
     .form-control {
       display: block;
       width: 100%;
       padding: 0.5rem 0.75rem;
       border: 1px solid var(--border-color);
       border-radius: 4px;
       font-size: 1rem;
       line-height: 1.5;
       transition: border-color 0.15s ease-in-out;
     }
     
     .form-control:focus {
       border-color: var(--color-primary);
       outline: 0;
       box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
     }
     
     /* Validation states */
     .form-control.is-valid {
       border-color: var(--color-success);
       background-image: url("data:image/svg+xml,...");
       background-repeat: no-repeat;
       background-position: right calc(0.375em + 0.1875rem) center;
       background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
     }
     
     .form-control.is-invalid {
       border-color: var(--color-danger);
       background-image: url("data:image/svg+xml,...");
       background-repeat: no-repeat;
       background-position: right calc(0.375em + 0.1875rem) center;
       background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
     }
     
     .invalid-feedback {
       display: none;
       width: 100%;
       margin-top: 0.25rem;
       font-size: 0.875rem;
       color: var(--color-danger);
     }
     
     .form-control.is-invalid ~ .invalid-feedback {
       display: block;
     }
     ```

</div>
</details>
