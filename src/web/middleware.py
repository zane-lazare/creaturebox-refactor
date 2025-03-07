# src/web/middleware.py
"""Middleware for the CreatureBox web application."""
from flask import request, g, current_app
import time
import logging
import re
from typing import Dict, Tuple, Optional, List, Callable, Any, Union

from .services.cache import cache_service
from .config import API_RATE_LIMIT, ENABLE_RATE_LIMITING

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiter middleware with support for per-endpoint configuration and priorities."""
    
    def __init__(self, app=None, default_limit=60, default_window=60, 
                 endpoints=None, priority_func=None):
        """Initialize the rate limiter.
        
        Args:
            app: The Flask app
            default_limit: Default maximum number of requests allowed per window
            default_window: Default time window in seconds
            endpoints: Optional dict mapping endpoint patterns to (limit, window) tuples
            priority_func: Optional function that returns priority multiplier for a request
        """
        self.default_limit = default_limit
        self.default_window = default_window
        self.endpoints = endpoints or {}
        self.priority_func = priority_func
        self.cache_prefix = "ratelimit:"
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the rate limiter with a Flask app."""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Check rate limit before processing request."""
        if not getattr(g, 'rate_limit_enabled', ENABLE_RATE_LIMITING):
            return
            
        # Get client identifier (IP address by default)
        client_id = self._get_client_identifier()
        
        # Get endpoint-specific limit or use default
        limit, window = self._get_limits_for_endpoint(request.endpoint, request.path)
        
        # Apply priority multiplier if available
        if self.priority_func:
            try:
                priority = self.priority_func(request)
                if priority > 0:
                    limit = int(limit * priority)
            except Exception as e:
                logger.warning(f"Error applying priority function: {str(e)}")
        
        # Generate cache key
        cache_key = self._generate_cache_key(client_id, request.endpoint)
        
        # Get current time
        current_time = time.time()
        
        # Get existing requests from cache
        requests_data = cache_service.get(cache_key)
        
        if requests_data is None:
            requests_data = {"requests": [], "limit": limit, "window": window}
        
        # Clean up old requests
        requests_data["requests"] = [t for t in requests_data["requests"] 
                                   if current_time - t < window]
        
        # Update limit and window in case configuration changed
        requests_data["limit"] = limit
        requests_data["window"] = window
        
        # Store rate limit data in g for header generation
        g.rate_limit_data = {
            "limit": limit,
            "remaining": max(0, limit - len(requests_data["requests"])),
            "reset": int(current_time + window - (current_time % window)),
            "window": window
        }
        
        # Check if limit exceeded
        if len(requests_data["requests"]) >= limit:
            logger.warning(f"Rate limit exceeded for {client_id} on {request.endpoint}")
            
            # Set retry-after header value
            if requests_data["requests"]:
                oldest_request = min(requests_data["requests"])
                retry_after = int(oldest_request + window - current_time)
                if retry_after < 0:
                    retry_after = 1
                g.rate_limit_data["retry_after"] = retry_after
            else:
                g.rate_limit_data["retry_after"] = window
            
            # Create rate limit error response
            return {
                'status': 'error',
                'error': {
                    'code': 429,
                    'message': 'Rate limit exceeded',
                    'details': {'retry_after': g.rate_limit_data.get("retry_after", window)}
                }
            }, 429
        
        # Add current request
        requests_data["requests"].append(current_time)
        
        # Save to cache with expiration
        cache_service.set(cache_key, requests_data, ttl=window * 2)
    
    def after_request(self, response):
        """Add rate limit headers to response."""
        if hasattr(g, 'rate_limit_data'):
            # Add standard rate limit headers
            rate_limit_data = g.rate_limit_data
            response.headers['X-RateLimit-Limit'] = str(rate_limit_data["limit"])
            response.headers['X-RateLimit-Remaining'] = str(rate_limit_data["remaining"])
            response.headers['X-RateLimit-Reset'] = str(rate_limit_data["reset"])
            
            # Add retry-after header if limit exceeded
            if rate_limit_data.get("retry_after"):
                response.headers['Retry-After'] = str(rate_limit_data["retry_after"])
        
        return response
    
    def _get_client_identifier(self) -> str:
        """Get client identifier for rate limiting.
        
        Returns:
            Client identifier string
        """
        # Start with IP address
        client_id = request.remote_addr
        
        # Check for API key if present
        api_key = request.headers.get('X-API-Key')
        if api_key:
            client_id = f"apikey:{api_key}"
        
        # Check for authorization header (Basic auth)
        auth = request.authorization
        if auth:
            client_id = f"user:{auth.username}"
        
        return client_id
    
    def _get_limits_for_endpoint(self, endpoint: str, path: str) -> Tuple[int, int]:
        """Get rate limit and window for the current endpoint.
        
        Args:
            endpoint: Flask endpoint name
            path: Request path
            
        Returns:
            Tuple of (limit, window)
        """
        # Check for exact endpoint match
        if endpoint in self.endpoints:
            return self.endpoints[endpoint]
        
        # Check for path pattern match
        for pattern, limits in self.endpoints.items():
            if pattern.startswith('/') and re.match(pattern, path):
                return limits
        
        # Return default limits
        return self.default_limit, self.default_window
    
    def _generate_cache_key(self, client_id: str, endpoint: str) -> str:
        """Generate cache key for rate limit data.
        
        Args:
            client_id: Client identifier
            endpoint: Flask endpoint name
            
        Returns:
            Cache key string
        """
        return f"{self.cache_prefix}{client_id}:{endpoint}"


class RequestLogger:
    """Middleware to log API requests."""
    
    def __init__(self, app=None):
        """Initialize the request logger.
        
        Args:
            app: The Flask app
        """
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the request logger with a Flask app."""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Log request details before processing."""
        g.start_time = time.time()
    
    def after_request(self, response):
        """Log response details after processing."""
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            
            # Only log 4xx and 5xx responses at WARNING level
            if response.status_code >= 400:
                logger.warning(
                    f"{request.remote_addr} - {request.method} {request.path} "
                    f"- {response.status_code} - {duration:.4f}s"
                )
            else:
                logger.info(
                    f"{request.remote_addr} - {request.method} {request.path} "
                    f"- {response.status_code} - {duration:.4f}s"
                )
        return response