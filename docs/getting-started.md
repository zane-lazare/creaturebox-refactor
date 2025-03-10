# Getting Started with CreatureBox Refactored

This guide will walk you through the process of setting up and running the CreatureBox Refactored platform.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/zane-lazare/creaturebox-refactor.git
cd creaturebox-refactor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the System

Copy the example configuration file and modify it as needed:

```bash
cp config/example.config.ini config/config.ini
```

Edit `config/config.ini` with your specific settings.

### 4. Start the Application

```bash
python src/app.py
```

The web interface should now be accessible at `http://localhost:5000`.

## Configuration Options

See the [Configuration](components/config.md) section for detailed information on available configuration options.

## Next Steps

- [Web Interface Guide](components/web.md)
- [Power Management](components/power.md)
- [Software Components](components/software.md)
