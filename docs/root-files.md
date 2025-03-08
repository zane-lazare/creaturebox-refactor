---
layout: default
title: Root Files
parent: Root Directory
nav_order: 1
permalink: /root/files/
---

# Root Files Documentation

{% include navigation.html %}

## Overview

The root files in the CreatureBox repository serve as the foundation for system installation, configuration, and documentation. These files provide essential functionality for setup, dependency management, and project information.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The root files in the CreatureBox repository serve several critical purposes:

- Provide entry points for system installation and configuration
- Define dependencies and requirements for reproducible builds
- Document project information, usage, and development guidelines
- Enable version control and proper project management
- Support development workflows and continuous integration
- Establish standard environment configuration

These files represent the entry point to the project for both users and developers, making them essential for proper system function and contribution.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Description |
|----------|------|------|-------------|
| install.sh | Shell | 2.5 KB | Primary installation script |
| pre_install_check.py | Python | 1.8 KB | System requirements verification |
| verify_installation.py | Python | 1.5 KB | Post-installation validation |
| requirements.txt | Text | 0.9 KB | Python package dependencies |
| package.json | JSON | 1.2 KB | Node.js dependencies and scripts |
| README.md | Markdown | 3.4 KB | Project documentation and overview |
| .env.example | Text | 0.5 KB | Environment variable template |
| LICENSE | Text | 1.1 KB | Project license information |
| CHANGELOG.md | Markdown | 2.2 KB | Version history and changes |
| .gitignore | Text | 0.7 KB | Version control exclusions |
| setup.cfg | INI | 0.4 KB | Python package configuration |
| pyproject.toml | TOML | 0.3 KB | Python build system configuration |
| Makefile | Make | 0.8 KB | Build and automation commands |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### Installation and Validation

#### install.sh
- **Primary Purpose**: Main system installation script
- **Key Functions**:
  * System dependency installation
  * Component configuration
  * Service setup
  * Permission management
  * Database initialization
- **Dependencies**: Bash shell, Linux utilities
- **Technical Notes**: Supports different installation modes (standard, development, upgrade)

#### pre_install_check.py
- **Primary Purpose**: Validates system compatibility
- **Key Functions**:
  * Hardware validation
  * Dependency checking
  * Disk space verification
  * Permission validation
  * Network connectivity testing
- **Dependencies**: Python 3.6+
- **Technical Notes**: Exit codes indicate specific validation failures

#### verify_installation.py
- **Primary Purpose**: Post-installation validation
- **Key Functions**:
  * Service status verification
  * Component integration testing
  * Configuration validation
  * Performance baseline measurement
  * Diagnostic report generation
- **Dependencies**: Installed CreatureBox system
- **Technical Notes**: Can generate both human and machine-readable reports

### Dependency Management

#### requirements.txt
- **Primary Purpose**: Python dependency specification
- **Key Contents**:
  * Web framework dependencies (Flask)
  * Database libraries (SQLAlchemy)
  * Image processing (Pillow)
  * Hardware interfaces (RPi.GPIO, picamera)
  * Utility libraries
- **Dependencies**: pip package manager
- **Technical Notes**: Version-pinned for reproducibility

#### package.json
- **Primary Purpose**: Node.js package definition
- **Key Contents**:
  * Frontend dependencies
  * Build scripts
  * Development tools
  * Project metadata
  * Script commands
- **Dependencies**: npm or yarn
- **Technical Notes**: Used primarily for web UI components

#### setup.cfg
- **Primary Purpose**: Python package configuration
- **Key Contents**:
  * Package metadata
  * Entry point definitions
  * Tool configurations
  * Test settings
- **Dependencies**: Python setuptools
- **Technical Notes**: Used in conjunction with pyproject.toml

#### pyproject.toml
- **Primary Purpose**: Modern Python build config
- **Key Contents**:
  * Build system requirements
  * Tool configurations
  * Development dependencies
- **Dependencies**: Python build tools
- **Technical Notes**: PEP 518 compliant build specification

### Project Documentation

#### README.md
- **Primary Purpose**: Project introduction and overview
- **Key Contents**:
  * Project description
  * Installation instructions
  * Usage examples
  * Configuration options
  * Screenshots/diagrams
  * Contribution guidelines
- **Dependencies**: None
- **Technical Notes**: Primary entry point for new users

#### LICENSE
- **Primary Purpose**: Legal terms of use
- **Key Contents**:
  * MIT license text
  * Copyright notice
  * Rights and limitations
  * Liability disclaimers
- **Dependencies**: None
- **Technical Notes**: Applies to all project code unless specified

#### CHANGELOG.md
- **Primary Purpose**: Version history tracking
- **Key Contents**:
  * Version numbers
  * Release dates
  * New features
  * Bug fixes
  * Breaking changes
  * Migration instructions
- **Dependencies**: None
- **Technical Notes**: Follows semantic versioning principles

### Configuration and Automation

#### .env.example
- **Primary Purpose**: Environment variable template
- **Key Contents**:
  * Database connection strings
  * API endpoints
  * Feature flags
  * Path configurations
  * Debug settings
- **Dependencies**: None
- **Technical Notes**: Must be copied to .env and customized

#### .gitignore
- **Primary Purpose**: Version control exclusions
- **Key Contents**:
  * Build artifacts
  * Local environment files
  * Sensitive information
  * Temporary files
  * Editor-specific files
- **Dependencies**: Git
- **Technical Notes**: Prevents sensitive or generated content from being committed

#### Makefile
- **Primary Purpose**: Build and automation tasks
- **Key Commands**:
  * `make install`: Install dependencies
  * `make test`: Run test suite
  * `make lint`: Code quality checks
  * `make clean`: Remove build artifacts
  * `make build`: Build distributable package
- **Dependencies**: GNU Make
- **Technical Notes**: Provides shorthand for common development tasks

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Root Directory](../root.md): Parent documentation
  * [Deployment](../deployment.md): Installation artifacts
  * [Source Directory](../src.md): Code being installed
  * [Configuration](../core-components/configuration.md): System configuration
- **Depends On**:
  * Operating system utilities
  * Language environments (Python, Node.js)
  * Package managers (pip, npm)
  * Build tools (make, setuptools)
- **Used By**:
  * System installers
  * Developers
  * CI/CD pipelines
  * Package distribution systems

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Standard Installation**:
   - **Description**: Installing CreatureBox on a new system
   - **Example**:
     ```bash
     # Clone repository
     git clone https://github.com/zane-lazare/creaturebox-refactor.git
     cd creaturebox-refactor
     
     # Verify system compatibility
     python3 pre_install_check.py
     
     # Run installation
     sudo ./install.sh
     
     # Verify successful installation
     python3 verify_installation.py
     ```

2. **Developer Environment Setup**:
   - **Description**: Setting up for code contribution
   - **Example**:
     ```bash
     # Clone repository
     git clone https://github.com/zane-lazare/creaturebox-refactor.git
     cd creaturebox-refactor
     
     # Create virtual environment
     python -m venv venv
     source venv/bin/activate
     
     # Install dependencies
     pip install -r requirements.txt
     npm install
     
     # Configure environment
     cp .env.example .env
     nano .env  # Edit as needed
     
     # Run development server
     make dev
     ```

3. **Custom Configuration**:
   - **Description**: Customizing installation parameters
   - **Example**:
     ```bash
     # Copy environment template
     cp .env.example .env
     
     # Edit environment file
     nano .env
     
     # Apply customized environment settings
     export $(grep -v '^#' .env | xargs)
     
     # Install with custom options
     ./install.sh --custom-config
     ```

4. **Building Release Package**:
   - **Description**: Creating distributable package
   - **Example**:
     ```bash
     # Install build dependencies
     pip install -r requirements-dev.txt
     
     # Run tests to verify functionality
     make test
     
     # Clean previous builds
     make clean
     
     # Build package
     make build
     
     # The resulting package will be in dist/
     ls -la dist/
     ```

</div>
</details>
