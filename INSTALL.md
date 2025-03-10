# CreatureBox Installation Guide

This document describes the new unified installation process for CreatureBox.

## Overview

CreatureBox now includes a single interactive installation script that combines:
- Pre-installation system checks
- Software installation
- Post-installation verification

## Directory Structure

```
CreatureBox-refactor/
├── install.sh            # Main installation script (entry point)
├── install/              # Installation directory
│   ├── pre_check.py      # System requirements check
│   ├── installer.py      # Installation logic
│   ├── verifier.py       # Verification logic
│   ├── utils.py          # Shared utility functions
│   └── deployment/        # Deployment configuration templates
│       ├── creaturebox.service  # Systemd service file
│       ├── gunicorn.conf.py     # Gunicorn configuration
│       └── nginx.conf           # Nginx configuration
└── src/                  # Main application code
```

## Quick Start

To install CreatureBox with the default settings, simply run:

```bash
chmod +x install.sh
./install.sh
```

The script will guide you through the installation process with clear prompts and feedback.

## Installation Options

The installation script supports several options:

```
OPTIONS:
  --help              Show help message
  --check-only        Only run pre-installation checks
  --install-only      Skip checks and proceed with installation
  --verify-only       Only verify an existing installation
  --non-interactive   Run in non-interactive mode (use defaults)
```

### Examples

```bash
# Run only the pre-installation checks
./install.sh --check-only

# Only verify an existing installation
./install.sh --verify-only

# Run a non-interactive installation (useful for automation)
./install.sh --non-interactive
```

## Dependencies

The installation script automatically installs all required dependencies listed in `requirements.txt`. The installer is configured to check for this file in both the repository root (standard location) and the `install/` directory.

## System Requirements

- Raspberry Pi (preferably Pi 4 or newer)
- Raspberry Pi OS (Bullseye or newer)
- Python 3.7+
- At least 1GB of free disk space
- Connected camera module
- Internet connection (for package installation)

## Post-Installation

After successful installation:

1. Access the web interface at:
   - http://creaturebox.local (from other devices on your network)
   - http://localhost:5000 (from this device)

2. Set up scheduled tasks using the provided crontab example:
   ```bash
   crontab -e
   ```
   Then add the entries from `~/CreatureBox/crontab.example`

## Troubleshooting

If you encounter any issues during installation:

1. Check the installation log at `~/creaturebox_install.log`
2. Run the verification to identify specific issues:
   ```bash
   ./install.sh --verify-only
   ```
3. For more advanced troubleshooting, examine the system information file generated during verification:
   ```bash
   cat ~/CreatureBox/system_info.json
   ```

## Manual Installation

If you prefer to run the installation steps manually, you can:

1. Run pre-installation checks:
   ```bash
   python3 install/pre_check.py
   ```

2. Run the installer:
   ```bash
   python3 install/installer.py
   ```

3. Verify the installation:
   ```bash
   python3 install/verifier.py
   ```
