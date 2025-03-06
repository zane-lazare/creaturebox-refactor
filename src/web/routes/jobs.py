# src/web/routes/jobs.py
from flask import Blueprint, jsonify, request, current_app
from ..services.job_queue import job_queue
from ..error_handlers import APIError, ErrorCode
from .api import create_success_response

# Create blueprint
jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@jobs_bp.route('/')
def list_jobs():
    """List all jobs with optional status filter."""
    status = request.args.get('status', None)
    jobs = job_queue.get_jobs(status)
    return jsonify(jobs)

@jobs_bp.route('/<job_id>')
def get_job(job_id):
    """Get a specific job by ID."""
    job = job_queue.get_job(job_id)
    
    if job is None:
        raise APIError(
            ErrorCode.RESOURCE_NOT_FOUND,
            f"Job not found: {job_id}"
        )
    
    return jsonify(job)

@jobs_bp.route('/<job_id>/cancel', methods=['POST'])
def cancel_job(job_id):
    """Cancel a job."""
    success = job_queue.cancel_job(job_id)
    
    if not success:
        raise APIError(
            ErrorCode.INVALID_REQUEST,
            f"Cannot cancel job {job_id}: not pending or not found"
        )
    
    return jsonify(create_success_response(
        message=f"Job {job_id} cancelled"
    ))

@jobs_bp.route('/cleanup', methods=['POST'])
def cleanup_jobs():
    """Clean up old completed jobs."""
    try:
        max_age = request.json.get('max_age', 86400) if request.json else 86400
        job_queue.cleanup_jobs(max_age)
        return jsonify(create_success_response(
            message=f"Cleaned up jobs older than {max_age} seconds"
        ))
    except Exception as e:
        current_app.logger.error(f"Error cleaning up jobs: {str(e)}")
        raise APIError(
            ErrorCode.UNKNOWN_ERROR,
            "Failed to clean up jobs",
            {"error": str(e)}
        )
