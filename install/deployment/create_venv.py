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
from utils import (
    print_colored, print_success, print_warning, print_error,
    print_section, logger
)

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
        print_error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print_error(f"Unexpected error creating virtual environment: {e}")
        return False

def create_activate_script(venv_path):
    """
    Create an activation script for the virtual environment.
    
    :param venv_path: Path to the virtual environment
    :return: Boolean indicating success or failure
    """
    try:
        # Path for the activation script
        activate_script_path = os.path.join(os.path.dirname(venv_path), 'activate_venv.sh')
        
        # Create the activation script
        with open(activate_script_path, 'w') as f:
            f.write(f"""#!/bin/bash
# CreatureBox Virtual Environment Activation Script

# Activate the virtual environment
source {venv_path}/bin/activate

# Optional: Change to the CreatureBox project directory
# cd /path/to/creaturebox
""")
        
        # Make the script executable
        os.chmod(activate_script_path, 0o755)
        
        print_success(f"Activation script created at {activate_script_path}")
        return True
    except Exception as e:
        print_error(f"Failed to create activation script: {e}")
        return False

def main():
    """
    Main function to set up the virtual environment.
    """
    # Default paths
    home_dir = os.path.expanduser('~')
    venv_path = os.path.join(home_dir, 'creaturebox-venv')
    
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
            shutil.rmtree(venv_path)
        except Exception as e:
            print_error(f"Failed to remove existing virtual environment: {e}")
            return False
    
    # Create virtual environment
    if not create_virtual_environment(venv_path):
        return False
    
    # Create activation script
    if not create_activate_script(venv_path):
        return False
    
    # Optional: Install initial requirements
    try:
        pip_path = os.path.join(venv_path, 'bin', 'pip')
        subprocess.run([pip_path, 'install', '--upgrade', 'pip'], check=True)
        print_success("Pip upgraded successfully.")
    except Exception as e:
        print_warning(f"Failed to upgrade pip: {e}")
    
    print_success("Virtual environment setup completed successfully!")
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
