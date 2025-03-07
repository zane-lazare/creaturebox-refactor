# Web Services Module Documentation

{% include navigation.html %}

## Overview

The Web Services Module provides the core business logic components that handle background processing, caching, storage management, and job queue functionality for the CreatureBox web application.

<details id="purpose">
<summary><h2>Purpose</h2></summary>
<div markdown="1">

The `src/web/services` directory contains service classes that implement the core business logic of the CreatureBox web application. This module provides:

- Background processing capabilities
- Caching mechanisms for performance optimization
- Storage management for photos and files
- Job queue for delayed and asynchronous tasks
- API interaction layers with system components
- Data access abstractions

These services act as the middle layer between the web routes (controllers) and the system resources, providing reusable, modular functionality that encapsulates complex operations.

</div>
</details>

<details id="file-inventory">
<summary><h2>File Inventory</h2></summary>
<div markdown="1">

| Filename | Type | Size | Purpose |
|----------|------|------|---------|
| __init__.py | Python | 0.2 KB | Package initialization |
| cache.py | Python | 1.6 KB | Data caching service |
| job_queue.py | Python | 2.2 KB | Background task scheduling |
| storage.py | Python | 2.8 KB | File storage management |

</div>
</details>

<details id="file-descriptions">
<summary><h2>File Descriptions</h2></summary>
<div markdown="1">

### __init__.py
- **Primary Purpose**: Package initialization
- **Key Functions**:
  * `register_services(app)`: Initializes all services with the Flask app
- **Dependencies**:
  * Flask application context
- **Technical Notes**: Ensures services are properly initialized in the correct order

### cache.py
- **Primary Purpose**: Data caching and performance optimization
- **Key Functions**:
  * `CacheService`: Main caching service class
  * `cache.get(key)`: Retrieve cached item
  * `cache.set(key, value, ttl)`: Store item in cache
  * `cache.delete(key)`: Remove item from cache
  * `cache.clear()`: Clear entire cache
  * `cache.get_or_set(key, callable, ttl)`: Get cached value or compute and cache
  * `cache_decorator(ttl)`: Decorator for caching function results
- **Dependencies**:
  * Redis or in-memory cache implementation
  * Serialization utilities
- **Technical Notes**: Configurable with different backend providers (Redis, in-memory, filesystem)

### job_queue.py
- **Primary Purpose**: Background and scheduled task processing
- **Key Functions**:
  * `JobQueue`: Main queue management class
  * `queue.enqueue(func, *args, **kwargs)`: Add task to queue
  * `queue.schedule(func, delay, *args, **kwargs)`: Schedule delayed task
  * `queue.recurring(func, interval, *args, **kwargs)`: Set up recurring task
  * `queue.cancel(job_id)`: Cancel pending job
  * `queue.status(job_id)`: Check job status
  * `queue.results(job_id)`: Get job results
  * `Worker`: Background worker implementation
- **Dependencies**:
  * Threading or multiprocessing
  * Redis for persistent job storage
- **Technical Notes**: Supports priority levels and job dependencies

### storage.py
- **Primary Purpose**: File and image storage management
- **Key Functions**:
  * `StorageService`: Main storage management class
  * `storage.save_file(file_obj, path)`: Save uploaded file
  * `storage.get_file(path)`: Retrieve file
  * `storage.delete_file(path)`: Remove file
  * `storage.list_files(directory)`: List files in directory
  * `storage.get_url(path)`: Get URL for file access
  * `storage.save_image(image, path, format)`: Save image with processing
  * `storage.create_thumbnail(image_path, size)`: Generate thumbnail
  * `storage.get_disk_usage()`: Check storage utilization
- **Dependencies**:
  * File system access
  * PIL for image processing
  * File type detection
- **Technical Notes**: Supports both local and remote storage backends

</div>
</details>

<details id="relationships">
<summary><h2>Relationships</h2></summary>
<div markdown="1">

- **Related To**:
  * [Web Routes](./src-web-routes.md): Routes use services for business logic
  * [Web Utilities](./src-web-utils.md): Services depend on utility functions
  * [Web Middleware](./src-web-middleware.md): Services use middleware context
- **Depends On**:
  * [Configuration Module](./src-config.md): Service configuration
  * [Software Module](./src-software.md): For camera and system control
  * Third-party libraries (Redis, PIL)
  * File system and hardware access
- **Used By**:
  * Route handlers in web application
  * Background processing tasks
  * Scheduled operations

</div>
</details>

<details id="use-cases">
<summary><h2>Use Cases</h2></summary>
<div markdown="1">

1. **Image Processing Pipeline**:
   - **Description**: Processing and storing captured images.
   - **Example**: 
     ```python
     # In a route handler
     from src.web.services.storage import storage_service
     from src.web.services.job_queue import job_queue
     
     @camera_bp.route('/api/camera/capture', methods=['POST'])
     def capture_image():
         # Trigger camera capture
         raw_image = camera_utility.capture()
         
         # Save original image
         original_path = storage_service.save_image(
             raw_image, 
             f"captures/{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg",
             format='jpeg',
             quality=95
         )
         
         # Queue background processing
         job_queue.enqueue(
             process_image,
             original_path,
             apply_filters=True,
             generate_thumbnails=True
         )
         
         return jsonify({"status": "success", "path": original_path})
     
     def process_image(image_path, apply_filters=False, generate_thumbnails=False):
         """Background task to process captured image"""
         if apply_filters:
             # Apply image enhancement filters
             storage_service.apply_filters(image_path)
             
         if generate_thumbnails:
             # Create multiple thumbnail sizes
             storage_service.create_thumbnail(image_path, (100, 100))
             storage_service.create_thumbnail(image_path, (400, 400))
     ```

2. **Caching for Performance**:
   - **Description**: Using caching to improve application performance.
   - **Example**: 
     ```python
     # In a service or route handler
     from src.web.services.cache import cache_service
     
     @gallery_bp.route('/api/gallery/recent', methods=['GET'])
     def get_recent_photos():
         # Cache key based on request parameters
         page = request.args.get('page', 1, type=int)
         cache_key = f"recent_photos:page:{page}"
         
         # Try to get from cache first
         cached_result = cache_service.get(cache_key)
         if cached_result:
             return jsonify(cached_result)
             
         # Not in cache, fetch from storage
         photos = storage_service.list_files(
             "captures", 
             sort_by="date", 
             order="desc", 
             limit=20, 
             offset=(page-1)*20
         )
         
         # Process photos
         result = {"photos": process_photo_list(photos), "page": page}
         
         # Cache for 5 minutes
         cache_service.set(cache_key, result, ttl=300)
         
         return jsonify(result)
     ```

3. **Background Job Processing**:
   - **Description**: Scheduling and monitoring background tasks.
   - **Example**: 
     ```python
     # In a route handler or service
     from src.web.services.job_queue import job_queue
     
     @system_bp.route('/api/system/backup', methods=['POST'])
     def trigger_backup():
         # Get backup parameters
         params = request.get_json()
         destination = params.get('destination', 'default')
         include_photos = params.get('include_photos', True)
         
         # Schedule backup job to run in the background
         job_id = job_queue.enqueue(
             perform_system_backup,
             destination,
             include_photos
         )
         
         return jsonify({"status": "scheduled", "job_id": job_id})
         
     @system_bp.route('/api/system/backup/status/<job_id>', methods=['GET'])
     def backup_status(job_id):
         # Check job status
         status = job_queue.status(job_id)
         
         if status == 'complete':
             results = job_queue.results(job_id)
             return jsonify({
                 "status": "complete",
                 "backup_size": results.get('size'),
                 "backup_location": results.get('path'),
                 "duration": results.get('duration')
             })
         elif status == 'failed':
             error = job_queue.results(job_id).get('error')
             return jsonify({"status": "failed", "error": error}), 500
         else:
             return jsonify({"status": status})
     ```

4. **Storage Management**:
   - **Description**: Managing disk storage and performing cleanup.
   - **Example**: 
     ```python
     # In a scheduled task
     from src.web.services.storage import storage_service
     from src.web.services.job_queue import job_queue
     
     def setup_storage_maintenance():
         # Schedule daily storage maintenance
         job_queue.recurring(
             maintain_storage,
             interval=24*60*60,  # Daily
             run_at="02:00"      # At 2 AM
         )
         
     def maintain_storage():
         """Perform storage maintenance tasks"""
         # Check storage usage
         usage = storage_service.get_disk_usage()
         
         # If storage is over 80% full, cleanup old files
         if usage.percent > 80:
             # Find oldest non-favorite images
             old_files = storage_service.list_files(
                 "captures",
                 sort_by="date",
                 order="asc",
                 filter={"favorite": False},
                 limit=100
             )
             
             # Delete files until under threshold or no more files
             deleted = 0
             for file in old_files:
                 if storage_service.get_disk_usage().percent < 70:
                     break
                     
                 storage_service.delete_file(file.path)
                 deleted += 1
                 
             return {"cleaned_up": True, "deleted_count": deleted}
         
         return {"cleaned_up": False, "usage_percent": usage.percent}
     ```

</div>
</details>
