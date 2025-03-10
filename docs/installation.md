# Installation Guide

## Prerequisites

Before installing CreatureBox, ensure you have:

- Python 3.8 or higher
- pip package manager
- Git (optional, but recommended)
- Virtual environment (recommended)

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/zane-lazare/creaturebox-refactor.git
cd creaturebox-refactor
```

### 2. Create Virtual Environment

```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initial Configuration

```bash
# Copy example configuration
cp config/example.config.ini config/config.ini

# Edit configuration as needed
nano config/config.ini
```

## Troubleshooting

- **Dependency Conflicts**: Ensure you're using a virtual environment
- **Python Version**: Verify you're using Python 3.8+
- **Permission Issues**: Use `sudo` carefully or prefer virtual environments

## Next Steps

- [Configure the System](configuration.md)
- [Explore Components](components/index.md)
