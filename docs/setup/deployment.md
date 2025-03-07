---
layout: default
title: Deployment
parent: Setup & Deployment
nav_order: 2
---

# Deployment

This documentation covers the production deployment of the CreatureBox system.

## Directory Purpose
The `deployment` directory contains configuration files necessary for deploying the CreatureBox application in a production environment. These files enable the application to run as a system service, be served through a production-grade web server, and handle higher loads efficiently. The configurations in this directory transform the application from a development-focused project into a robust, production-ready system that can operate reliably on Raspberry Pi hardware in field conditions.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| creaturebox.service | Systemd Service | 0.6 KB | System service configuration |
| gunicorn.conf.py | Python | 0.8 KB | WSGI server configuration |
| nginx.conf | Configuration | 1.2 KB | Web server configuration |

## Production Stack

The production deployment uses the following stack:

<div class="mermaid">
graph TD;
    Client[Web Browser] --> Nginx[Nginx Web Server];
    Nginx --> Static[Static Files];
    Nginx --> Gunicorn[Gunicorn WSGI Server];
    Gunicorn --> Flask[Flask Application];
    
    classDef client fill:#bbf,stroke:#333,stroke-width:1px;
    classDef server fill:#fbb,stroke:#333,stroke-width:1px;
    classDef app fill:#bfb,stroke:#333,stroke-width:1px;
    
    class Client client;
    class Nginx,Gunicorn server;
    class Flask app;
</div>

## Deployment Steps

### 1. Service Configuration

The `creaturebox.service` file configures the application as a systemd service:

```ini
[Unit]
Description=CreatureBox Web Interface
After=network.target

[Service]
User=pi
WorkingDirectory=/opt/creaturebox
ExecStart=/usr/local/bin/gunicorn -c /opt/creaturebox/deployment/gunicorn.conf.py 'src.web.app:create_app("production")'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Deploy by copying to the systemd directory:

```bash
sudo cp deployment/creaturebox.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable creaturebox
sudo systemctl start creaturebox
```

### 2. WSGI Server Setup

The `gunicorn.conf.py` file configures the Gunicorn WSGI server:

```python
# Gunicorn configuration
import multiprocessing

# Worker configuration
workers = multiprocessing.cpu_count() * 2 + 1
workers = min(workers, 8)  # Limit for Raspberry Pi resources
timeout = 120
keepalive = 5

# Logging
errorlog = '/var/log/creaturebox/gunicorn-error.log'
accesslog = '/var/log/creaturebox/gunicorn-access.log'
loglevel = 'info'

# Bind
bind = '127.0.0.1:5000'
```

### 3. Web Server Configuration

The `nginx.conf` file configures Nginx as a reverse proxy:

```nginx
server {
    listen 80;
    server_name localhost;

    access_log /var/log/nginx/creaturebox-access.log;
    error_log /var/log/nginx/creaturebox-error.log;

    location /static/ {
        alias /opt/creaturebox/src/web/static/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Deploy by copying to Nginx:

```bash
sudo cp deployment/nginx.conf /etc/nginx/sites-available/creaturebox
sudo ln -s /etc/nginx/sites-available/creaturebox /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

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

### 1. Field Deployment
The deployment configuration enables reliable operation in field conditions:
- Automatic service restarts if failures occur
- Efficient resource usage on limited hardware
- Performance optimization for slower networks

### 2. Remote Management
The deployed system can be remotely managed:
- Web interface accessible over local network
- Structured logs for troubleshooting
- Service monitoring via systemd

### 3. Multiple Device Support
The production deployment supports multiple simultaneous users:
- Worker process scaling based on hardware capability
- Static file caching for improved performance
- Request queuing during high load