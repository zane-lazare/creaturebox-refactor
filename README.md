# CreatureBox Refactored

A platform for managing and monitoring creature habitats with advanced automation and control features.

## Features

- Centralized monitoring system for environmental parameters
- Automated power management for habitat components
- Web-based control interface
- Configurable alerts and notifications
- Data logging and analysis

## Installation

CreatureBox now includes a unified installation script for easy setup:

```bash
chmod +x install.sh
./install.sh
```

The installation script will guide you through the process with easy-to-follow prompts.

For detailed installation options and requirements, see [INSTALL.md](INSTALL.md).

### Manual Installation (Alternative)

If you prefer to install components manually:

1. Clone the repository:
```bash
git clone https://github.com/zane-lazare/creaturebox-refactor.git
cd creaturebox-refactor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the system:
```bash
cp config/example.config.ini config/config.ini
# Edit config/config.ini with your specific settings
```

4. Start the application:
```bash
python src/app.py
```

The web interface should now be accessible at `http://localhost:5000`.

## Documentation

Full documentation is available at [https://zane-lazare.github.io/creaturebox-refactor/](https://zane-lazare.github.io/creaturebox-refactor/).

For local development, you can build and serve the documentation:
```bash
# Install MkDocs and required theme
pip install mkdocs mkdocs-material

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

## Components

- **Web Interface**: User-friendly dashboard for monitoring and control
- **Power Management**: Control and monitor power outlets
- **Software Components**: Core functionality including data collection and analysis
- **Configuration**: System settings and user preferences

## License

[MIT License](LICENSE)
