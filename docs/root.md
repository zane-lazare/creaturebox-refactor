# Root Directory Documentation

## Directory Purpose
The root directory serves as the entry point and primary organizational level for the CreatureBox project. It contains essential setup scripts, configuration files, and documentation that enable users to install, understand, and use the CreatureBox wildlife monitoring system. This directory establishes the project structure and provides the foundation for all CreatureBox functionality.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| README.md | Markdown | 3.8 KB | Primary project documentation |
| install.sh | Shell Script | 1.2 KB | Main installation script |
| license.md | Markdown | 1.0 KB | MIT license information |
| pre_install_check.py | Python | 0.8 KB | System compatibility verification |
| pytest.ini | Configuration | 0.3 KB | PyTest configuration |
| requirements.txt | Text | 0.6 KB | Python dependency list |
| verify_installation.py | Python | 0.9 KB | Post-installation verification |

## Detailed File Descriptions

### README.md
- **Primary Purpose**: Provides comprehensive overview and documentation for the CreatureBox project
- **Key Sections**:
  * Project introduction and features list
  * Installation instructions
  * API endpoint documentation
  * Architecture overview
  * Development setup guide
- **Dependencies**: None (standalone documentation)
- **Technical Notes**: Written in GitHub-flavored Markdown

### install.sh
- **Primary Purpose**: Automates the installation process for the CreatureBox system
- **Key Functions**:
  * Dependency installation
  * Configuration file setup
  * Service registration
  * Permissions configuration
- **Dependencies**: 
  * Bash shell
  * Python 3.7+
  * pre_install_check.py (runs this first)
  * verify_installation.py (runs this after installation)
- **Technical Notes**: Contains error handling for failed installations

### license.md
- **Primary Purpose**: Defines the licensing terms (MIT) for the project
- **Key Sections**:
  * License text
  * Copyright notice
  * Usage permissions
- **Dependencies**: None
- **Technical Notes**: Standard MIT license format

### pre_install_check.py
- **Primary Purpose**: Verifies system compatibility before installation
- **Key Functions**:
  * `check_python_version()`: Ensures compatible Python version
  * `check_dependencies()`: Verifies required system packages
  * `check_disk_space()`: Ensures sufficient storage
- **Dependencies**: Python standard library
- **Technical Notes**: Exits with non-zero code if checks fail

### pytest.ini
- **Primary Purpose**: Configures pytest behavior for testing
- **Key Settings**:
  * Test discovery patterns
  * Plugin configuration
  * Test reporting options
- **Dependencies**: pytest
- **Technical Notes**: Used by the CI/CD pipeline and local development

### requirements.txt
- **Primary Purpose**: Defines Python package dependencies
- **Key Sections**:
  * Core dependencies
  * Optional dependencies
  * Version constraints
- **Dependencies**: pip (Python package manager)
- **Technical Notes**: Used during installation and for development environment setup

### verify_installation.py
- **Primary Purpose**: Confirms successful installation
- **Key Functions**:
  * `verify_files()`: Checks all required files are present
  * `verify_permissions()`: Validates file permissions
  * `verify_services()`: Tests service startup
- **Dependencies**: Python standard library
- **Technical Notes**: Called by install.sh after installation completes

## Relationship Documentation
- **Related To**: 
  * /deployment (deployment configurations)
  * /src (source code modules)
- **Depends On**:
  * External Python packages (specified in requirements.txt)
  * System services (systemd for service management)
- **Used By**:
  * End users during initial setup
  * Developers for project orientation
  * CI/CD systems for testing and deployment

## Use Cases
1. **System Installation**:
   - **Implementation**: The install.sh script conducts pre-installation checks, installs dependencies, and configures services.
   - **Example**: `./install.sh --target=/opt/creaturebox --user=pi`

2. **Project Understanding**:
   - **Implementation**: README.md provides comprehensive documentation about the system's capabilities.
   - **Example**: A new user reads the README.md to understand the API structure before development.

3. **Development Environment Setup**:
   - **Implementation**: requirements.txt specifies all dependencies for development.
   - **Example**: `pip install -r requirements.txt[dev]` to set up development dependencies.

4. **System Validation**:
   - **Implementation**: verify_installation.py confirms all components are correctly installed.
   - **Example**: `python verify_installation.py --verbose` to get detailed verification information.
