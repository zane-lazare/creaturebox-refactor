#!/usr/bin/env python3
"""
CreatureBox Virtual Environment Setup Script
-------------------------------------------
Creates and sets up a Python virtual environment for CreatureBox.
"""

import os
import sys
import subprocess
import shutil

# Import utility functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    from utils import (
        print_colored, print_success, print_warning, print_error,
        print_section, logger, HOME_DIR, TARGET_DIR, VENV_PATH
    )
except ImportError:
    # If import fails, set default values
    HOME_DIR = os.path.expanduser('~')
    TARGET_DIR = os.path.join(HOME_DIR, 'CreatureBox')
    VENV_PATH = os.path.join(HOME_DIR, 'creaturebox-venv')
    
    def print_section(msg): print(f"\n{msg}\n" + "-" * len(msg))
    def print_success(msg): print(f"✓ {msg}")
    def print_warning(msg): print(f"! {msg}")
    def print_error(msg): print(f"✗ {msg}")
    def print_colored(msg, *args): print(msg)

def create_virtual_environment(venv_path):
    """
    Create a Python virtual environment.
    
    :param venv_path: Path where the virtual environment will be created
    :return: Boolean indicating success or failure
    """
    print_section(f"Creating virtual environment at {venv_path}...")
    
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(venv_path), exist_ok=True)
        
        # Use venv to create virtual environment
        subprocess.run([sys.executable, '-m', 'venv', venv_path], 
                       check=True, 
                       capture_output=True, 
                       text=True)
        
        print_success("Virtual environment created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        if hasattr(e, 'stderr'):
            print_error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print_error(f"Unexpected error creating virtual environment: {e}")
        return False

def create_activate_script(venv_path, target_dir=None):
    """
    Create activation scripts for the virtual environment.
    
    :param venv_path: Path to the virtual environment
    :param target_dir: Target installation directory (optional)
    :return: Boolean indicating success or failure
    """
    try:
        # Create activation scripts in multiple locations for convenience
        script_locations = [
            os.path.join(os.path.dirname(venv_path), 'activate_venv.sh')
        ]
        
        # Also create in target directory if specified
        if target_dir and os.path.isdir(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            script_locations.append(os.path.join(target_dir, 'activate_venv.sh'))
        
        # Create the activation scripts
        for script_path in script_locations:
            with open(script_path, 'w') as f:
                f.write(f"""#!/bin/bash
# CreatureBox Virtual Environment Activation Script

# Activate the virtual environment
source {venv_path}/bin/activate

# Optional: Change to the CreatureBox project directory
# cd {target_dir if target_dir else '/path/to/creaturebox'}
""")
            
            # Make the script executable
            os.chmod(script_path, 0o755)
            print_success(f"Activation script created at {script_path}")
        
        return True
    except Exception as e:
        print_error(f"Failed to create activation script: {e}")
        return False

def main():
    """
    Main function to set up the virtual environment.
    """
    # Use the paths from utils if available
    venv_path = VENV_PATH
    target_dir = TARGET_DIR
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(venv_path), exist_ok=True)
    os.makedirs(target_dir, exist_ok=True)
    
    # Print paths that will be used
    print_section("Creating virtual environment with the following paths:")
    print(f"Virtual environment path: {venv_path}")
    print(f"Target installation directory: {target_dir}")
    
    # Ensure no existing virtual environment
    if os.path.exists(venv_path):
        print_warning(f"Virtual environment already exists at {venv_path}")
        print_warning("Do you want to remove and recreate it? (y/n)")
        response = input().lower().strip()
        
        if response != 'y':
            print_colored("Virtual environment setup cancelled.")
            return False
        
        # Remove existing virtual environment
        try:
            print_section(f"Removing existing virtual environment at {venv_path}...")
            shutil.rmtree(venv_path)
            print_success("Existing virtual environment removed.")
        except Exception as e:
            print_error(f"Failed to remove existing virtual environment: {e}")
            return False
    
    # Create virtual environment
    if not create_virtual_environment(venv_path):
        return False
    
    # Create activation scripts
    if not create_activate_script(venv_path, target_dir):
        return False
    
    # Optional: Install initial requirements
    try:
        pip_cmd = os.path.join(venv_path, 'bin', 'pip')
        if not os.path.exists(pip_cmd):
            # On Windows, pip is in the Scripts directory
            pip_cmd = os.path.join(venv_path, 'Scripts', 'pip')
        
        subprocess.run([pip_cmd, 'install', '--upgrade', 'pip'], check=True)
        print_success("Pip upgraded successfully.")
    except Exception as e:
        print_warning(f"Failed to upgrade pip: {e}")
    
    print_success("Virtual environment setup completed successfully!")
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
