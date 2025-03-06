import pytest
import time
import threading
from ..services.job_queue import job_queue, JobStatus, background_task


def test_job_queue_singleton():
    """Test that job_queue is a singleton."""
    from ..services.job_queue import JobQueue
    new_queue = JobQueue()
    assert new_queue is job_queue


def test_add_job():
    """Test adding a job to the queue."""
    # Make sure the queue is stopped for testing
    job_queue.stop()
    
    def test_function(x, y):
        return x + y
    
    # Add a job
    job_id = job_queue.add_job(test_function, args=[1, 2], name="TestJob")
    
    # Check that the job was added
    assert job_id is not None
    
    # Get the job
    job_info = job_queue.get_job(job_id)
    
    # Check job info
    assert job_info is not None
    assert job_info["name"] == "TestJob"
    assert job_info["status"] == JobStatus.PENDING.value


def test_job_execution():
    """Test that jobs execute correctly."""
    # Start the queue
    job_queue.start(num_workers=1)
    
    # Create a test function with a delay
    result_container = {"value": None}
    
    def test_function(x, y):
        time.sleep(0.1)  # Small delay to ensure state transitions
        result = x + y
        result_container["value"] = result
        return result
    
    # Add a job
    job_id = job_queue.add_job(test_function, args=[1, 2], name="ExecutionTest")
    
    # Wait for the job to complete
    max_wait = 10  # seconds
    start_time = time.time()
    while time.time() - start_time < max_wait:
        job_info = job_queue.get_job(job_id)
        if job_info["status"] in (JobStatus.COMPLETED.value, JobStatus.FAILED.value):
            break
        time.sleep(0.1)
    
    # Check job status and result
    job_info = job_queue.get_job(job_id)
    assert job_info["status"] == JobStatus.COMPLETED.value
    assert result_container["value"] == 3
    
    # Stop the queue
    job_queue.stop()


def test_job_failure():
    """Test handling of a failed job."""
    # Start the queue
    job_queue.start(num_workers=1)
    
    # Create a test function that raises an exception
    def failing_function():
        raise ValueError("Test error")
    
    # Add a job
    job_id = job_queue.add_job(failing_function, name="FailureTest")
    
    # Wait for the job to complete
    max_wait = 10  # seconds
    start_time = time.time()
    while time.time() - start_time < max_wait:
        job_info = job_queue.get_job(job_id)
        if job_info["status"] in (JobStatus.COMPLETED.value, JobStatus.FAILED.value):
            break
        time.sleep(0.1)
    
    # Check job status and error
    job_info = job_queue.get_job(job_id)
    assert job_info["status"] == JobStatus.FAILED.value
    assert job_info["error"] is not None
    assert job_info["error"]["type"] == "ValueError"
    assert job_info["error"]["message"] == "Test error"
    
    # Stop the queue
    job_queue.stop()


def test_background_task_decorator():
    """Test the background_task decorator."""
    # Make sure queue is stopped initially
    job_queue.stop()
    
    # Create a function with the decorator
    result_container = {"value": None}
    
    @background_task(name="BackgroundTest")
    def background_function(x, y):
        time.sleep(0.1)
        result = x * y
        result_container["value"] = result
        return result
    
    # Call the function (should start the queue)
    job_id = background_function(3, 4)
    
    # Check that the job was created
    assert job_id is not None
    
    # Wait for the job to complete
    max_wait = 10  # seconds
    start_time = time.time()
    while time.time() - start_time < max_wait:
        job_info = job_queue.get_job(job_id)
        if job_info["status"] in (JobStatus.COMPLETED.value, JobStatus.FAILED.value):
            break
        time.sleep(0.1)
    
    # Check the result
    assert result_container["value"] == 12
    
    # Stop the queue
    job_queue.stop()


def test_multiple_jobs():
    """Test running multiple jobs concurrently."""
    # Start the queue with 2 workers
    job_queue.start(num_workers=2)
    
    # Create a list to track completed jobs
    completed_jobs = []
    job_lock = threading.Lock()
    
    def test_function(job_id, delay):
        time.sleep(delay)
        with job_lock:
            completed_jobs.append(job_id)
        return job_id
    
    # Add several jobs with different delays
    job_ids = []
    for i in range(5):
        job_id = job_queue.add_job(test_function, args=[i, 0.2], name=f"MultiJob-{i}")
        job_ids.append(job_id)
    
    # Wait for all jobs to complete
    max_wait = 10  # seconds
    start_time = time.time()
    while time.time() - start_time < max_wait:
        with job_lock:
            if len(completed_jobs) == len(job_ids):
                break
        time.sleep(0.1)
    
    # Check that all jobs completed
    assert len(completed_jobs) == len(job_ids)
    
    # Check job statuses
    for job_id in job_ids:
        job_info = job_queue.get_job(job_id)
        assert job_info["status"] == JobStatus.COMPLETED.value
    
    # Stop the queue
    job_queue.stop()
