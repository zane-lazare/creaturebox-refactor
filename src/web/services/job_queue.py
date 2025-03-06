"""
Background job queue for processing photos and other long-running tasks.
"""
import os
import time
import uuid
import queue
import threading
import logging
import traceback
from enum import Enum
from functools import wraps
from typing import Dict, List, Callable, Any, Optional, Union, Tuple

from ..config import PHOTO_PROCESSING_THREADS

logger = logging.getLogger(__name__)

# Job status enum
class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Job:
    """Represents a background job."""
    
    def __init__(self, func: Callable, args: List = None, kwargs: Dict = None, 
                 name: str = None, timeout: int = 300):
        """Initialize a job.
        
        Args:
            func: The function to run
            args: Positional arguments for the function
            kwargs: Keyword arguments for the function
            name: Human-readable job name
            timeout: Maximum time to run in seconds
        """
        self.id = str(uuid.uuid4())
        self.func = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.name = name or func.__name__
        self.timeout = timeout
        
        self.status = JobStatus.PENDING
        self.result = None
        self.error = None
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None
    
    def run(self):
        """Run the job."""
        self.started_at = time.time()
        self.status = JobStatus.RUNNING
        
        try:
            self.result = self.func(*self.args, **self.kwargs)
            self.status = JobStatus.COMPLETED
        except Exception as e:
            self.error = {
                "type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc()
            }
            self.status = JobStatus.FAILED
            logger.error(f"Job {self.id} ({self.name}) failed: {str(e)}")
        finally:
            self.completed_at = time.time()
    
    def to_dict(self):
        """Convert job to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration": (self.completed_at - self.started_at) if self.completed_at else None,
            "error": self.error
        }


class JobQueue:
    """Background job queue for processing tasks."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(JobQueue, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the job queue."""
        # Only initialize once for singleton
        if self._initialized:
            return
        
        self._queue = queue.Queue()
        self._jobs = {}  # Store jobs by ID
        self._workers = []
        self._lock = threading.RLock()
        self._running = False
        self._initialized = True
    
    def start(self, num_workers: int = PHOTO_PROCESSING_THREADS):
        """Start the worker threads."""
        with self._lock:
            if self._running:
                return
            
            self._running = True
            
            # Create worker threads
            for i in range(num_workers):
                worker = threading.Thread(
                    target=self._worker_thread,
                    name=f"JobQueue-Worker-{i}",
                    daemon=True
                )
                worker.start()
                self._workers.append(worker)
            
            logger.info(f"Started job queue with {num_workers} workers")
    
    def stop(self, wait: bool = True):
        """Stop the worker threads.
        
        Args:
            wait: Whether to wait for all jobs to finish
        """
        with self._lock:
            if not self._running:
                return
            
            self._running = False
            
            # Add sentinel values to stop workers
            for _ in range(len(self._workers)):
                self._queue.put(None)
            
            if wait:
                # Wait for all workers to finish
                for worker in self._workers:
                    worker.join()
            
            self._workers = []
            logger.info("Stopped job queue")
    
    def add_job(self, func: Callable, args: List = None, kwargs: Dict = None,
                name: str = None, timeout: int = 300) -> str:
        """Add a job to the queue.
        
        Args:
            func: The function to run
            args: Positional arguments for the function
            kwargs: Keyword arguments for the function
            name: Human-readable job name
            timeout: Maximum time to run in seconds
            
        Returns:
            Job ID
        """
        # Create a new job
        job = Job(func, args, kwargs, name, timeout)
        
        # Store the job
        with self._lock:
            self._jobs[job.id] = job
        
        # Add to queue
        self._queue.put(job)
        
        return job.id
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """Get a job by ID.
        
        Args:
            job_id: The job ID
            
        Returns:
            Job info dictionary or None if not found
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if job:
                return job.to_dict()
            return None
    
    def get_jobs(self, status: str = None) -> List[Dict]:
        """Get all jobs, optionally filtered by status.
        
        Args:
            status: Filter by job status
            
        Returns:
            List of job info dictionaries
        """
        with self._lock:
            if status:
                # Convert string status to enum
                try:
                    status_enum = JobStatus(status)
                    return [job.to_dict() for job in self._jobs.values()
                            if job.status == status_enum]
                except ValueError:
                    # Invalid status
                    return []
            else:
                return [job.to_dict() for job in self._jobs.values()]
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job if it's still pending.
        
        Args:
            job_id: The job ID
            
        Returns:
            True if cancelled, False otherwise
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if job and job.status == JobStatus.PENDING:
                job.status = JobStatus.CANCELLED
                # Note: Can't remove from queue, but worker will skip cancelled jobs
                return True
            return False
    
    def cleanup_jobs(self, max_age: int = 86400):
        """Remove old completed jobs.
        
        Args:
            max_age: Maximum age in seconds (default: 24 hours)
        """
        now = time.time()
        with self._lock:
            to_remove = []
            for job_id, job in self._jobs.items():
                if job.status in (JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED):
                    if job.completed_at and now - job.completed_at > max_age:
                        to_remove.append(job_id)
            
            for job_id in to_remove:
                del self._jobs[job_id]
    
    def _worker_thread(self):
        """Worker thread function."""
        while self._running:
            try:
                # Get a job from the queue
                job = self._queue.get(block=True, timeout=1.0)
                
                # None is a sentinel value indicating shutdown
                if job is None:
                    break
                
                # Skip cancelled jobs
                if job.status == JobStatus.CANCELLED:
                    self._queue.task_done()
                    continue
                
                # Run the job
                job.run()
                
                # Mark task as done
                self._queue.task_done()
            except queue.Empty:
                # Queue empty, continue polling
                continue
            except Exception as e:
                logger.error(f"Error in job queue worker: {str(e)}")
                traceback.print_exc()


# Create a singleton instance
job_queue = JobQueue()


def background_task(name=None, timeout=300):
    """Decorator to run a function as a background task.
    
    Args:
        name: Human-readable task name
        timeout: Maximum execution time in seconds
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Make sure job queue is started
            if not job_queue._running:
                job_queue.start()
            
            # Submit the task
            return job_queue.add_job(
                func=func,
                args=args,
                kwargs=kwargs,
                name=name or func.__name__,
                timeout=timeout
            )
        return wrapper
    return decorator
