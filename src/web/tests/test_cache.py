import pytest
import time
from ..services.cache import cache_service, cached, CacheService, InMemoryCache


def test_cache_service_singleton():
    """Test that cache_service is a singleton."""
    new_service = CacheService()
    assert new_service is cache_service


def test_cache_basic_operations():
    """Test basic cache operations."""
    # Make sure we're using in-memory cache for tests
    if not isinstance(cache_service._cache, InMemoryCache):
        cache_service._cache = InMemoryCache()
    
    # Clear any existing cache entries
    cache_service.clear()
    
    # Test set and get
    cache_service.set('test_key', 'test_value')
    assert cache_service.get('test_key') == 'test_value'
    
    # Test delete
    assert cache_service.delete('test_key')
    assert cache_service.get('test_key') is None
    
    # Test non-existent key
    assert cache_service.get('non_existent') is None
    assert not cache_service.delete('non_existent')


def test_cache_ttl():
    """Test cache TTL (expiration)."""
    # Make sure we're using in-memory cache for tests
    if not isinstance(cache_service._cache, InMemoryCache):
        cache_service._cache = InMemoryCache()
    
    # Clear any existing cache entries
    cache_service.clear()
    
    # Set with TTL of 1 second
    cache_service.set('ttl_key', 'ttl_value', ttl=1)
    
    # Should be available immediately
    assert cache_service.get('ttl_key') == 'ttl_value'
    
    # Wait for expiration
    time.sleep(1.1)
    
    # Should be expired now
    assert cache_service.get('ttl_key') is None


def test_cached_decorator():
    """Test the @cached decorator."""
    # Make sure we're using in-memory cache for tests
    if not isinstance(cache_service._cache, InMemoryCache):
        cache_service._cache = InMemoryCache()
    
    # Clear any existing cache entries
    cache_service.clear()
    
    # Call counter to verify caching
    call_count = {'value': 0}
    
    @cached(ttl=5)
    def cached_function(x, y):
        call_count['value'] += 1
        return x + y
    
    # First call should execute the function
    result1 = cached_function(1, 2)
    assert result1 == 3
    assert call_count['value'] == 1
    
    # Second call with same args should use cache
    result2 = cached_function(1, 2)
    assert result2 == 3
    assert call_count['value'] == 1  # Should not increase
    
    # Call with different args should execute the function
    result3 = cached_function(3, 4)
    assert result3 == 7
    assert call_count['value'] == 2
    
    # Clear cache and verify function is called again
    cache_service.clear()
    result4 = cached_function(1, 2)
    assert result4 == 3
    assert call_count['value'] == 3


def test_cache_complex_types():
    """Test caching complex data types."""
    # Make sure we're using in-memory cache for tests
    if not isinstance(cache_service._cache, InMemoryCache):
        cache_service._cache = InMemoryCache()
    
    # Clear any existing cache entries
    cache_service.clear()
    
    # Test with a dictionary
    cache_service.set('dict_key', {'name': 'test', 'value': 123})
    dict_result = cache_service.get('dict_key')
    assert dict_result == {'name': 'test', 'value': 123}
    
    # Test with a list
    cache_service.set('list_key', [1, 2, 3, 'test'])
    list_result = cache_service.get('list_key')
    assert list_result == [1, 2, 3, 'test']
    
    # Test with a nested structure
    complex_data = {
        'users': [
            {'id': 1, 'name': 'Alice', 'roles': ['admin', 'user']},
            {'id': 2, 'name': 'Bob', 'roles': ['user']}
        ],
        'settings': {
            'theme': 'dark',
            'notifications': True
        }
    }
    cache_service.set('complex_key', complex_data)
    complex_result = cache_service.get('complex_key')
    assert complex_result == complex_data
