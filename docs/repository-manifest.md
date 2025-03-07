---
layout: default
title: Repository Structure
nav_order: 8
permalink: /repository-manifest/
---

# Repository Structure Manifest

{% include navigation.html %}

## Overview

Detailed mapping of the repository's directory structure, capturing comprehensive metadata about each directory.

<details id="structure-summary">
<summary><h2>Structure Summary</h2></summary>
<div markdown="1">

- **Root Directories**: 
  * `deployment/`
  * `src/`

### Deployment Directory
- **Files**: 3
  * `creaturebox.service`
  * `gunicorn.conf.py`
  * `nginx.conf`

### Source Directory
**Subdirectories**:
1. `config/`
2. `power/`
3. `software/`
4. `web/`

#### Web Subdirectories
- `middleware/`
- `routes/`
- `services/`
- `static/`
- `tests/`
- `utils/`

</div>
</details>

<details id="manifest-metadata">
<summary><h2>Manifest Metadata</h2></summary>
<div markdown="1">

- Captures directory paths
- Tracks directory depth
- Counts files and subdirectories
- Lists files and subdirectories

</div>
</details>

<details id="generation-method">
<summary><h2>Generation Method</h2></summary>
<div markdown="1">

- Recursively mapped repository structure
- Provides comprehensive directory insights

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

- Project architecture visualization
- Dependency tracking
- Structural analysis
- Documentation mapping

</div>
</details>

## Documentation Map

The repository structure is reflected in the documentation organization:

- **[Core Components](./core-components/index.md)**
  - [Configuration](./core-components/configuration.md) - `src/config/`
  - [Power Management](./core-components/power-management.md) - `src/power/`
  - [Software Module](./core-components/software-module.md) - `src/software/`

- **[Web Interface](./web-interface.md)** - `src/web/`
  - [Core Web Components](./web-interface/core.md) - `src/web/`
  - [API Routes](./web-interface/routes.md) - `src/web/routes/`
  - [Middleware](./web-interface/middleware.md) - `src/web/middleware/`
  - [Services](./web-interface/services.md) - `src/web/services/`
  - [Utilities](./web-interface/utils.md) - `src/web/utils/`
  - [Static Resources](./web-interface/static.md) - `src/web/static/`
  - [Tests](./web-interface/tests.md) - `src/web/tests/`

- **Deployment Documentation**
  - [Deployment Configuration](./deployment.md) - `deployment/`
  - [Root Documentation](./root.md) - Root directory files