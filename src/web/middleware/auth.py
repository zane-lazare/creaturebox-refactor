# src/web/middleware/auth.py
"""Authentication middleware for the CreatureBox web application."""
from flask import request, g, current_app, Response
from functools import wraps
import base64
import binascii
import logging
from typing import Dict, Callable, Optional, List, Union, Any

from ..error_handlers import APIError, ErrorCode

logger = logging.getLogger(__name__)

class BasicAuth:
    """Basic HTTP Authentication middleware."""
    
    def __init__(self, app=None, users=None, realm="CreatureBox API"):
        """Initialize the Basic authentication middleware.
        
        Args:
            app: The Flask app
            users: Dictionary of username:password pairs
            realm: Authentication realm name
        """
        self.users = users or {}
        self.realm = realm
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with a Flask app."""
        # Store self in app extensions
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['basic_auth'] = self
    
    def check_credentials(self, username: str, password: str) -> bool:
        """Check if credentials are valid.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            True if credentials are valid
        """
        return username in self.users and self.users[username] == password
    
    def authenticate(self):
        """Create authentication challenge response.
        
        Returns:
            Response with WWW-Authenticate header
        """
        response = Response(
            "Authentication required",
            401,
            {'WWW-Authenticate': f'Basic realm="{self.realm}"'}
        )
        return response
    
    def require_auth(self, view_function):
        """Decorator to require authentication for a view function.
        
        Args:
            view_function: Flask view function
            
        Returns:
            Decorated function
        """
        @wraps(view_function)
        def decorated(*args, **kwargs):
            auth = request.authorization
            
            if not auth:
                logger.warning(f"Authentication failed: No credentials provided")
                return self.authenticate()
                
            if not self.check_credentials(auth.username, auth.password):
                logger.warning(f"Authentication failed: Invalid credentials for {auth.username}")
                return self.authenticate()
            
            # Store authenticated user in g
            g.auth_user = auth.username
            
            return view_function(*args, **kwargs)
        return decorated


class APIKeyAuth:
    """API Key Authentication middleware (foundation for future implementation)."""
    
    def __init__(self, app=None, api_keys=None, header_name="X-API-Key"):
        """Initialize the API Key authentication middleware.
        
        Args:
            app: The Flask app
            api_keys: Dictionary mapping API keys to user identifiers
            header_name: Header name for API key
        """
        self.api_keys = api_keys or {}
        self.header_name = header_name
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with a Flask app."""
        # Store self in app extensions
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['api_key_auth'] = self
    
    def check_api_key(self, api_key: str) -> Optional[str]:
        """Check if API key is valid.
        
        Args:
            api_key: API key string
            
        Returns:
            User identifier or None if invalid
        """
        return self.api_keys.get(api_key)
    
    def require_api_key(self, view_function):
        """Decorator to require API key for a view function.
        
        Args:
            view_function: Flask view function
            
        Returns:
            Decorated function
        """
        @wraps(view_function)
        def decorated(*args, **kwargs):
            api_key = request.headers.get(self.header_name)
            
            if not api_key:
                logger.warning(f"API key authentication failed: No key provided")
                raise APIError(
                    ErrorCode.PERMISSION_DENIED,
                    "API key required"
                )
                
            user_id = self.check_api_key(api_key)
            if not user_id:
                logger.warning(f"API key authentication failed: Invalid key")
                raise APIError(
                    ErrorCode.PERMISSION_DENIED,
                    "Invalid API key"
                )
            
            # Store authenticated user in g
            g.auth_user = user_id
            g.auth_api_key = api_key
            
            return view_function(*args, **kwargs)
        return decorated


# Convenience functions for route protection

def auth_required(f):
    """Decorator to require authentication using configured auth method.
    
    This decorator allows routes to be protected without knowing which
    authentication method is configured. It will use the first available
    authentication method (Basic Auth, API Key, etc).
    
    Args:
        f: Flask view function
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Find available auth methods
        app = current_app
        
        # Try Basic Auth if configured
        if 'basic_auth' in app.extensions:
            return app.extensions['basic_auth'].require_auth(f)(*args, **kwargs)
        
        # Try API Key Auth if configured
        if 'api_key_auth' in app.extensions:
            return app.extensions['api_key_auth'].require_api_key(f)(*args, **kwargs)
        
        # No auth configured, just call the function
        logger.warning("No authentication method configured, but route requires auth")
        return f(*args, **kwargs)
    
    return decorated