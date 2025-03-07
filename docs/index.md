# CreatureBox Documentation

Welcome to the CreatureBox documentation. This guide provides comprehensive information about the CreatureBox system architecture, components, and usage.

## Documentation Improvements

We've recently improved the documentation structure with:
- **Collapsible sections** for better navigation
- **Horizontal navigation menu** to quickly jump to sections
- **Proper table formatting** for file inventories
- **Consolidated content** to eliminate redundancy

See the [Documentation Cleanup Plan](./documentation-cleanup-plan.md) for details on the improvements.

## System Components

<div class="component-grid">
  <div class="component-card">
    <h3>Core System</h3>
    <ul>
      <li><a href="./root.md">Root Directory</a></li>
      <li><a href="./deployment.md">Deployment</a></li>
      <li><a href="./src.md">Source Directory</a></li>
    </ul>
  </div>

  <div class="component-card">
    <h3>Configuration</h3>
    <ul>
      <li><a href="./src-config.md">Configuration Module</a></li>
      <li><a href="./src-power.md">Power Management</a></li>
    </ul>
  </div>

  <div class="component-card">
    <h3>Software</h3>
    <ul>
      <li><a href="./src-software.md">Software Module</a></li>
      <li><a href="./src-software-scripts.md">Utility Scripts</a></li>
    </ul>
  </div>

  <div class="component-card">
    <h3>Web Interface</h3>
    <ul>
      <li><a href="./src-web.md">Web Core</a></li>
      <li><a href="./src-web-routes.md">Web Routes</a></li>
      <li><a href="./src-web-services.md">Web Services</a></li>
      <li><a href="./src-web-middleware.md">Web Middleware</a></li>
      <li><a href="./src-web-utils.md">Web Utilities</a></li>
      <li><a href="./src-web-tests.md">Web Tests</a></li>
      <li><a href="./src-web-static.md">Web Static Resources</a></li>
    </ul>
  </div>
</div>

## System Architecture

The CreatureBox system consists of the following high-level components:

1. **Hardware Control Layer**
   - Camera and sensor interfaces
   - Power management
   - External device control

2. **Core Software Layer**
   - Operational scripts
   - System management
   - Scheduling and automation

3. **Web Interface Layer**
   - Flask web application
   - RESTful API endpoints
   - User interface

4. **Deployment Layer**
   - Server configuration
   - Service management
   - Installation utilities

## Documentation Structure

Each module's documentation follows a consistent structure with these sections:

1. **Overview** - Brief introduction to the module
2. **Purpose** - Detailed explanation of the module's role
3. **File Inventory** - Complete listing of files with metadata
4. **File Descriptions** - In-depth analysis of each file
5. **Relationships** - Dependencies and connections
6. **Use Cases** - Concrete usage examples

All sections are collapsible to help you focus on the information you need.

## How to Navigate this Documentation

1. **Expand/Collapse Sections**: Click on any section header to expand or collapse it
2. **Jump to Sections**: Use the horizontal navigation menu below each page title
3. **Cross-reference Links**: Blue links will take you to related documentation
4. **Section Anchors**: Append `#section-id` to URLs to link directly to sections:
   - `#purpose` - Jump to purpose section
   - `#file-inventory` - Jump to file inventory
   - `#file-descriptions` - Jump to file descriptions
   - `#relationships` - Jump to relationship documentation
   - `#use-cases` - Jump to use cases

## Reference Materials

- [Component Map](./component-map.md) - Visual representation of system components
- [Repository Structure](./repository-manifest.md) - Complete file hierarchy
- [Documentation Template](./templates/document-template.md) - Template for creating documentation

## Getting Started

If you're new to the CreatureBox system, we recommend starting with:

1. [System Overview](./README.md)
2. [Installation Guide](./setup.md)
3. [Web Interface](./src-web.md)

<style>
.component-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-gap: 20px;
  margin: 30px 0;
}

.component-card {
  background: #f8f9fa;
  border-radius: 5px;
  padding: 15px 20px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.component-card h3 {
  margin-top: 0;
  border-bottom: 1px solid #e1e4e8;
  padding-bottom: 10px;
  color: #0366d6;
}

.component-card ul {
  padding-left: 20px;
}

.component-card li {
  margin-bottom: 5px;
}
</style>
