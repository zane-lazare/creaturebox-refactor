"""
Caching service for the CreatureBox web interface.
Supports both Redis-based and in-memory caching.
"""
import time
import threading
import logging
import functools
from typing import Any, Dict, Optional, Callable, Union, Tuple, List

from ..config import CACHE_TIMEOUT

logger = logging.getLogger(__name__)

# Try to import Redis, but don't fail if not available
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class InMemoryCache:
    """Simple in-memory cache with TTL."""
    
    def __init__(self):
        """Initialize the cache."""
        self._cache = {}
        self._lock = threading.RLock()
        self._cleanup_thread = None
        self._running = False
        
        # Start background cleanup thread
        self._start_cleanup_thread()
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        with self._lock:
            item = self._cache.get(key)
            if item is None:
                return None
            
            value, expiry = item
            if expiry and time.time() > expiry:
                # Expired item
                del self._cache[key]
                return None
            
            return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None for no expiration)
            
        Returns:
            True if successful
        """
        with self._lock:
            if ttl is not None:
                expiry = time.time() + ttl
            else:
                expiry = None
            
            self._cache[key] = (value, expiry)
            return True
    
    def delete(self, key: str) -> bool:
        """Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> bool:
        """Clear all cache entries.
        
        Returns:
            True if successful
        """
        with self._lock:
            self._cache.clear()
            return True
    
    def _cleanup_expired(self):
        """Remove expired items from the cache."""
        now = time.time()
        with self._lock:
            keys_to_delete = []
            for key, (_, expiry) in self._cache.items():
                if expiry and now > expiry:
                    keys_to_delete.append(key)
            
            for key in keys_to_delete:
                del self._cache[key]
            
            return len(keys_to_delete)
    
    def _cleanup_thread_func(self):
        """Background thread for cleaning up expired items."""
        while self._running:
            try:
                # Sleep first to avoid immediate cleanup
                time.sleep(60)
                
                # Cleanup expired items
                removed = self._cleanup_expired()
                if removed > 0:
                    logger.debug(f"Removed {removed} expired cache items")
            except Exception as e:
                logger.error(f"Error in cache cleanup thread: {str(e)}")
    
    def _start_cleanup_thread(self):
        """Start the background cleanup thread."""
        if self._cleanup_thread is not None:
            return
        
        self._running = True
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_thread_func,
            name="Cache-Cleanup",
            daemon=True
        )
        self._cleanup_thread.start()
    
    def shutdown(self):
        """Shutdown the cache."""
        self._running = False
        if self._cleanup_thread:
            self._cleanup_thread.join(timeout=1.0)


class RedisCache:
    """Redis-based cache."""
    
    def __init__(self, host='localhost', port=6379, db=0, prefix='creaturebox:'):
        """Initialize the Redis cache.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database
            prefix: Key prefix
        """
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._prefix = prefix
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        import pickle
        
        full_key = f"{self._prefix}{key}"
        value = self._redis.get(full_key)
        
        if value is None:
            return None
        
        try:
            return pickle.loads(value)
        except Exception as e:
            logger.error(f"Error deserializing cached value: {str(e)}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None for no expiration)
            
        Returns:
            True if successful
        """
        import pickle
        
        full_key = f"{self._prefix}{key}"
        
        try:
            serialized = pickle.dumps(value)
            if ttl is not None:
                self._redis.setex(full_key, ttl, serialized)
            else:
                self._redis.set(full_key, serialized)
            return True
        except Exception as e:
            logger.error(f"Error serializing or setting cached value: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        full_key = f"{self._prefix}{key}"
        result = self._redis.delete(full_key)
        return result > 0
    
    def clear(self) -> bool:
        """Clear all cache entries with the specified prefix.
        
        Returns:
            True if successful
        """
        try:
            # Find all keys with prefix
            pattern = f"{self._prefix}*"
            keys = self._redis.keys(pattern)
            
            # Delete all keys
            if keys:
                self._redis.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    def shutdown(self):
        """Shutdown the Redis connection."""
        try:
            self._redis.close()
        except Exception as e:
            logger.error(f"Error closing Redis connection: {str(e)}")


class CacheService:
    """Cache service that provides either Redis or in-memory caching."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(CacheService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the cache service."""
        # Only initialize once for singleton
        if self._initialized:
            return
        
        self._cache = None
        self._initialize_cache()
        self._initialized = True
    
    def _initialize_cache(self):
        """Initialize the appropriate cache backend."""
        # Try to use Redis if available
        if REDIS_AVAILABLE:
            try:
                self._cache = RedisCache()
                # Test connection
                self._cache.set('__test__', 'test')
                test_value = self._cache.get('__test__')
                self._cache.delete('__test__')
                
                if test_value == 'test':
                    logger.info("Using Redis cache backend")
                    return
                else:
                    logger.warning("Redis connection test failed, falling back to in-memory cache")
            except Exception as e:
                logger.warning(f"Failed to initialize Redis cache: {str(e)}, falling back to in-memory cache")
        
        # Fallback to in-memory cache
        self._cache = InMemoryCache()
        logger.info("Using in-memory cache backend")
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        return self._cache.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = CACHE_TIMEOUT) -> bool:
        """Set a value in the cache."""
        return self._cache.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """Delete a value from the cache."""
        return self._cache.delete(key)
    
    def clear(self) -> bool:
        """Clear all cache entries."""
        return self._cache.clear()
    
    def shutdown(self):
        """Shutdown the cache."""
        if self._cache:
            self._cache.shutdown()


# Create a singleton instance
cache_service = CacheService()


def cached(ttl: Optional[int] = CACHE_TIMEOUT, key_prefix: str = ""):
    """Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds (None for no expiration)
        key_prefix: Optional prefix for cache keys
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = _generate_cache_key(key_prefix, func, args, kwargs)
            
            # Try to get from cache
            cached_value = cache_service.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call the function
            result = func(*args, **kwargs)
            
            # Cache the result
            cache_service.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator


def _generate_cache_key(prefix: str, func: Callable, args: tuple, kwargs: dict) -> str:
    """Generate a cache key for a function call.
    
    Args:
        prefix: Key prefix
        func: Function being called
        args: Positional arguments
        kwargs: Keyword arguments
        
    Returns:
        Cache key
    """
    import hashlib
    import json
    
    # Start with prefix and function name
    key_parts = [prefix, func.__module__, func.__name__]
    
    # Add args and kwargs
    try:
        # Convert args to strings
        for arg in args:
            key_parts.append(str(arg))
        
        # Convert kwargs to strings (sorted by key)
        for k in sorted(kwargs.keys()):
            key_parts.append(f"{k}={kwargs[k]}")
        
        # Join parts
        key = ":".join(key_parts)
        
        # If the key is too long, hash it
        if len(key) > 250:
            key = hashlib.md5(key.encode('utf-8')).hexdigest()
        
        return key
    except Exception as e:
        # Fallback for non-serializable objects
        logger.warning(f"Error generating cache key: {str(e)}")
        return f"{prefix}:{func.__module__}.{func.__name__}:{hash(str(args))}{hash(str(kwargs))}"
