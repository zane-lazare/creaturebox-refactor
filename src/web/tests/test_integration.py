# src/web/tests/test_integration.py
"""Integration tests for the CreatureBox web interface.

These tests verify the interactions between different components of the system,
such as the job queue, cache service, and storage management.
"""
import pytest
import json
import time
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from flask import Flask, g

from ..app import create_app
from ..services.job_queue import job_queue, JobStatus
from ..services.cache import cache_service
from ..services.storage import storage_manager
from ..middleware import RateLimiter
from ..middleware.auth import BasicAuth

@pytest.fixture
def integration_app():
    """Create a Flask app for integration testing with all components enabled."""
    # Create a temporary directory for test files
    test_dir = tempfile.mkdtemp()
    
    # Save current environment
    old_env = os.environ.copy()
    
    # Setup test environment
    os.environ['CREATUREBOX_HOME'] = test_dir
    os.environ['CREATUREBOX_PHOTOS_DIR'] = os.path.join(test_dir, 'photos')
    os.environ['CREATUREBOX_LOG_DIR'] = os.path.join(test_dir, 'logs')
    
    # Create necessary directories
    os.makedirs(os.path.join(test_dir, 'photos'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'photos_backedup'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'logs'), exist_ok=True)
    
    # Create test photos
    sample_photo_dir = os.path.join(test_dir, 'photos', '2025-01-01')
    os.makedirs(sample_photo_dir, exist_ok=True)
    with open(os.path.join(sample_photo_dir, 'test_photo.jpg'), 'w') as f:
        f.write('test photo data')
    
    # Create test settings files
    with open(os.path.join(test_dir, 'camera_settings.csv'), 'w') as f:
        f.write("SETTING,VALUE,DETAILS\n")
        f.write("ImageFileType,0,jpeg\n")
        f.write("ExposureTime,500,microseconds\n")
    
    with open(os.path.join(test_dir, 'schedule_settings.csv'), 'w') as f:
        f.write("SETTING,VALUE,DETAILS\n")
        f.write("hour,8;9;10,morning hours\n")
        f.write("minute,0,on the hour\n")
        f.write("weekday,1;2;3;4;5,weekdays\n")
    
    with open(os.path.join(test_dir, 'controls.txt'), 'w') as f:
        f.write("name=TestMothBox\n")
        f.write("shutdown_enabled=False\n")
        f.write("OnlyFlash=False\n")
        f.write("LastCalibration=1234567890\n")
    
    # Create the app
    app = create_app()
    app.config['TESTING'] = True
    
    # Configure authentication for testing
    users = {"admin": "password", "user": "userpass"}
    BasicAuth(app=app, users=users)
    
    # Configure rate limiter for testing
    endpoints = {
        'system.system_status': (100, 60),  # 100 requests per minute for status
        'system.reboot_system': (5, 60),    # 5 requests per minute for reboot
        'camera.capture_photo': (10, 60)    # 10 requests per minute for capture
    }
    RateLimiter(app=app, default_limit=50, default_window=60, endpoints=endpoints)
    
    # Start services
    with app.app_context():
        # Make sure job queue is started
        job_queue.start(num_workers=2)
    
    # Return the app for testing
    yield app
    
    # Clean up
    with app.app_context():
        # Stop job queue
        job_queue.stop()
    
    # Remove test directory
    shutil.rmtree(test_dir)
    
    # Restore environment
    os.environ.clear()
    os.environ.update(old_env)

@pytest.fixture
def client(integration_app):
    """A test client for the app."""
    return integration_app.test_client()

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['status'] == 'healthy'

def test_rate_limiting_integration(client):
    """Test rate limiting integration with the API."""
    # Make multiple requests to test rate limiting
    for i in range(6):  # System reboot endpoint has limit of 5
        response = client.post('/api/system/reboot')
        
        # First 5 should succeed (but not actually reboot in test)
        if i < 5:
            assert response.status_code in (200, 403)  # 403 if auth required
            
            # Verify rate limit headers
            assert 'X-RateLimit-Limit' in response.headers
            assert 'X-RateLimit-Remaining' in response.headers
            assert 'X-RateLimit-Reset' in response.headers
            
            # Verify remaining count decreases
            remaining = int(response.headers['X-RateLimit-Remaining'])
            assert remaining == 5 - i - 1
        else:
            # 6th request should be rate limited
            assert response.status_code == 429
            
            # Verify error response
            data = json.loads(response.data)
            assert data['status'] == 'error'
            assert data['error']['code'] == 429
            
            # Verify retry-after header
            assert 'Retry-After' in response.headers

def test_auth_integration(client):
    """Test authentication integration with the API."""
    # First try without auth
    response = client.get('/api/system/status')
    
    if response.status_code == 401:
        # If auth is required, verify WWW-Authenticate header
        assert 'WWW-Authenticate' in response.headers
        assert 'Basic' in response.headers['WWW-Authenticate']
        
        # Try with valid auth
        auth_header = f"Basic {base64.b64encode(b'admin:password').decode('utf-8')}"
        response = client.get('/api/system/status', headers={'Authorization': auth_header})
        assert response.status_code == 200

def test_job_queue_integration(client, integration_app):
    """Test job queue integration with the API."""
    # Submit a job through the API
    response = client.post('/api/storage/backup')
    assert response.status_code == 200
    
    # Get job ID from response
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'job_id' in data['data']
    
    job_id = data['data']['job_id']
    
    # Check job status
    with integration_app.app_context():
        # Wait for job to complete (with timeout)
        max_wait = 10  # seconds
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            job = job_queue.get_job(job_id)
            if job['status'] in (JobStatus.COMPLETED.value, JobStatus.FAILED.value):
                break
            time.sleep(0.1)
        
        # Verify job completed
        job = job_queue.get_job(job_id)
        assert job['status'] in (JobStatus.COMPLETED.value, JobStatus.FAILED.value)
    
    # Verify job status through API
    response = client.get(f'/api/jobs/{job_id}')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] in (JobStatus.COMPLETED.value, JobStatus.FAILED.value)

def test_cache_integration(client, integration_app):
    """Test cache service integration with the API."""
    # Make a request that should be cached
    response1 = client.get('/api/system/status')
    assert response1.status_code == 200
    
    # Mock cache_service.get to verify it's called on second request
    original_get = cache_service.get
    
    try:
        with patch('src.web.services.cache.cache_service.get') as mock_get:
            # Configure mock to return cached data
            mock_get.side_effect = original_get
            
            # Make second request
            response2 = client.get('/api/system/status')
            assert response2.status_code == 200
            
            # Verify cache was checked
            assert mock_get.called
    finally:
        # Restore original method
        cache_service.get = original_get

def test_storage_integration(client, integration_app):
    """Test storage management integration with the API."""
    # Get storage stats
    response = client.get('/api/storage/stats')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'photos' in data
    assert 'count' in data['photos']
    assert data['photos']['count'] >= 1  # Should have our test photo
    
    # Start a backup job
    response = client.post('/api/storage/backup')
    assert response.status_code == 200
    
    # Verify backup created the expected files
    with integration_app.app_context():
        # Allow time for job to complete
        time.sleep(2)
        
        backup_dir = os.path.join(
            os.environ.get('CREATUREBOX_HOME'), 
            'photos_backedup', 
            '2025-01-01'
        )
        
        # Check that backup directory exists and contains the test photo
        assert os.path.exists(backup_dir)
        assert os.path.exists(os.path.join(backup_dir, 'test_photo.jpg'))

def test_error_handling_integration(client):
    """Test error handling integration across components."""
    # Test 404 error
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert data['error']['code'] == 1002  # RESOURCE_NOT_FOUND
    
    # Test invalid JSON
    response = client.post('/api/storage/clean', 
                          data='invalid json',
                          content_type='application/json')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['status'] == 'error'
    
    # Test missing resource
    response = client.get('/api/gallery/photos/view/2099-01-01/nonexistent.jpg')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert data['error']['code'] == 2000  # FILE_NOT_FOUND
