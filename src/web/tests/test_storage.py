import pytest
import os
import shutil
from unittest.mock import patch, MagicMock
from ..services.storage import storage_manager


def test_storage_manager_singleton():
    """Test that storage_manager is a singleton."""
    from ..services.storage import StorageManager
    new_manager = StorageManager()
    assert new_manager is storage_manager


def test_get_storage_stats(tmpdir):
    """Test getting storage statistics."""
    # Create test directories
    photos_dir = tmpdir.mkdir("photos")
    photos_dir.mkdir("2025-01-01")
    photos_dir.mkdir("2025-02-01")
    backup_dir = tmpdir.mkdir("photos_backup")
    
    # Create some test files
    photo1 = photos_dir.join("2025-01-01/test1.jpg")
    photo1.write("test data 1")
    photo2 = photos_dir.join("2025-01-01/test2.jpg")
    photo2.write("test data 2")
    photo3 = photos_dir.join("2025-02-01/test3.jpg")
    photo3.write("test data 3")
    
    # Mock paths for testing
    with patch('src.web.services.storage.PHOTOS_DIR', str(photos_dir)), \
         patch('src.web.services.storage.PHOTOS_BACKUP_DIR', str(backup_dir)):
        
        # Get stats
        stats = storage_manager.get_storage_stats()
        
        # Check that stats are returned
        assert 'total_space' in stats
        assert 'used_space' in stats
        assert 'free_space' in stats
        assert 'photos' in stats
        assert 'backups' in stats
        assert 'external' in stats
        
        # Check photo stats
        assert stats['photos']['count'] == 3
        assert stats['photos']['size'] > 0
        assert len(stats['photos']['dates']) == 2
        assert '2025-01-01' in stats['photos']['dates']
        assert '2025-02-01' in stats['photos']['dates']
        
        # Check backup stats
        assert stats['backups']['count'] == 0
        assert stats['backups']['size'] == 0
        
        # External stats
        assert 'available' in stats['external']


@pytest.mark.parametrize("filename,expected", [
    ("test.jpg", True),
    ("test.JPG", True),
    ("test.jpeg", True),
    ("test.png", True),
    ("test.bmp", True),
    ("test.txt", False),
    ("test", False),
])
def test_is_photo_file(filename, expected):
    """Test is_photo_file function."""
    result = storage_manager._is_photo_file(filename)
    assert result == expected


@pytest.mark.parametrize("dirname,expected", [
    ("2025-01-01", True),
    ("2025-02-29", True),  # Leap year
    ("2025-13-01", False),  # Invalid month
    ("2025-01-32", False),  # Invalid day
    ("2025-1-1", False),    # Wrong format
    ("not-a-date", False),
])
def test_is_date_dir(dirname, expected):
    """Test is_date_dir function."""
    result = storage_manager._is_date_dir(dirname)
    assert result == expected


@patch('src.web.services.storage.shutil.copy2')
def test_backup_photos(mock_copy, tmpdir):
    """Test backup_photos function."""
    # Create test directories
    photos_dir = tmpdir.mkdir("photos")
    photos_dir.mkdir("2025-01-01")
    backup_dir = tmpdir.mkdir("photos_backup")
    
    # Create some test files
    photo1 = photos_dir.join("2025-01-01/test1.jpg")
    photo1.write("test data 1")
    photo2 = photos_dir.join("2025-01-01/test2.jpg")
    photo2.write("test data 2")
    
    # Mock background_task decorator to run synchronously
    with patch('src.web.services.storage.background_task', lambda name=None, timeout=None: lambda func: func), \
         patch('src.web.services.storage.PHOTOS_DIR', str(photos_dir)), \
         patch('src.web.services.storage.PHOTOS_BACKUP_DIR', str(backup_dir)):
        
        # Run backup
        result = storage_manager.backup_photos()
        
        # Check result
        assert result['status'] == 'success'
        assert result['backed_up'] == 2
        assert result['failed'] == 0
        assert result['total_size'] > 0
        
        # Check that copy was called for each file
        assert mock_copy.call_count == 2


@patch('src.web.services.storage.shutil.rmtree')
@patch('src.web.services.storage.shutil.copy2')
def test_clean_photos(mock_copy, mock_rmtree, tmpdir):
    """Test clean_photos function."""
    # Create test directories
    photos_dir = tmpdir.mkdir("photos")
    old_date_dir = photos_dir.mkdir("2024-01-01")  # Old directory to be cleaned
    new_date_dir = photos_dir.mkdir("2025-01-01")  # Recent directory to keep
    backup_dir = tmpdir.mkdir("photos_backup")
    
    # Create some test files
    old_photo = old_date_dir.join("old.jpg")
    old_photo.write("old data")
    new_photo = new_date_dir.join("new.jpg")
    new_photo.write("new data")
    
    # Mock functions and paths
    with patch('src.web.services.storage.background_task', lambda name=None, timeout=None: lambda func: func), \
         patch('src.web.services.storage.PHOTOS_DIR', str(photos_dir)), \
         patch('src.web.services.storage.PHOTOS_BACKUP_DIR', str(backup_dir)), \
         patch('src.web.services.storage.datetime') as mock_datetime, \
         patch('os.statvfs') as mock_statvfs:
        
        # Mock datetime.now to return a fixed date
        mock_now = MagicMock()
        mock_now.strftime.return_value = '2025-03-01'
        mock_datetime.now.return_value = mock_now
        mock_datetime.strftime.return_value = '2025-03-01'
        
        # Mock timedelta to work with our mock datetime
        mock_datetime.timedelta.side_effect = lambda days: MagicMock()
        
        # Mock os.statvfs to simulate low disk space
        mock_stat = MagicMock()
        mock_stat.f_blocks = 1000
        mock_stat.f_bfree = 100  # 10% free space (below 20% threshold)
        mock_stat.f_frsize = 1024
        mock_statvfs.return_value = mock_stat
        
        # Run cleanup
        result = storage_manager.clean_photos(days_to_keep=30, min_free_percent=20.0)
        
        # Check that old directory was deleted
        assert mock_rmtree.call_count == 1
        mock_rmtree.assert_called_with(str(old_date_dir))
        
        # Check result
        assert result['status'] == 'success'
        assert result['deleted'] == 1


def test_external_storage_detection():
    """Test external storage detection."""
    # Mock functions to simulate no external storage
    with patch('os.path.exists', return_value=False):
        stats = storage_manager._get_external_storage_stats()
        assert stats['available'] == False
    
    # Mock functions to simulate external storage
    with patch('os.path.exists', return_value=True), \
         patch('os.listdir', return_value=['pi']), \
         patch('os.path.isdir', return_value=True), \
         patch('os.path.ismount', return_value=True), \
         patch('os.statvfs') as mock_statvfs:
        
        # Setup mock statvfs return
        mock_stat = MagicMock()
        mock_stat.f_blocks = 1000
        mock_stat.f_bfree = 500
        mock_stat.f_frsize = 1024
        mock_statvfs.return_value = mock_stat
        
        # Test with mocked external storage
        with patch('os.listdir', side_effect=[['pi'], ['usb']]):
            stats = storage_manager._get_external_storage_stats()
            assert stats['available'] == True
            assert stats['total_space'] == 1000 * 1024
            assert stats['free_space'] == 500 * 1024


def test_api_endpoints(client):
    """Test storage API endpoints."""
    # Mock storage_manager functions
    with patch('src.web.routes.storage.storage_manager') as mock_manager:
        # Setup mock return values
        mock_manager.get_storage_stats.return_value = {
            'total_space': 1000000,
            'free_space': 500000,
            'photos': {'count': 100},
            'external': {'available': True}
        }
        mock_manager.backup_photos.return_value = 'job-123'
        mock_manager.backup_to_external.return_value = 'job-456'
        mock_manager.clean_photos.return_value = 'job-789'
        
        # Test stats endpoint
        response = client.get('/api/storage/stats')
        assert response.status_code == 200
        data = response.get_json()
        assert data['total_space'] == 1000000
        assert data['photos']['count'] == 100
        
        # Test backup endpoint
        response = client.post('/api/storage/backup')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['data']['job_id'] == 'job-123'
        
        # Test external backup endpoint
        response = client.post('/api/storage/backup/external')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['data']['job_id'] == 'job-456'
        
        # Test cleanup endpoint
        response = client.post('/api/storage/clean', json={'days_to_keep': 60})
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['data']['job_id'] == 'job-789'
        
        # Verify external backup fails when no external storage
        mock_manager.get_storage_stats.return_value = {
            'external': {'available': False}
        }
        response = client.post('/api/storage/backup/external')
        assert response.status_code == 404
