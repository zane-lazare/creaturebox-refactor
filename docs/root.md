# Root Directory Documentation

{% include navigation.html %}

## Overview

The Root Directory contains the essential installation, verification, and setup scripts that enable deployment and configuration of the CreatureBox system, along with project documentation and dependency definitions.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The repository root directory contains the primary project setup files and installation scripts that facilitate the deployment and configuration of the CreatureBox system. This includes:

- Installation scripts for setting up the environment
- Pre-installation checks for system requirements
- Verification tools for validating successful setup
- Documentation for the project
- Dependency management files
- Project metadata and configuration files

These files serve as the entry point for new installations and provide the foundation for the system deployment process.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Purpose |
|----------|------|------|---------|
| install.sh | Shell | 2.5 KB | Main installation script |
| pre_install_check.py | Python | 1.8 KB | System requirements verification |
| verify_installation.py | Python | 1.5 KB | Post-installation validation |
| requirements.txt | Text | 0.9 KB | Python dependencies |
| package.json | JSON | 1.2 KB | Node.js dependencies |
| README.md | Markdown | 3.4 KB | Project documentation |
| .env.example | Text | 0.5 KB | Environment variable template |
| LICENSE | Text | 1.1 KB | License information |
| CHANGELOG.md | Markdown | 2.2 KB | Version history |
| .gitignore | Text | 0.7 KB | Git ignore patterns |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### Installation Scripts

#### install.sh
- **Primary Purpose**: Main system installation script
- **Key Functions**:
  * Checks system compatibility
  * Installs required dependencies
  * Sets up directory structure
  * Configures services
  * Initializes databases
  * Sets up user permissions
  * Performs initial system configuration
- **Dependencies**:
  * Bash shell
  * System utilities (apt, systemd)
- **Technical Notes**: Must be run with root privileges

#### pre_install_check.py
- **Primary Purpose**: Verifies system meets requirements
- **Key Functions**:
  * Checks hardware compatibility
  * Verifies available disk space
  * Validates Python version
  * Checks for required system utilities
  * Tests camera connectivity
  * Validates network configuration
- **Dependencies**:
  * Python 3.6+
  * Hardware access libraries
- **Technical Notes**: Returns non-zero exit code if requirements not met

#### verify_installation.py
- **Primary Purpose**: Validates successful installation
- **Key Functions**:
  * Tests system services
  * Verifies database connections
  * Checks camera functionality
  * Tests web server configuration
  * Validates user permissions
  * Performs end-to-end system test
- **Dependencies**:
  * Installed CreatureBox components
- **Technical Notes**: Generates detailed report of system status

### Project Configuration

#### requirements.txt
- **Primary Purpose**: Python dependency definitions
- **Key Contents**:
  * Flask and extensions (web framework)
  * Pillow (image processing)
  * SQLAlchemy (database ORM)
  * Requests (HTTP client)
  * Gunicorn (WSGI server)
  * Hardware interface libraries
- **Dependencies**:
  * pip (Python package manager)
- **Technical Notes**: Version-pinned for reproducible installations

#### package.json
- **Primary Purpose**: Node.js dependency definitions
- **Key Contents**:
  * Web UI dependencies
  * Development tools
  * Build scripts
  * Package metadata
- **Dependencies**:
  * npm or yarn (Node.js package managers)
- **Technical Notes**: Used primarily for web interface development

### Documentation

#### README.md
- **Primary Purpose**: Project overview and quick start
- **Key Contents**:
  * Project description
  * Installation instructions
  * Basic usage guide
  * System requirements
  * Troubleshooting information
  * Contributing guidelines
- **Technical Notes**: Entry point for new users

#### .env.example
- **Primary Purpose**: Environment variable template
- **Key Contents**:
  * Database connection settings
  * API keys and secrets
  * File paths and directories
  * Feature flags
  * Debug settings
- **Technical Notes**: Must be copied to .env and populated with actual values

#### LICENSE
- **Primary Purpose**: Legal licensing information
- **Key Contents**:
  * License type (MIT)
  * Copyright notice
  * Usage permissions
  * Liability disclaimers
- **Technical Notes**: Applies to all code in the repository

#### CHANGELOG.md
- **Primary Purpose**: Version history tracking
- **Key Contents**:
  * Version numbers
  * Release dates
  * Feature additions
  * Bug fixes
  * Breaking changes
- **Technical Notes**: Follows semantic versioning

#### .gitignore
- **Primary Purpose**: Git version control exclusions
- **Key Contents**:
  * Generated files
  * Environment-specific files
  * Sensitive configuration
  * Dependencies and build artifacts
  * Temporary files
- **Technical Notes**: Prevents accidental commit of sensitive or generated content

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Deployment](./deployment.md): Installation scripts setup deployment files
  * [Source Directory](./src.md): Installs and configures source components
- **Depends On**:
  * Operating system services and utilities
  * Python and Node.js environments
  * Hardware interfaces
- **Used By**:
  * Initial system setup process
  * Continuous integration/deployment pipeline
  * System administrators

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Initial System Installation**:
   - **Description**: Setting up CreatureBox on a new device.
   - **Example**: 
     ```bash
     # First verify system compatibility
     python3 pre_install_check.py
     
     # If checks pass, run the installation
     sudo ./install.sh
     
     # Verify successful installation
     python3 verify_installation.py --verbose
     ```

2. **Development Environment Setup**:
   - **Description**: Setting up a development environment for contributing.
   - **Example**: 
     ```bash
     # Clone the repository
     git clone https://github.com/zane-lazare/creaturebox-refactor.git
     cd creaturebox-refactor
     
     # Install Python dependencies
     python -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     
     # Install Node.js dependencies for web interface
     npm install
     
     # Configure environment
     cp .env.example .env
     # Edit .env with appropriate settings
     
     # Run in development mode
     ./install.sh --dev-mode
     ```

3. **System Upgrade**:
   - **Description**: Upgrading an existing installation.
   - **Example**: 
     ```bash
     # Stop services
     sudo systemctl stop creaturebox.service
     
     # Backup current configuration
     ./install.sh --backup-config
     
     # Perform upgrade
     sudo ./install.sh --upgrade
     
     # Verify upgrade
     python3 verify_installation.py --upgrade-check
     
     # Restart services
     sudo systemctl start creaturebox.service
     ```

4. **Troubleshooting Installation Issues**:
   - **Description**: Diagnosing and fixing installation problems.
   - **Example**: 
     ```bash
     # Run pre-installation check with detailed output
     python3 pre_install_check.py --verbose
     
     # Check system dependencies
     ./install.sh --check-dependencies
     
     # Run verification with debug information
     python3 verify_installation.py --debug
     
     # Generate system report for support
     ./install.sh --generate-report > system_report.txt
     ```

</div>
</details>
