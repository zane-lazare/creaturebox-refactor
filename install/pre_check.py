#!/usr/bin/env python3
"""
CreatureBox Pre-Installation Check Script
----------------------------------------
This script checks if the system meets the requirements for installing CreatureBox.
"""

import os
import sys
import re
import subprocess
import platform
import shutil
from pathlib import Path

# Import utility functions
from utils import (
    print_colored, print_success, print_warning, print_error, 
    print_section, logger, GREEN, YELLOW, RED, NC,
    is_raspberry_pi, detect_pi_model, is_command_available,
    run_command
)

def check_raspberry_pi():
    """Check if running on a Raspberry Pi."""
    print_section("Checking system architecture...")
    
    # Check for Raspberry Pi model in /proc/cpuinfo
    try:
        is_pi = is_raspberry_pi()
        pi_model = detect_pi_model()
        
        if is_pi:
            # Try to get the model
            if pi_model != "unknown":
                print_success(f"Raspberry Pi detected: Model {pi_model}")
            else:
                print_success("Raspberry Pi detected.")
            return True
        else:
            print_warning("Not running on a Raspberry Pi.")
            print_warning("This software is designed for Raspberry Pi hardware.")
            return False
    except Exception as e:
        print_warning(f"Could not determine if this is a Raspberry Pi: {e}")
        return False

def check_python_version():
    """Check if Python version is 3.7 or newer."""
    print_section("Checking Python version...")
    
    # Use platform module to get Python version
    python_version = platform.python_version()
    python_version_tuple = tuple(map(int, python_version.split('.')))
    
    if python_version_tuple >= (3, 7):
        print_success(f"Python version {python_version} detected (3.7+ required).")
        return True
    else:
        print_error(f"Python version {python_version} is not supported.")
        print_error("CreatureBox requires Python 3.7 or newer.")
        return False

def check_disk_space():
    """Check if there's enough disk space."""
    print_section("Checking available disk space...")
    
    # Check available space in the home directory
    home_dir = os.path.expanduser('~')
    try:
        stat = os.statvfs(home_dir)
        available_space_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)
        
        if available_space_mb >= 1000:  # At least 1 GB
            print_success(f"Available space: {available_space_mb:.2f} MB (minimum 1000 MB required).")
            return True
        else:
            print_error(f"Low disk space: {available_space_mb:.2f} MB available.")
            print_error("At least 1000 MB (1 GB) is recommended.")
            return False
    except Exception as e:
        print_warning(f"Could not check disk space: {e}")
        return False
        
def check_camera():
    """Check if a camera is available."""
    print_section("Checking camera availability...")    
    # Try using libcamera-hello --list-cameras (more reliable with picamera2)
    try:
        result = run_command(['libcamera-hello', '--list-cameras'])
        if "Available cameras" in result.stdout and not "No cameras available" in result.stdout:
            print_success("Camera detected using libcamera-hello.")
            return True
    except Exception:
        pass    
    
    # Original detection methods
    try:
        result = run_command(['vcgencmd', 'get_camera'])
        if 'detected=1' in result.stdout:
            print_success("Camera module is detected and enabled.")
            return True
        else:
            print_warning("Camera module is not detected or not enabled.")
            print_warning("You may need to enable it using 'sudo raspi-config'.")
    except Exception:
        pass
            
    # Try an alternative approach
    if os.path.exists('/dev/video0'):
        print_success("Camera device /dev/video0 is available.")
        return True
    else:
        print_warning("No camera device found.")
        print_warning("Make sure your camera is connected and enabled.")
        return False
        
def check_required_commands():
    """Check if required commands are available."""
    print_section("Checking required commands...")
    
    required_commands = {
        'git': 'Git is required to clone the repository.',
        'python3': 'Python 3 is required to run the software.',
        'pip3': 'pip is required to install Python dependencies.',
        'nginx': 'Nginx is required for the web interface.'
    }
    
    missing_commands = [cmd for cmd in required_commands if not is_command_available(cmd)]
    
    for cmd in missing_commands:
        print_warning(f"{cmd} is not available. {required_commands[cmd]}")
    
    if missing_commands:
        print("\nMissing commands can be installed with:")
        print("sudo apt-get update")
        print(f"sudo apt-get install {' '.join(missing_commands)}")
        return False
    
    return True

def check_network():
    """Check network connectivity."""
    print_section("Checking network connectivity...")
    
    try:
        # Try to ping Google's DNS server (8.8.8.8)
        result = run_command(['ping', '-c', '1', '8.8.8.8'])
        
        if result.returncode == 0:
            print_success("Network connection is available.")
            return True
        else:
            print_warning("Network connection might not be available.")
            print_warning("Internet access is required for installation.")
            return False
    except Exception as e:
        print_warning(f"Could not check network connectivity: {e}")
        return False

def run_checks(show_summary=True):
    """Run all checks and return results."""
    checks = [
        (check_python_version, "Python version"),
        (check_raspberry_pi, "Raspberry Pi"),
        (check_camera, "Camera"),
        (check_disk_space, "Disk space"),
        (check_required_commands, "Required commands"),
        (check_network, "Network connectivity")
    ]
    
    results = []
    for check_func, name in checks:
        result = check_func()
        results.append((name, result))
        print()
    
    if show_summary:
        # Print summary
        print("\n==================================================")
        print("PRE-INSTALLATION CHECK SUMMARY")
        print("==================================================")
        
        all_passed = True
        
        for name, result in results:
            if result is True:
                status = f"{GREEN}PASS{NC}"
            elif result is False:
                status = f"{RED}FAIL{NC}"
                all_passed = False
            else:
                status = f"{YELLOW}WARNING{NC}"
            
            print(f"{name:.<25} {status}")
        
        print("\n==================================================")
        
        if all_passed:
            print_success("All checks passed. Your system meets the requirements for CreatureBox.")
            print("\nYou can proceed with the installation.")
            return True
        else:
            print_error("Some checks failed. Please address the issues before proceeding.")
            return False
    
    # Return True if all checks passed
    return all(result for _, result in results)

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    from utils import print_banner
    print_banner()
    run_checks()
