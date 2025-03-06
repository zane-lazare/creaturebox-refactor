# CreatureBox Web Interface

A web interface for controlling and monitoring CreatureBox wildlife monitoring systems.

## Features

- System monitoring and control
- Camera configuration and control
- Photo gallery management
- Scheduling and automation
- Network management
- Log viewing

## Installation

### Requirements

- Python 3.7+
- Raspberry Pi (tested on Pi 4 and Pi 5)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/creaturebox-refactor.git
cd creaturebox-refactor

# Install dependencies
pip install -r requirements.txt

# Install optional dependencies if needed
pip install -r requirements.txt[optional]

# Install development dependencies (for contributing)
pip install -r requirements.txt[dev]
```

## Usage

```bash
python -m src.web.app
```

Then navigate to `http://raspberrypi:5000` or `http://[IP_ADDRESS]:5000` in your browser.

## Development

This project uses a modular architecture:

- `src/web/routes/` - API route handlers
- `src/web/utils/` - Utility functions
- `src/web/services/` - Background services
- `src/web/tests/` - Tests

### Running Tests

```bash
pytest
```

## License

MIT
