# src/web/services Directory Documentation

## Directory Purpose
The `src/web/services` directory contains core service modules that provide essential background functionality for the CreatureBox web application. These services handle operations such as caching, background job processing, and storage management, which require persistent state and potentially long-running operations. The services in this directory enable the application to efficiently manage resources, provide responsiveness to users, and maintain data integrity, even during complex operations that would otherwise block the main application thread.

## File Inventory
| Filename | Type | Size | Description |
|----------|------|------|-------------|
| cache.py | Python | 1.2 KB | Caching service implementation |
| job_queue.py | Python | 2.3 KB | Background job processing service |
| storage.py | Python | 1.8 KB | Photo storage management service |

## Detailed File Descriptions

### cache.py
- **Primary Purpose**: Provides a flexible caching system to improve application performance
- **Key Functions**:
  * `Cache` class: Abstract base class defining cache interface
  * `MemoryCache` class: In-memory implementation of caching
  * `RedisCache` class: Redis-backed implementation (when available)
  * `get_cache(config)`: Factory function to select appropriate cache implementation
  * `cache_decorator()`: Function decorator for easy result caching
- **Dependencies**:
  * Redis (optional)
  * Python standard library
- **Technical Notes**: 
  * Automatically falls back to memory cache if Redis is unavailable
  * Implements TTL (time-to-live) for cached items
  * Thread-safe implementation for concurrent access

### job_queue.py
- **Primary Purpose**: Manages asynchronous execution of long-running tasks
- **Key Functions**:
  * `JobQueue` class: Core job processing system
  * `Job` class: Representation of a background task
  * `enqueue(func, *args, **kwargs)`: Adds a job to the queue
  * `get_job_status(job_id)`: Retrieves current status of a job
  * `cancel_job(job_id)`: Attempts to cancel a running job
  * `cleanup_old_jobs(max_age)`: Removes completed jobs older than specified time
- **Dependencies**:
  * Threading module
  * Queue module
  * uuid module
- **Technical Notes**: 
  * Implements worker pool pattern for parallel processing
  * Provides real-time status updates for running jobs
  * Maintains persistent job history for monitoring

### storage.py
- **Primary Purpose**: Manages photo storage operations and organization
- **Key Functions**:
  * `StorageManager` class: Core storage management functionality
  * `get_storage_stats()`: Returns disk usage and capacity information
  * `backup_photos(destination)`: Creates backups of photo files
  * `cleanup_old_photos(days_to_keep)`: Manages storage by removing old images
  * `organize_photos_by_date()`: Organizes photo files into date-based directories
- **Dependencies**:
  * os module
  * shutil module
  * datetime module
  * src/web/utils/files.py
- **Technical Notes**: 
  * Implements safe file operations with error handling
  * Includes validation to prevent accidental data loss
  * Uses transactional approach for operations affecting multiple files

## Relationship Documentation
- **Related To**:
  * src/web/routes/*.py (routes that use these services)
  * src/web/app.py (application initialization)
- **Depends On**:
  * src/web/utils/*.py (utility functions)
  * src/config/ (configuration settings)
  * External services (Redis, when available)
- **Used By**:
  * API endpoints that require background processing
  * Operations that benefit from caching
  * Storage management functions

## Use Cases
1. **Performance Optimization Through Caching**:
   - **Implementation**: The cache.py module provides both in-memory and Redis-backed caching to improve response times for frequently accessed data.
   - **Example**:
     ```python
     from src.web.services.cache import get_cache, cache_decorator
     
     cache = get_cache(app.config)
     
     # Function decorator approach
     @cache_decorator(timeout=300)  # Cache for 5 minutes
     def get_system_status():
         # Complex or slow operation to get status
         return status_data
     
     # Direct cache usage
     def get_photo_metadata(photo_id):
         cache_key = f"photo:{photo_id}:metadata"
         cached = cache.get(cache_key)
         if cached:
             return cached
             
         metadata = compute_photo_metadata(photo_id)
         cache.set(cache_key, metadata, timeout=600)
         return metadata
     ```

2. **Long-Running Background Tasks**:
   - **Implementation**: The job_queue.py module enables asynchronous execution of time-consuming operations without blocking the web server.
   - **Example**:
     ```python
     from src.web.services.job_queue import JobQueue
     
     job_queue = JobQueue(worker_count=4)
     
     # API route handler
     @app.route('/api/photos/process-batch', methods=['POST'])
     def process_photo_batch():
         photos = request.json.get('photos', [])
         job = job_queue.enqueue(process_multiple_photos, photos)
         return jsonify({'job_id': job.id, 'status': job.status})
     
     # Status checking endpoint
     @app.route('/api/jobs/<job_id>', methods=['GET'])
     def check_job_status(job_id):
         job = job_queue.get_job(job_id)
         if not job:
             abort(404)
         return jsonify({
             'id': job.id,
             'status': job.status,
             'progress': job.progress,
             'result': job.result if job.status == 'completed' else None
         })
     ```

3. **Photo Storage Management**:
   - **Implementation**: The storage.py module handles organization and management of photo files.
   - **Example**:
     ```python
     from src.web.services.storage import StorageManager
     
     storage_mgr = StorageManager(base_path='/opt/creaturebox/photos')
     
     # API route for storage cleanup
     @app.route('/api/storage/cleanup', methods=['POST'])
     def cleanup_storage():
         days_to_keep = request.json.get('days_to_keep', 30)
         job = job_queue.enqueue(
             storage_mgr.cleanup_old_photos, 
             days_to_keep
         )
         return jsonify({'job_id': job.id})
         
     # API route for storage stats
     @app.route('/api/storage/stats', methods=['GET'])
     def get_storage_info():
         stats = storage_mgr.get_storage_stats()
         return jsonify(stats)
     ```

4. **External Storage Backup**:
   - **Implementation**: The storage.py module provides functionality to backup photos to external devices.
   - **Example**:
     ```python
     # API route for external backup
     @app.route('/api/storage/backup/external', methods=['POST'])
     def backup_to_external():
         device_path = request.json.get('device_path')
         if not os.path.exists(device_path):
             abort(400, "External device not found")
             
         job = job_queue.enqueue(
             storage_mgr.backup_photos,
             destination=device_path,
             incremental=True
         )
         return jsonify({'job_id': job.id})
     ```
