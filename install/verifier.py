#!/usr/bin/env python3
"""
CreatureBox Installation Verification Script
-------------------------------------------
This script verifies that the CreatureBox installation is complete and functional.
"""

import os
import sys
import subprocess
import importlib
import json
import time
import requests
from pathlib import Path

# Import utility functions
from utils import (
    print_colored, print_success, print_warning, print_error, 
    print_section, print_step, logger, GREEN, YELLOW, RED, NC,
    run_command, HOME_DIR, TARGET_DIR, VENV_PATH
)

# Total number of verification steps
TOTAL_STEPS = 7

class VerificationError(Exception):
    """Exception raised for verification errors."""
    pass

def check_python_environment():
    """Check Python version and virtual environment."""
    print_step(1, TOTAL_STEPS, "Checking Python environment")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print_error(f"Python version {python_version.major}.{python_version.minor} is not supported.")
        print_error("CreatureBox requires Python 3.7+")
        return False
    
    print_success(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if virtual environment exists
    if not os.path.exists(VENV_PATH):
        print_error(f"Virtual environment not found at: {VENV_PATH}")
        return False
    
    # Check if we're in the correct virtual environment
    if os.environ.get('VIRTUAL_ENV') and os.environ.get('VIRTUAL_ENV').startswith(VENV_PATH):
        print_success("Running in the CreatureBox virtual environment")
    else:
        print_warning("Not running in the CreatureBox virtual environment")
        print_warning(f"Expected: {VENV_PATH}")
        print_warning(f"Current: {os.environ.get('VIRTUAL_ENV', 'None')}")
    
    return True

def check_required_packages():
    """Check if required Python packages are installed."""
    print_step(2, TOTAL_STEPS, "Checking required Python packages")
    
    required_packages = [
        'flask',
        'flask_cors',
        'numpy',
        'PIL',  # Pillow
        'piexif',
        'psutil',
        'RPi',  # RPi.GPIO
        'schedule'
    ]
    
    # Ensure we run pip from the virtual environment
    pip_path = os.path.join(VENV_PATH, 'bin', 'pip')
    if not os.path.exists(pip_path):
        pip_path = os.path.join(VENV_PATH, 'Scripts', 'pip')  # Windows
    
    installed_packages = []
    try:
        result = run_command([pip_path, 'list'])
        installed_packages = result.stdout.lower()
    except Exception as e:
        print_error(f"Could not check installed packages: {e}")
        return False
    
    missing_packages = []
    for package in required_packages:
        package_lower = package.lower()
        if package_lower == 'pil':
            # Check for Pillow instead
            if 'pillow' in installed_packages:
                print_success(f"Package 'Pillow' (PIL) is installed")
            else:
                missing_packages.append('Pillow (PIL)')
                print_error(f"Package 'Pillow' (PIL) is NOT installed")
        elif package_lower == 'rpi':
            # Check for RPi.GPIO
            if 'rpi.gpio' in installed_packages:
                print_success(f"Package 'RPi.GPIO' is installed")
            else:
                missing_packages.append('RPi.GPIO')
                print_error(f"Package 'RPi.GPIO' is NOT installed")
        else:
            if package_lower in installed_packages:
                print_success(f"Package '{package}' is installed")
            else:
                missing_packages.append(package)
                print_error(f"Package '{package}' is NOT installed")
    
    if missing_packages:
        print_error(f"Missing required packages: {', '.join(missing_packages)}")
        return False
    
    print_success("All required Python packages are installed")
    return True

def check_directory_structure():
    """Check if the CreatureBox directory structure is correct."""
    print_step(3, TOTAL_STEPS, "Checking directory structure")
    
    required_dirs = [
        '',  # Main directory
        'Software',
        'photos',
        'photos_backedup',
        'logs',
        'web',
        'web/static'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = os.path.join(TARGET_DIR, dir_name)
        if not os.path.isdir(dir_path):
            missing_dirs.append(dir_name)
            print_error(f"Directory '{dir_path}' is missing")
        else:
            print_success(f"Directory '{dir_path}' exists")
    
    if missing_dirs:
        print_error(f"Missing required directories: {', '.join(missing_dirs)}")
        return False
    
    print_success("Directory structure is correct")
    return True

def check_critical_files():
    """Check if critical files exist."""
    print_step(4, TOTAL_STEPS, "Checking critical files")
    
    required_files = [
        'TakePhoto.py',
        'Scheduler.py',
        'camera_settings.csv',
        'schedule_settings.csv',
        'controls.txt',
        'web/app.py'
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = os.path.join(TARGET_DIR, file_name)
        if not os.path.isfile(file_path):
            missing_files.append(file_name)
            print_error(f"File '{file_path}' is missing")
        else:
            print_success(f"File '{file_path}' exists")
    
    if missing_files:
        print_error(f"Missing required files: {', '.join(missing_files)}")
        return False
    
    print_success("All critical files are present")
    return True

def check_permissions():
    """Check if files and directories have correct permissions."""
    print_step(5, TOTAL_STEPS, "Checking file permissions")
    
    # Check if scripts are executable
    script_dirs = [
        os.path.join(TARGET_DIR, 'Software'),
        TARGET_DIR  # For symlinked scripts
    ]
    
    non_executable_scripts = []
    for script_dir in script_dirs:
        if os.path.isdir(script_dir):
            for file_name in os.listdir(script_dir):
                if file_name.endswith('.py') or file_name.endswith('.sh'):
                    file_path = os.path.join(script_dir, file_name)
                    if os.path.isfile(file_path) and not os.access(file_path, os.X_OK):
                        non_executable_scripts.append(file_path)
                        print_error(f"Script '{file_path}' is not executable")
    
    if non_executable_scripts:
        print_error(f"{len(non_executable_scripts)} scripts are not executable")
        return False
    
    print_success("File permissions are correct")
    return True

def check_system_services():
    """Check if system services are installed and running."""
    print_step(6, TOTAL_STEPS, "Checking system services")
    
    # Check web service
    try:
        result = run_command(['systemctl', 'is-active', 'creaturebox-web.service'])
        if result.stdout.strip() == 'active':
            print_success("Web service is running")
        else:
            print_error("Web service is not running")
            return False
    except Exception:
        print_error("Failed to check web service status")
        return False
    
    # Check nginx
    try:
        result = run_command(['systemctl', 'is-active', 'nginx'])
        if result.stdout.strip() == 'active':
            print_success("Nginx service is running")
        else:
            print_error("Nginx service is not running")
            return False
    except Exception:
        print_error("Failed to check nginx status")
        return False
    
    # Check if nginx config is valid
    try:
        result = run_command(['sudo', 'nginx', '-t'])
        if result.returncode == 0:
            print_success("Nginx configuration is valid")
        else:
            print_error(f"Nginx configuration is invalid: {result.stderr}")
            return False
    except Exception:
        print_error("Failed to check nginx configuration")
        return False
    
    print_success("System services are configured correctly")
    return True

def check_web_interface():
    """Check if the web interface is accessible."""
    print_step(7, TOTAL_STEPS, "Checking web interface accessibility")
    
    # Try to connect to the web interface
    try:
        # Try localhost access first
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print_success("Web interface is accessible via localhost")
            return True
    except requests.RequestException as e:
        print_warning(f"Could not access web interface via localhost: {e}")
    
    # Try IP address if localhost failed
    try:
        # Get IP address
        ip_result = run_command(['hostname', '-I'])
        ip_address = ip_result.stdout.strip().split()[0]
        
        response = requests.get(f'http://{ip_address}:5000', timeout=5)
        if response.status_code == 200:
            print_success(f"Web interface is accessible via IP address: {ip_address}")
            return True
    except (requests.RequestException, IndexError, subprocess.SubprocessError) as e:
        print_error(f"Could not access web interface via IP address: {e}")
    
    print_error("Web interface is not accessible")
    return False

def check_camera():
    """Check if the camera is accessible."""
    print_section("Checking camera accessibility")
    
    # Method 1: Check for video devices
    camera_detected = False
    if os.path.exists('/dev/video0'):
        print_success("Camera device /dev/video0 found")
        camera_detected = True
    
    # Method 2: Try libcamera-hello if available
    if not camera_detected:
        try:
            result = run_command(['libcamera-hello', '--list-cameras'])
            
            if "Available cameras" in result.stdout and not "No cameras available" in result.stdout:
                print_success("Camera detected via libcamera-hello")
                camera_detected = True
        except Exception:
            print_warning("Could not check camera using libcamera-hello")
    
    # Method 3: Try the traditional vcgencmd method (might not work on newer systems)
    if not camera_detected:
        try:
            result = run_command(['vcgencmd', 'get_camera'])
            
            if 'detected=1' in result.stdout:
                print_success("Camera detected via vcgencmd")
                camera_detected = True
            else:
                print_warning("Camera not detected via vcgencmd")
        except Exception:
            print_warning("vcgencmd not available or not working on this system")
    
    # If a camera was detected by any method, try to take a test photo
    if camera_detected:
        test_photo_path = os.path.join(TARGET_DIR, 'test_photo.jpg')
        try:
            # Use libcamera-still to take a photo
            result = run_command(['libcamera-still', '-o', test_photo_path, '-n', '--immediate'])
            
            if result.returncode == 0 and os.path.exists(test_photo_path):
                print_success("Successfully took a test photo")
                # Clean up test photo
                os.remove(test_photo_path)
                return True
            else:
                print_error(f"Failed to take a test photo: {result.stderr}")
                return False
        except Exception as e:
            print_error(f"Error while testing camera: {e}")
            return False
    
    print_error("No camera detected by any method")
    return False

def generate_system_info():
    """Generate system information for debugging."""
    print_section("Generating system information")
    
    system_info = {}
    
    # OS information
    try:
        with open('/etc/os-release', 'r') as f:
            os_info = {}
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os_info[key] = value.strip('"')
            system_info['os'] = os_info
    except:
        system_info['os'] = "Could not determine OS information"
    
    # Hardware information
    try:
        result = run_command(['cat', '/proc/cpuinfo'])
        system_info['hardware'] = result.stdout
    except:
        system_info['hardware'] = "Could not determine hardware information"
    
    # Python version
    system_info['python_version'] = sys.version
    
    # Environment variables
    system_info['environment_variables'] = {key: value for key, value in os.environ.items() 
                                          if not key.startswith('_')}
    
    # Write to file
    info_path = os.path.join(TARGET_DIR, 'system_info.json')
    with open(info_path, 'w') as f:
        json.dump(system_info, f, indent=2)
    
    print_success(f"System information written to {info_path}")
    return info_path

def run_verification():
    """Run all verification checks and return overall status."""
    verification_steps = [
        ("Python Environment", check_python_environment),
        ("Required Packages", check_required_packages),
        ("Directory Structure", check_directory_structure),
        ("Critical Files", check_critical_files),
        ("File Permissions", check_permissions),
        ("System Services", check_system_services),
        ("Web Interface", check_web_interface)
    ]
    
    # Optional camera check
    if os.path.exists('/dev/video0') or os.path.exists('/dev/vchiq'):
        verification_steps.append(("Camera", check_camera))
    
    # Run all checks
    results = {}
    for name, check_func in verification_steps:
        results[name] = check_func()
        print()
    
    # Count failures
    failures = sum(1 for result in results.values() if result is False)
    
    print("\n" + "="*50)
    print("VERIFICATION RESULTS:")
    print("="*50)
    
    for check, result in results.items():
        status = f"{GREEN}PASS{NC}" if result else f"{RED}FAIL{NC}"
        print(f"{check:.<30} {status}")
    
    print("="*50)
    if failures == 0:
        print_success("OVERALL STATUS: SUCCESS - All checks passed!")
        return True
    else:
        print_error(f"OVERALL STATUS: FAILED - {failures} check(s) failed")
        return False

def print_troubleshooting_suggestions():
    """Print troubleshooting suggestions."""
    print("\nTROUBLESHOOTING SUGGESTIONS:")
    print("1. Ensure the virtual environment is activated:")
    print(f"   source {os.path.join(VENV_PATH, 'bin', 'activate')}")
    print("2. Check service status:")
    print("   sudo systemctl status creaturebox-web.service")
    print("3. Check nginx configuration:")
    print("   sudo nginx -t")
    print("4. Check system logs:")
    print("   sudo journalctl -u creaturebox-web.service")
    print("   sudo journalctl -u nginx")
    
    # Generate system info
    info_path = generate_system_info()
    print(f"\nSystem information saved to: {info_path}")

def verify_installation():
    """Run verification and print results."""
    try:
        # First, make sure we're in the virtual environment
        if not os.environ.get('VIRTUAL_ENV'):
            venv_activate = os.path.join(VENV_PATH, 'bin', 'activate')
            venv_activate_cmd = f"source {venv_activate}"
            if os.path.exists(os.path.join(VENV_PATH, 'Scripts', 'activate')):  # Windows
                venv_activate = os.path.join(VENV_PATH, 'Scripts', 'activate')
                venv_activate_cmd = venv_activate
                
            if os.path.exists(venv_activate):
                print_warning(f"This script should be run within the virtual environment.")
                print_warning(f"Please activate it with: {venv_activate_cmd}")
                return False
        
        success = run_verification()
        
        if not success:
            print_troubleshooting_suggestions()
            return False
        else:
            print("\nVerification successful! CreatureBox is properly installed and configured.")
            print("\nYou can access the web interface at:")
            print("  - http://creaturebox.local    (from other devices on the network)")
            print("  - http://localhost:5000       (from this device)")
            
            # Try to get IP address
            try:
                ip_result = run_command(['hostname', '-I'])
                ip_address = ip_result.stdout.strip().split()[0]
                print(f"  - http://{ip_address}:5000   (using IP address)")
            except:
                pass
            
            return True
    except Exception as e:
        print_error(f"Unexpected error during verification: {e}")
        print_troubleshooting_suggestions()
        return False

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    from utils import print_banner
    print_banner()
    verify_installation()
