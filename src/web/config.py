# Base Paths
HOME_DIR = os.path.expanduser("~")
BASE_DIR = os.path.join(HOME_DIR, "CreatureBox")
PHOTOS_DIR = os.path.join(BASE_DIR, "photos")
SCRIPTS_DIR = os.path.join(BASE_DIR, "Software")
CONFIG_DIR = BASE_DIR

# File Paths
CAMERA_SETTINGS_FILE = os.path.join(CONFIG_DIR, "camera_settings.csv")
SCHEDULE_SETTINGS_FILE = os.path.join(CONFIG_DIR, "schedule_settings.csv")
CONTROLS_FILE = os.path.join(CONFIG_DIR, "controls.txt")

# Web Server Settings
PORT = 5000
HOST = '0.0.0.0'
DEBUG = False

# Feature Flags
ENABLE_CAMERA_STREAM = True
ENABLE_BACKGROUND_JOBS = True

# Performance Settings
PHOTO_PROCESSING_THREADS = 2
CACHE_TIMEOUT = 300  # seconds
