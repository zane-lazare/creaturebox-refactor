# src/web/tests/test_middleware.py
import pytest
import time
import json
from unittest.mock import patch, MagicMock
from flask import Flask, Blueprint, jsonify, request

from ..middleware import RateLimiter, RequestLogger
from ..services.cache import cache_service

@pytest.fixture
def rate_limit_app():
    """Create a Flask app with rate limiting enabled."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    # Create a blueprint with test routes
    bp = Blueprint('test', __name__)
    
    @bp.route('/standard')
    def standard_endpoint():
        return jsonify({"message": "standard endpoint"})
    
    @bp.route('/high-load')
    def high_load_endpoint():
        return jsonify({"message": "high load endpoint"})
    
    @bp.route('/admin/action')
    def admin_endpoint():
        return jsonify({"message": "admin endpoint"})
    
    app.register_blueprint(bp)
    
    # Configure rate limiter with per-endpoint limits
    endpoints = {
        'test.standard_endpoint': (20, 60),  # 20 requests per minute
        'test.high_load_endpoint': (5, 60),  # 5 requests per minute
        '/admin/.*': (3, 60)  # 3 requests per minute for admin routes
    }
    
    # Define priority function
    def priority_func(request):
        # Give higher priority (2x) to local requests
        if request.remote_addr == '127.0.0.1':
            return 2.0
        return 1.0
    
    # Initialize rate limiter with the app
    limiter = RateLimiter(
        app=app,
        default_limit=10,
        default_window=60,
        endpoints=endpoints,
        priority_func=priority_func
    )
    
    # Also add request logger
    logger = RequestLogger(app=app)
    
    return app

@pytest.fixture
def mock_cache():
    """Mock cache service for testing."""
    # Save original get and set methods
    original_get = cache_service.get
    original_set = cache_service.set
    
    # Use an in-memory dict for testing
    test_cache = {}
    
    def mock_get(key):
        return test_cache.get(key)
    
    def mock_set(key, value, ttl=None):
        test_cache[key] = value
        return True
    
    # Replace methods
    cache_service.get = mock_get
    cache_service.set = mock_set
    
    yield
    
    # Restore original methods
    cache_service.get = original_get
    cache_service.set = original_set

def test_rate_limiter_basic(rate_limit_app, mock_cache):
    """Test basic rate limiting functionality."""
    client = rate_limit_app.test_client()
    
    # Make requests up to the limit
    for i in range(10):
        response = client.get('/standard')
        assert response.status_code == 200
        
        # Check response headers
        assert 'X-RateLimit-Limit' in response.headers
        assert 'X-RateLimit-Remaining' in response.headers
        assert 'X-RateLimit-Reset' in response.headers
        
        # Verify remaining count decreases
        remaining = int(response.headers['X-RateLimit-Remaining'])
        assert remaining == 10 - i - 1
    
    # Next request should be rate limited
    response = client.get('/standard')
    assert response.status_code == 429
    
    # Check error response
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert data['error']['code'] == 429
    assert 'retry_after' in data['error']['details']
    
    # Check retry-after header
    assert 'Retry-After' in response.headers

def test_rate_limiter_per_endpoint(rate_limit_app, mock_cache):
    """Test per-endpoint rate limiting configuration."""
    client = rate_limit_app.test_client()
    
    # Test standard endpoint (limit: 20)
    for i in range(15):
        response = client.get('/standard')
        assert response.status_code == 200
    
    # Test high-load endpoint (limit: 5)
    for i in range(5):
        response = client.get('/high-load')
        assert response.status_code == 200
    
    # Next request should be rate limited
    response = client.get('/high-load')
    assert response.status_code == 429
    
    # Admin endpoint (limit: 3)
    for i in range(3):
        response = client.get('/admin/action')
        assert response.status_code == 200
    
    # Next request should be rate limited
    response = client.get('/admin/action')
    assert response.status_code == 429

def test_rate_limiter_priority(rate_limit_app, mock_cache):
    """Test priority mechanism for rate limiting."""
    client = rate_limit_app.test_client()
    
    # Test with default remote_addr (localhost, 2x priority)
    # Should allow 20 requests instead of 10
    for i in range(20):
        response = client.get('/standard')
        assert response.status_code == 200
    
    # Next request should be rate limited
    response = client.get('/standard')
    assert response.status_code == 429

def test_rate_limiter_client_identification(rate_limit_app, mock_cache):
    """Test client identification methods."""
    client = rate_limit_app.test_client()
    
    # Test with API key
    for i in range(5):
        response = client.get('/standard', headers={'X-API-Key': 'test-key'})
        assert response.status_code == 200
    
    # Test with different API key (should have separate limit)
    for i in range(5):
        response = client.get('/standard', headers={'X-API-Key': 'different-key'})
        assert response.status_code == 200
    
    # Test with Basic auth
    for i in range(5):
        response = client.get('/standard', 
                             headers={'Authorization': 'Basic dXNlcjpwYXNz'})  # user:pass in base64
        assert response.status_code == 200

def test_rate_limiter_cache_integration(rate_limit_app):
    """Test rate limiter integration with cache service."""
    client = rate_limit_app.test_client()
    
    # Mock cache_service get and set
    with patch('src.web.services.cache.cache_service.get') as mock_get, \
         patch('src.web.services.cache.cache_service.set') as mock_set:
        
        # Configure mock to simulate cache hit/miss
        mock_get.return_value = {"requests": [time.time() - 10], "limit": 10, "window": 60}
        
        # Make a request
        response = client.get('/standard')
        
        # Verify cache was used
        assert mock_get.called
        assert mock_set.called
        
        # Check cache key format
        cache_key = mock_get.call_args[0][0]
        assert cache_key.startswith('ratelimit:')

def test_request_logger(rate_limit_app, caplog):
    """Test request logger middleware."""
    client = rate_limit_app.test_client()
    
    # Make a successful request
    response = client.get('/standard')
    assert response.status_code == 200
    
    # Check that request was logged at INFO level
    assert any("127.0.0.1 - GET /standard - 200 -" in record.message 
              for record in caplog.records if record.levelname == 'INFO')
    
    # Make a request that will return a 404
    response = client.get('/non-existent')
    assert response.status_code == 404
    
    # Check that 4xx response was logged at WARNING level
    assert any("127.0.0.1 - GET /non-existent - 404 -" in record.message 
              for record in caplog.records if record.levelname == 'WARNING')