#!/usr/bin/env python3
"""
CreatureBox Installation Utilities
---------------------------------
Shared utility functions for the CreatureBox installation process.
"""

import os
import sys
import subprocess
import platform
import logging
import shutil
from pathlib import Path

# ANSI color codes
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
BOLD = '\033[1m'
NC = '\033[0m'  # No Color

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('creaturebox_installer')

# Define common paths
HOME_DIR = os.path.expanduser('~')
INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(INSTALL_DIR)
TARGET_DIR = os.path.join(HOME_DIR, 'CreatureBox')
VENV_PATH = os.path.join(HOME_DIR, 'creaturebox-venv')
DEPLOYMENT_DIR = os.path.join(INSTALL_DIR, 'deployment')

def setup_logging(log_file=None):
    """Set up logging to both console and file if specified."""
    if log_file:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Add file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

def print_colored(message, color=NC, bold=False):
    """Print a message with the specified color."""
    prefix = BOLD if bold else ""
    print(f"{prefix}{color}{message}{NC}")

def print_step(step_number, total_steps, message):
    """Print a step message with step number and total."""
    print_colored(f"\n[Step {step_number}/{total_steps}] {message}", BLUE, bold=True)
    print_colored("=" * 60, BLUE)

def print_section(message):
    """Print a section header."""
    print_colored(f"\n{message}", BLUE)
    print_colored("-" * len(message), BLUE)

def print_banner():
    """Print the CreatureBox banner."""
    print(f"{GREEN}")
    print("  ____                _                  ____            ")
    print(" / ___|_ __ ___  __ _| |_ _   _ _ __ ___| __ )  _____  __")
    print("| |   | '__/ _ \/ _` | __| | | | '__/ _ \  _ \ / _ \ \/ /")
    print("| |___| | |  __/ (_| | |_| |_| | | |  __/ |_) | (_) >  < ")
    print(" \____|_|  \___|\__,_|\__|\__,_|_|  \___|____/ \___/_/\_\\")
    print(f"{NC}")
    print("CreatureBox Installation Script")
    print("------------------------------")
    print()

def print_success(message):
    """Print a success message."""
    print_colored(f"✓ {message}", GREEN)

def print_warning(message):
    """Print a warning message."""
    print_colored(f"! {message}", YELLOW)

def print_error(message):
    """Print an error message."""
    print_colored(f"✗ {message}", RED)

def prompt_yes_no(question, default="yes"):
    """Ask a yes/no question and return the answer."""
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        prompt = " [y/n] "

    while True:
        print_colored(question + prompt, BLUE, bold=True)
        choice = input().lower()
        if choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")

def run_command(cmd, shell=False, check=True, capture_output=True):
    """Run a command and return the result."""
    try:
        if capture_output:
            result = subprocess.run(
                cmd, 
                shell=shell, 
                check=check, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            return result
        else:
            # Just run the command and let output go to terminal
            subprocess.run(cmd, shell=shell, check=check)
            return None
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        print_error(f"Command failed: {e}")
        return e

def is_raspberry_pi():
    """Check if running on a Raspberry Pi."""
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            return 'Raspberry Pi' in cpuinfo or 'BCM' in cpuinfo
    except FileNotFoundError:
        return False

def detect_pi_model():
    """Detect Raspberry Pi model."""
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            if 'Raspberry Pi 5' in cpuinfo:
                return "5"
            elif 'Raspberry Pi 4' in cpuinfo:
                return "4"
            elif 'Raspberry Pi' in cpuinfo:
                return "other"
    except FileNotFoundError:
        pass
    return "unknown"

def which(program):
    """Cross-platform which implementation."""
    return shutil.which(program)

def is_command_available(command):
    """Check if a command is available."""
    return which(command) is not None

def check_python_version():
    """Check if Python version is 3.7 or newer."""
    python_version = platform.python_version()
    python_version_tuple = tuple(map(int, python_version.split('.')))
    return python_version_tuple >= (3, 7), python_version

def create_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """Create a progress bar."""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    return f"\r{prefix} |{bar}| {percent}% {suffix}"

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
