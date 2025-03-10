# Web Interface

The web interface provides a user-friendly dashboard for monitoring and controlling the CreatureBox system.

## Architecture

The web interface is built using:
- Flask (Python web framework)
- Bootstrap for responsive design
- Chart.js for data visualization
- JavaScript for interactive elements

## Key Components

### Flask Application

The Flask application serves as the backend for the web interface, handling API requests and rendering HTML templates.

```python
from flask import Flask
from flask_cors import CORS

def create_app():
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    from src.web.routes import register_routes
    register_routes(app)
    
    return app
```

### Routes

Routes are organized into blueprints for better code organization:

```python
from flask import Blueprint, render_template, jsonify

web_bp = Blueprint('web', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

@web_bp.route('/')
def index():
    """Render the main dashboard."""
    return render_template('index.html')

@api_bp.route('/system/status')
def get_status():
    """Return the system status as JSON."""
    # Get system status
    status = get_system_status()
    return jsonify(status)

def register_routes(app):
    """Register all blueprints with the app."""
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
```

### Templates

The web interface uses Jinja2 templates to render HTML:

- `templates/base.html`: Base template with common elements
- `templates/index.html`: Dashboard template
- `templates/settings.html`: System settings template

## Dashboard Panels

The dashboard is divided into several panels:

1. **System Status** - Shows overall system health and uptime
2. **Environmental Data** - Displays current temperature, humidity, and light levels
3. **Power Control** - Interface for managing power outlets
4. **Alerts** - Recent system alerts and notifications

## API Endpoints

The web interface communicates with the backend via API endpoints. Key endpoints:

- `GET /api/system/status` - Get system status
- `GET /api/environment/current` - Get current environmental data
- `GET /api/power/status` - Get power outlet status
- `PUT /api/power/outlet/{id}` - Control power outlet

## Authentication

The web interface uses session-based authentication:

1. Users log in via the login form
2. Upon successful authentication, a session is created
3. Protected routes check for a valid session
4. Sessions expire after a configurable timeout

## Development

### Running the Development Server

```bash
# From the project root
python -m src.web.app
```

The development server will be available at `http://localhost:5000`.

### Adding New Dashboard Panels

To add a new dashboard panel:

1. Create a new template in `templates/panels/`
2. Include the panel in `templates/index.html`
3. Add any necessary JavaScript to `static/js/`
4. Update the route handler to provide required data
