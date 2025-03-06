# src/web/routes/storage.py
from flask import Blueprint, jsonify, request, current_app
from ..services.storage import storage_manager
from ..error_handlers import APIError, ErrorCode
from .api import create_success_response

# Create blueprint
storage_bp = Blueprint('storage', __name__, url_prefix='/api/storage')

@storage_bp.route('/stats')
def storage_stats():
    """Get storage statistics."""
    stats = storage_manager.get_storage_stats()
    return jsonify(stats)

@storage_bp.route('/backup', methods=['POST'])
def backup_photos():
    """Backup photos."""
    try:
        # Start backup as background task
        job_id = storage_manager.backup_photos()
        
        return jsonify(create_success_response(
            data={'job_id': job_id},
            message='Photo backup started'
        ))
    except Exception as e:
        current_app.logger.error(f"Error starting backup: {str(e)}")
        raise APIError(
            ErrorCode.SYSTEM_COMMAND_FAILED,
            "Failed to start backup process",
            {"error": str(e)}
        )

@storage_bp.route('/backup/external', methods=['POST'])
def backup_to_external():
    """Backup photos to external storage."""
    try:
        # Get external storage stats first to check availability
        stats = storage_manager.get_storage_stats()
        
        if not stats['external']['available']:
            raise APIError(
                ErrorCode.RESOURCE_NOT_FOUND,
                "No external storage found"
            )
        
        # Start backup to external storage
        job_id = storage_manager.backup_to_external()
        
        return jsonify(create_success_response(
            data={'job_id': job_id},
            message='External backup started'
        ))
    except APIError:
        raise
    except Exception as e:
        current_app.logger.error(f"Error starting external backup: {str(e)}")
        raise APIError(
            ErrorCode.SYSTEM_COMMAND_FAILED,
            "Failed to start external backup process",
            {"error": str(e)}
        )

@storage_bp.route('/clean', methods=['POST'])
def clean_photos():
    """Clean up old photos."""
    try:
        # Get parameters
        days_to_keep = request.json.get('days_to_keep', 90) if request.json else 90
        min_free_percent = request.json.get('min_free_percent', 20.0) if request.json else 20.0
        
        # Validate parameters
        if days_to_keep < 1:
            raise APIError(
                ErrorCode.INVALID_REQUEST,
                "days_to_keep must be at least 1"
            )
        
        if min_free_percent < 5.0 or min_free_percent > 95.0:
            raise APIError(
                ErrorCode.INVALID_REQUEST,
                "min_free_percent must be between 5.0 and 95.0"
            )
        
        # Start cleanup
        job_id = storage_manager.clean_photos(
            days_to_keep=days_to_keep,
            min_free_percent=min_free_percent
        )
        
        return jsonify(create_success_response(
            data={'job_id': job_id},
            message='Photo cleanup started'
        ))
    except APIError:
        raise
    except Exception as e:
        current_app.logger.error(f"Error starting cleanup: {str(e)}")
        raise APIError(
            ErrorCode.SYSTEM_COMMAND_FAILED,
            "Failed to start cleanup process",
            {"error": str(e)}
        )
