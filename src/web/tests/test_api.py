import pytest
import json

def test_health_endpoint(client):
    """Test the API health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'data' in data
    assert data['data']['status'] == 'healthy'


def test_system_status_endpoint(client):
    """Test the system status endpoint."""
    response = client.get('/api/system/status')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'system' in data
    assert 'power' in data
    assert 'storage' in data
    assert 'schedule' in data
    
    # Check system info fields
    assert 'cpuTemp' in data['system']
    assert 'cpuUsage' in data['system']
    assert 'memoryUsage' in data['system']
    assert 'uptime' in data['system']
    assert 'deviceName' in data['system']
    assert 'status' in data['system']


def test_error_handling(client):
    """Test error handling for non-existent endpoints."""
    response = client.get('/api/non_existent_endpoint')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'error' in data
    assert data['error']['code'] == 1002  # RESOURCE_NOT_FOUND
