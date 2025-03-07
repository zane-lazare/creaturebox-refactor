# deployment/gunicorn.conf.py
"""Gunicorn configuration for CreatureBox web interface."""
import os
import multiprocessing

# Read environment variables for configuration
creaturebox_home = os.environ.get('CREATUREBOX_HOME', '/opt/creaturebox')
creaturebox_log_dir = os.environ.get('CREATUREBOX_LOG_DIR', '/var/log/creaturebox')

# Ensure log directory exists
os.makedirs(creaturebox_log_dir, exist_ok=True)

# Worker configuration - conservative to avoid conflicts with background job queue
workers = max(2, min(multiprocessing.cpu_count(), 4))  # 2-4 workers based on CPU count
threads = 1  # Single thread per worker to avoid conflicts with job queue
worker_class = 'sync'  # Use sync workers for compatibility with background jobs

# Avoid worker timeout for long-running background operations
timeout = 120  # 2 minutes timeout for worker operations
keepalive = 5  # Keep connections alive for 5 seconds

# Server socket
bind = os.environ.get('CREATUREBOX_BIND', '127.0.0.1:5000')

# Process naming
proc_name = 'creaturebox'
pythonpath = creaturebox_home

# Logging configuration
errorlog = os.path.join(creaturebox_log_dir, 'gunicorn_error.log')
accesslog = os.path.join(creaturebox_log_dir, 'gunicorn_access.log')
loglevel = os.environ.get('CREATUREBOX_LOG_LEVEL', 'info').lower()

# Access log format - consistent with internal logging
access_log_format = '%(h)s - %(m)s %(U)s - %(s)s - %(M).4fms'

# Graceful shutdown to allow background jobs to complete
graceful_timeout = 30

# Pre-load application to catch startup errors
preload_app = True

# Custom hooks for application lifecycle management
def on_starting(server):
    """Log when server is starting."""
    import logging
    logging.info("Gunicorn server is starting")

def on_exit(server):
    """Perform cleanup when server is shutting down."""
    import logging
    logging.info("Gunicorn server is shutting down")
