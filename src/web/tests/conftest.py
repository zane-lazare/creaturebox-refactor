import os
import pytest
import tempfile
from flask import Flask

from ..app import create_app
from .. import config


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary directory for test files
    test_dir = tempfile.mkdtemp()
    
    # Create test directory structure
    os.makedirs(os.path.join(test_dir, "photos"), exist_ok=True)
    os.makedirs(os.path.join(test_dir, "logs"), exist_ok=True)
    
    # Override configuration for testing
    config.BASE_DIR = test_dir
    config.PHOTOS_DIR = os.path.join(test_dir, "photos")
    config.LOG_DIR = os.path.join(test_dir, "logs")
    config.CAMERA_SETTINGS_FILE = os.path.join(test_dir, "camera_settings.csv")
    config.SCHEDULE_SETTINGS_FILE = os.path.join(test_dir, "schedule_settings.csv")
    config.CONTROLS_FILE = os.path.join(test_dir, "controls.txt")
    
    # Create empty camera settings file
    with open(config.CAMERA_SETTINGS_FILE, 'w') as f:
        f.write("SETTING,VALUE\n")
        f.write("ImageFileType,0\n")
        f.write("ExposureTime,500\n")
        f.write("AnalogueGain,1.5\n")
    
    # Create empty schedule settings file
    with open(config.SCHEDULE_SETTINGS_FILE, 'w') as f:
        f.write("SETTING,VALUE\n")
        f.write("weekday,1;2;3;4;5\n")
        f.write("hour,8;9;10;14;15;16\n")
        f.write("runtime,60\n")
    
    # Create controls file
    with open(config.CONTROLS_FILE, 'w') as f:
        f.write("name=TestCreatureBox\n")
        f.write("lights_on=false\n")
        f.write("runtime=60\n")
    
    # Disable hardware-dependent features for testing
    config.ENABLE_CAMERA_STREAM = False
    config.DEBUG = True
    
    # Create app with test config
    app = create_app()
    
    # Return test app
    yield app
    
    # Clean up temporary directory
    import shutil
    shutil.rmtree(test_dir)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def mock_camera():
    """Mock camera functionality for testing."""
    class MockCamera:
        def __init__(self):
            self.calibrated = False
            self.photos_taken = 0
        
        def calibrate(self):
            self.calibrated = True
            return True, "Calibration successful"
        
        def take_photo(self, filename=None):
            self.photos_taken += 1
            if filename:
                # Create an empty file to simulate a photo
                with open(filename, 'w') as f:
                    f.write("Mock photo data")
            return True, f"Photo captured: {filename}"
    
    return MockCamera()


@pytest.fixture
def mock_system():
    """Mock system functionality for testing."""
    class MockSystem:
        def __init__(self):
            self.rebooted = False
            self.shutdown = False
            self.lights_on = False
        
        def reboot(self):
            self.rebooted = True
            return True, "System rebooting"
        
        def shutdown(self):
            self.shutdown = True
            return True, "System shutting down"
        
        def toggle_lights(self, state=None):
            if state is not None:
                self.lights_on = state
            else:
                self.lights_on = not self.lights_on
            return True, f"Lights {'on' if self.lights_on else 'off'}"
    
    return MockSystem()
