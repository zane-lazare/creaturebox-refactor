# deployment Directory Documentation

## Directory Purpose
The `deployment` directory contains configuration files necessary for deploying the CreatureBox application in a production environment. These files enable the application to run as a system service, be served through a production-grade web server, and handle higher loads efficiently. The configurations in this directory transform the application from a development-focused project into a robust, production-ready system that can operate reliably on Raspberry Pi hardware in field conditions.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| creaturebox.service | Systemd Service | 0.6 KB | System service configuration |
| gunicorn.conf.py | Python | 0.8 KB | WSGI server configuration |
| nginx.conf | Configuration | 1.2 KB | Web server configuration |

## Detailed File Descriptions

### creaturebox.service
- **Primary Purpose**: Configures the CreatureBox application as a systemd service for automatic startup and management
- **Key Sections**:
  * `[Unit]`: Service description and dependencies
  * `[Service]`: Execution configuration, environment, and restart policies
  * `[Install]`: System integration settings
- **Dependencies**:
  * systemd
  * gunicorn
  * Python 3.7+
- **Technical Notes**: 
  * Configured to restart on failure for reliability
  * Runs as a specific user (typically 'pi') with limited privileges
  * Starts after network services to ensure connectivity

### gunicorn.conf.py
- **Primary Purpose**: Configures the Gunicorn WSGI server for running the Flask application
- **Key Functions**:
  * Sets worker processes based on available CPU cores
  * Configures request timeout settings
  * Sets up access and error logging
  * Defines socket binding
- **Dependencies**:
  * Gunicorn
  * Multiprocessing module
- **Technical Notes**:
  * Optimized for Raspberry Pi hardware constraints
  * Includes graceful worker restart settings
  * Configures proper error handling and reporting

### nginx.conf
- **Primary Purpose**: Configures Nginx as a reverse proxy and static file server for the application
- **Key Sections**:
  * Server block configuration
  * Static file handling
  * Proxy settings for Gunicorn
  * Caching policies
  * Security headers
- **Dependencies**:
  * Nginx web server
  * Running Gunicorn service
- **Technical Notes**:
  * Optimized for serving static files efficiently
  * Configured for secure headers and proper content types
  * Includes gzip compression for bandwidth efficiency
  * Handles both HTTP and HTTPS configurations

## Relationship Documentation
- **Related To**:
  * Root directory (install.sh uses these files)
  * src/web directory (application being served)
- **Depends On**:
  * System services (systemd)
  * External software (Nginx, Gunicorn)
  * src/web/app.py (application entry point)
- **Used By**:
  * Production deployment process
  * System administrators
  * install.sh script

## Use Cases
1. **Automatic Service Management**:
   - **Implementation**: The creaturebox.service file enables the application to run as a system service that starts automatically on boot and restarts on failure.
   - **Example**: 
     ```bash
     # Service installation and control
     sudo cp deployment/creaturebox.service /etc/systemd/system/
     sudo systemctl daemon-reload
     sudo systemctl enable creaturebox.service
     sudo systemctl start creaturebox.service
     ```

2. **Production Web Serving**:
   - **Implementation**: The combination of gunicorn.conf.py and nginx.conf provides a robust production web serving setup.
   - **Example**: 
     ```
     # Gunicorn runs the Python application with multiple workers
     gunicorn -c deployment/gunicorn.conf.py 'src.web.app:create_app("production")'
     
     # Nginx serves as a reverse proxy, handling static files directly
     # and forwarding API requests to Gunicorn
     ```

3. **Optimized Performance**:
   - **Implementation**: Configuration settings in gunicorn.conf.py and nginx.conf optimize the application for Raspberry Pi hardware.
   - **Example**: The gunicorn.conf.py file automatically calculates optimal worker count based on available CPU cores:
     ```python
     workers = multiprocessing.cpu_count() * 2 + 1 if multiprocessing.cpu_count() <= 2 else multiprocessing.cpu_count()
     # Limits worker count on resource-constrained devices
     workers = min(workers, 8)
     ```

4. **Secure Deployment**:
   - **Implementation**: Security headers and best practices configured in nginx.conf.
   - **Example**: Headers configured in nginx.conf include:
     ```
     # Security headers
     add_header X-Content-Type-Options "nosniff";
     add_header X-Frame-Options "SAMEORIGIN";
     add_header Content-Security-Policy "default-src 'self';";
     ```
