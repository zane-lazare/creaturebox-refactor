"""
Storage management service for photos and backups.
"""
import os
import shutil
import logging
import time
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Any

from ..config import PHOTOS_DIR, PHOTOS_BACKUP_DIR
from ..error_handlers import APIError, ErrorCode
from .job_queue import background_task

logger = logging.getLogger(__name__)


class StorageManager:
    """Storage management service."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(StorageManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the storage manager."""
        # Only initialize once for singleton
        if self._initialized:
            return
        
        # Ensure directories exist
        os.makedirs(PHOTOS_DIR, exist_ok=True)
        os.makedirs(PHOTOS_BACKUP_DIR, exist_ok=True)
        
        self._initialized = True
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics.
        
        Returns:
            Dictionary with storage statistics
        """
        try:
            # Get disk stats for photos directory
            disk_stats = os.statvfs(PHOTOS_DIR)
            total_space = disk_stats.f_blocks * disk_stats.f_frsize
            free_space = disk_stats.f_bfree * disk_stats.f_frsize
            used_space = total_space - free_space
            
            # Calculate total sizes and counts
            photos_stats = self._get_directory_stats(PHOTOS_DIR)
            backup_stats = self._get_directory_stats(PHOTOS_BACKUP_DIR)
            
            # Check if external storage is mounted
            external_stats = self._get_external_storage_stats()
            
            # Return combined stats
            return {
                'total_space': total_space,
                'used_space': used_space,
                'free_space': free_space,
                'photos': photos_stats,
                'backups': backup_stats,
                'external': external_stats
            }
        except Exception as e:
            logger.error(f"Error getting storage stats: {str(e)}")
            return {
                'total_space': 0,
                'used_space': 0,
                'free_space': 0,
                'photos': {'count': 0, 'size': 0},
                'backups': {'count': 0, 'size': 0},
                'external': {'available': False}
            }
    
    def _get_directory_stats(self, directory: str) -> Dict[str, Any]:
        """Get directory statistics.
        
        Args:
            directory: Directory path
            
        Returns:
            Dictionary with directory statistics
        """
        try:
            total_size = 0
            file_count = 0
            
            # Calculate total size and count
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if self._is_photo_file(file):
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                        file_count += 1
            
            # Get creation dates
            dates = []
            for item in os.listdir(directory):
                if os.path.isdir(os.path.join(directory, item)) and self._is_date_dir(item):
                    dates.append(item)
            
            return {
                'count': file_count,
                'size': total_size,
                'dates': sorted(dates)
            }
        except Exception as e:
            logger.error(f"Error getting directory stats for {directory}: {str(e)}")
            return {
                'count': 0,
                'size': 0,
                'dates': []
            }
    
    def _get_external_storage_stats(self) -> Dict[str, Any]:
        """Check for external storage (USB drive, etc).
        
        Returns:
            Dictionary with external storage information
        """
        try:
            # Look for mounted media paths
            external = {'available': False, 'path': None, 'total_space': 0, 'free_space': 0}
            
            # Common mount paths on Raspberry Pi
            mount_paths = ['/media', '/mnt']
            
            for mount_base in mount_paths:
                if os.path.exists(mount_base):
                    # Check all user mount points
                    for user_dir in os.listdir(mount_base):
                        user_path = os.path.join(mount_base, user_dir)
                        if os.path.isdir(user_path):
                            # Check all mounts for this user
                            for mount_point in os.listdir(user_path):
                                mount_path = os.path.join(user_path, mount_point)
                                if os.path.ismount(mount_path):
                                    external['available'] = True
                                    external['path'] = mount_path
                                    
                                    # Get storage stats
                                    disk_stats = os.statvfs(mount_path)
                                    external['total_space'] = disk_stats.f_blocks * disk_stats.f_frsize
                                    external['free_space'] = disk_stats.f_bfree * disk_stats.f_frsize
                                    return external
            
            return external
        except Exception as e:
            logger.error(f"Error checking external storage: {str(e)}")
            return {'available': False}
    
    def _is_photo_file(self, filename: str) -> bool:
        """Check if a file is a photo.
        
        Args:
            filename: File name
            
        Returns:
            True if file is a photo
        """
        photo_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
        return filename.lower().endswith(photo_extensions)
    
    def _is_date_dir(self, dirname: str) -> bool:
        """Check if a directory name is a date (YYYY-MM-DD format).
        
        Args:
            dirname: Directory name
            
        Returns:
            True if directory is a date
        """
        try:
            if len(dirname) != 10:
                return False
            
            year, month, day = dirname.split('-')
            
            # Check valid date
            datetime(int(year), int(month), int(day))
            return True
        except ValueError:
            return False
    
    @background_task(name="Backup Photos")
    def backup_photos(self, target_dir: Optional[str] = None) -> Dict[str, Any]:
        """Backup photos to the backup directory.
        
        Args:
            target_dir: Optional target directory (default: PHOTOS_BACKUP_DIR)
            
        Returns:
            Dictionary with backup results
        """
        if target_dir is None:
            target_dir = PHOTOS_BACKUP_DIR
        
        try:
            start_time = time.time()
            backed_up = 0
            failed = 0
            total_size = 0
            
            # Ensure backup directory exists
            os.makedirs(target_dir, exist_ok=True)
            
            # Get list of photos in the source directory
            photos = []
            for root, dirs, files in os.walk(PHOTOS_DIR):
                for file in files:
                    if self._is_photo_file(file):
                        source_path = os.path.join(root, file)
                        
                        # Determine path in backup directory
                        rel_path = os.path.relpath(source_path, PHOTOS_DIR)
                        backup_path = os.path.join(target_dir, rel_path)
                        
                        photos.append((source_path, backup_path))
            
            # Copy each photo
            for source_path, backup_path in photos:
                try:
                    # Create target directory if it doesn't exist
                    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                    
                    # Check if file exists and is newer
                    source_mtime = os.path.getmtime(source_path)
                    source_size = os.path.getsize(source_path)
                    
                    # Skip if backup exists and is the same
                    if os.path.exists(backup_path):
                        backup_mtime = os.path.getmtime(backup_path)
                        backup_size = os.path.getsize(backup_path)
                        
                        if backup_mtime >= source_mtime and backup_size == source_size:
                            continue
                    
                    # Copy the file
                    shutil.copy2(source_path, backup_path)
                    total_size += source_size
                    backed_up += 1
                except Exception as e:
                    logger.error(f"Error backing up {source_path}: {str(e)}")
                    failed += 1
            
            # Calculate duration
            duration = time.time() - start_time
            
            return {
                'status': 'success',
                'backed_up': backed_up,
                'failed': failed,
                'total_size': total_size,
                'duration': duration
            }
        except Exception as e:
            logger.error(f"Error during backup: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    @background_task(name="Backup to External")
    def backup_to_external(self) -> Dict[str, Any]:
        """Backup photos to external storage if available.
        
        Returns:
            Dictionary with backup results
        """
        try:
            # Check if external storage is available
            external = self._get_external_storage_stats()
            if not external['available'] or not external['path']:
                return {
                    'status': 'error',
                    'error': 'No external storage available'
                }
            
            # Create backup directory on external storage
            backup_dir = os.path.join(external['path'], 'CreatureBox_Backup')
            
            # Start backup
            return self.backup_photos(backup_dir)
        except Exception as e:
            logger.error(f"Error backing up to external storage: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    @background_task(name="Clean Photos")
    def clean_photos(self, days_to_keep: int = 90, min_free_percent: float = 20.0) -> Dict[str, Any]:
        """Clean up old photos to free up space.
        
        Args:
            days_to_keep: Number of days of photos to keep
            min_free_percent: Minimum percentage of free space to maintain
            
        Returns:
            Dictionary with cleanup results
        """
        try:
            # Check current free space
            stats = os.statvfs(PHOTOS_DIR)
            total_space = stats.f_blocks * stats.f_frsize
            free_space = stats.f_bfree * stats.f_frsize
            free_percent = (free_space / total_space) * 100
            
            # If we have enough free space, do nothing
            if free_percent >= min_free_percent:
                return {
                    'status': 'success',
                    'message': f'Sufficient free space ({free_percent:.1f}%), no cleaning needed',
                    'deleted': 0,
                    'freed': 0
                }
            
            # Get all date directories
            date_dirs = []
            
            for item in os.listdir(PHOTOS_DIR):
                item_path = os.path.join(PHOTOS_DIR, item)
                if os.path.isdir(item_path) and self._is_date_dir(item):
                    date_dirs.append((item, item_path))
            
            # Sort by date (oldest first)
            date_dirs.sort()
            
            # Calculate cutoff date
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            cutoff_str = cutoff_date.strftime('%Y-%m-%d')
            
            # Delete old directories
            deleted_count = 0
            freed_space = 0
            
            for date_str, dir_path in date_dirs:
                # Stop if we've freed enough space
                if free_percent >= min_free_percent:
                    break
                
                # Skip if newer than cutoff
                if date_str >= cutoff_str:
                    continue
                
                try:
                    # Check if backed up
                    backup_path = os.path.join(PHOTOS_BACKUP_DIR, date_str)
                    if not os.path.exists(backup_path):
                        # Backup before deleting
                        logger.info(f"Backing up {date_str} before deletion")
                        
                        # Create date directory in backup
                        os.makedirs(backup_path, exist_ok=True)
                        
                        # Copy files
                        for file in os.listdir(dir_path):
                            if self._is_photo_file(file):
                                source_file = os.path.join(dir_path, file)
                                backup_file = os.path.join(backup_path, file)
                                shutil.copy2(source_file, backup_file)
                    
                    # Calculate directory size
                    dir_size = 0
                    for file in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file)
                        if os.path.isfile(file_path):
                            dir_size += os.path.getsize(file_path)
                    
                    # Delete directory
                    shutil.rmtree(dir_path)
                    deleted_count += 1
                    freed_space += dir_size
                    
                    # Recalculate free space
                    stats = os.statvfs(PHOTOS_DIR)
                    free_space = stats.f_bfree * stats.f_frsize
                    free_percent = (free_space / total_space) * 100
                except Exception as e:
                    logger.error(f"Error cleaning directory {dir_path}: {str(e)}")
            
            return {
                'status': 'success',
                'message': f'Cleaned up {deleted_count} directories, freed {freed_space} bytes',
                'deleted': deleted_count,
                'freed': freed_space,
                'free_percent': free_percent
            }
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }


# Create singleton instance
storage_manager = StorageManager()
