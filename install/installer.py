#!/usr/bin/env python3
"""
CreatureBox Installation Script
------------------------------
This script installs the CreatureBox software and web dashboard.
"""

import os
import sys
import shutil
import time
import subprocess
import importlib.util
from pathlib import Path

# Import utility functions
from utils import (
    print_colored, print_success, print_warning, print_error, 
    print_section, print_step, logger, GREEN, YELLOW, RED, NC,
    run_command, prompt_yes_no, is_raspberry_pi, detect_pi_model,
    HOME_DIR, REPO_DIR, TARGET_DIR, VENV_PATH, INSTALL_DIR, ensure_directories_exist
)

# Total number of installation steps for progress tracking
TOTAL_STEPS = 8

def detect_pi_model_details():
    """Detect and return Raspberry Pi model information."""
    pi_model = detect_pi_model()
    print_section(f"Detected Raspberry Pi Model: {pi_model if pi_model != 'unknown' else 'Unknown'}")
    return pi_model

def install_system_packages():
    """Install required system packages."""
    print_step(1, TOTAL_STEPS, "Installing required system packages")
    
    try:
        # Update package lists
        print_section("Updating package lists...")
        run_command(['sudo', 'apt-get', 'update'], capture_output=False)
        
        # Install required packages
        print_section("Installing packages...")
        packages = [
            # Core system dependencies
            'git', 'wget', 'curl', 'software-properties-common', 
            'gnupg', 'ca-certificates',
            
            # Python related
            'python3', 'python3-pip', 'python3-venv',
            
            # Camera dependencies
            'libcamera-dev', 'libcamera-apps', 'python3-libcamera',
            'python3-picamera2', 'libcap-dev', 'v4l-utils',
            
            # Networking
            'network-manager', 'avahi-daemon', 'nginx',
            
            # Utilities
            'rsync', 'psmisc'
        ]
        
        run_command(['sudo', 'apt-get', 'install', '-y'] + packages, capture_output=False)
        print_success("System packages installed successfully")
        return True
    except Exception as e:
        print_error(f"Failed to install system packages: {e}")
        return False

def setup_virtual_environment():
    """Setup Python virtual environment."""
    print_step(2, TOTAL_STEPS, "Setting up Python virtual environment")
    
    try:
        # Create target directory first to ensure it exists
        os.makedirs(TARGET_DIR, exist_ok=True)
        
        # Use the dedicated create_venv.py script from deployment
        venv_script = os.path.join(INSTALL_DIR, 'deployment', 'create_venv.py')
        
        if os.path.exists(venv_script):
            # Run the script directly
            result = run_command(['python3', venv_script], capture_output=False)
            if result and result.returncode != 0:
                raise Exception(f"Virtual environment script failed with code {result.returncode}")
        else:
            # Manual virtual environment setup if script doesn't exist
            if os.path.exists(VENV_PATH):
                print_warning(f"Virtual environment already exists at {VENV_PATH}")
                if prompt_yes_no("Do you want to recreate it?", "no"):
                    print_section("Removing existing virtual environment...")
                    shutil.rmtree(VENV_PATH)
                    print_section("Creating new virtual environment...")
                    run_command(['python3', '-m', 'venv', VENV_PATH], capture_output=False)
            else:
                print_section(f"Creating virtual environment at {VENV_PATH}...")
                run_command(['python3', '-m', 'venv', VENV_PATH], capture_output=False)
                
            # Write activation scripts to multiple locations
            for script_path in [
                os.path.join(HOME_DIR, 'activate_venv.sh'),
                os.path.join(TARGET_DIR, 'activate_venv.sh')
            ]:
                with open(script_path, 'w') as f:
                    f.write(f'#!/bin/bash\nsource {VENV_PATH}/bin/activate\n')
                os.chmod(script_path, 0o755)
                print_success(f"Activation script created at {script_path}")
        
        print_success("Virtual environment setup completed successfully!")
        return True
    except Exception as e:
        print_error(f"Failed to setup virtual environment: {e}")
        return False

def install_python_dependencies(pi_model):
    """Install Python dependencies."""
    print_step(3, TOTAL_STEPS, "Installing Python dependencies")
    
    try:
        # Determine the correct pip path based on platform
        pip_path = os.path.join(VENV_PATH, 'bin', 'pip')
        if not os.path.exists(pip_path) and os.path.exists(os.path.join(VENV_PATH, 'Scripts', 'pip')):
            # Windows uses Scripts directory
            pip_path = os.path.join(VENV_PATH, 'Scripts', 'pip')
            
        # Determine the correct activation script based on platform
        if os.name == 'nt':  # Windows
            activate_cmd = f"{os.path.join(VENV_PATH, 'Scripts', 'activate')} && "
        else:  # Unix/Linux
            activate_cmd = f"source {os.path.join(VENV_PATH, 'bin', 'activate')} && "
        
        # Upgrade pip, setuptools, and wheel
        print_section("Upgrading pip, setuptools, and wheel...")
        run_command(
            activate_cmd + "pip install --upgrade pip setuptools wheel", 
            shell=True, 
            capture_output=False
        )
        
        # Install from requirements.txt
        # Check multiple locations for requirements.txt
        requirements_paths = [
            os.path.join(REPO_DIR, 'requirements.txt'),  # Root directory (standard)
            os.path.join(INSTALL_DIR, 'requirements.txt')  # Install directory (alternative)
        ]
        
        requirements_path = next((path for path in requirements_paths if os.path.exists(path)), None)
        
        if requirements_path:
            print_section("Installing packages from requirements.txt...")
            run_command(
                activate_cmd + f"pip install -r {requirements_path}", 
                shell=True, 
                capture_output=False
            )
        else:
            # Fallback installation
            print_section("requirements.txt not found, installing packages directly...")
            packages = [
                'Flask==2.1.0',
                'flask-cors==3.0.10',
                'numpy==1.22.0',
                'opencv-python-headless==4.5.5.64',
                'Pillow==9.0.0',
                'piexif==1.1.3',
                'psutil==5.9.0',
                'RPi.GPIO==0.7.0',
                'schedule==1.1.0',
                'python-crontab==2.6.0'
            ]
            
            # Install picamera2 for Pi 5
            if pi_model == "5":
                packages.append('picamera2')
                
            packages_str = ' '.join(packages)
            run_command(
                activate_cmd + f"pip install {packages_str}", 
                shell=True, 
                capture_output=False
            )
        
        # Create a file to indicate which Pi model was used for installation
        os.makedirs(TARGET_DIR, exist_ok=True)
        with open(os.path.join(TARGET_DIR, 'pi_model.txt'), 'w') as f:
            f.write(f"PI_MODEL={pi_model}\n")
        
        # Check if PiJuice is present and install the module if needed
        try:
            result = run_command(['lsusb'])
            if 'PiJuice' in result.stdout:
                print_section("PiJuice detected, installing PiJuice Python module...")
                run_command(
                    activate_cmd + "pip install pijuice.py", 
                    shell=True, 
                    capture_output=False
                )
        except Exception as juice_err:
            print_warning(f"Could not check for PiJuice: {juice_err}")
        
        print_success("Python dependencies installed successfully")
        return True
    except Exception as e:
        print_error(f"Failed to install Python dependencies: {e}")
        return False

def create_directory_structure():
    """Create directory structure."""
    print_step(4, TOTAL_STEPS, "Creating directory structure")
    
    try:
        directories = [
            '',  # Main directory
            'software',
            'photos',
            'photos_backedup',
            'logs',
            'web',
            'web/static',
            'web/static/css',
            'web/static/js',
            'web/static/img'
        ]
        
        for directory in directories:
            path = os.path.join(TARGET_DIR, directory)
            os.makedirs(path, exist_ok=True)
            print(f"Created directory: {path}")
        
        print_success("Directory structure created successfully")
        return True
    except Exception as e:
        print_error(f"Failed to create directory structure: {e}")
        return False

def copy_files():
    """Copy files to installation directory."""
    print_step(5, TOTAL_STEPS, "Copying files to installation directory")
    
    try:
        # Ensure source files exist
        src_dir = os.path.join(REPO_DIR, 'src')
        if not os.path.exists(src_dir):
            print_error(f"Source directory not found: {src_dir}")
            return False
        
        # Create required directories first
        for dir_path in [
            os.path.join(TARGET_DIR, 'software'),
            os.path.join(TARGET_DIR, 'web'),
            os.path.join(TARGET_DIR, 'web', 'static')
        ]:
            os.makedirs(dir_path, exist_ok=True)
        
        # Copy files using a safer approach
        print_section("Copying Software files...")
        software_src = os.path.join(src_dir, 'software')
        software_dst = os.path.join(TARGET_DIR, 'software')
        
        if os.path.exists(software_src):
            # Use shutil.copytree with dirs_exist_ok on Python 3.8+
            if hasattr(shutil, 'copytree') and 'dirs_exist_ok' in shutil.copytree.__code__.co_varnames:
                shutil.copytree(software_src, software_dst, dirs_exist_ok=True)
            else:
                # Fallback for older Python versions
                for item in os.listdir(software_src):
                    s = os.path.join(software_src, item)
                    d = os.path.join(software_dst, item)
                    if os.path.isdir(s):
                        if os.path.exists(d):
                            shutil.rmtree(d)
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)
        else:
            print_warning(f"Software source directory not found: {software_src}")
        
        print_section("Copying config files...")
        config_src = os.path.join(src_dir, 'config')
        if os.path.exists(config_src):
            for item in os.listdir(config_src):
                s = os.path.join(config_src, item)
                d = os.path.join(TARGET_DIR, item)
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
        else:
            print_warning(f"Config source directory not found: {config_src}")
        
        print_section("Copying web files...")
        web_app_src = os.path.join(src_dir, 'web', 'app.py')
        web_app_dst = os.path.join(TARGET_DIR, 'web')
        if os.path.exists(web_app_src):
            shutil.copy2(web_app_src, web_app_dst)
        else:
            print_warning(f"Web app source file not found: {web_app_src}")
        
        web_static_src = os.path.join(src_dir, 'web', 'static')
        web_static_dst = os.path.join(TARGET_DIR, 'web', 'static')
        if os.path.exists(web_static_src):
            # Use shutil.copytree with dirs_exist_ok on Python 3.8+
            if hasattr(shutil, 'copytree') and 'dirs_exist_ok' in shutil.copytree.__code__.co_varnames:
                shutil.copytree(web_static_src, web_static_dst, dirs_exist_ok=True)
            else:
                # Fallback for older Python versions
                for item in os.listdir(web_static_src):
                    s = os.path.join(web_static_src, item)
                    d = os.path.join(web_static_dst, item)
                    if os.path.isdir(s):
                        if os.path.exists(d):
                            shutil.rmtree(d)
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)
        else:
            print_warning(f"Web static source directory not found: {web_static_src}")
        
        # Copy README and LICENSE
        readme_path = os.path.join(REPO_DIR, 'README.md')
        license_path = os.path.join(REPO_DIR, 'license.md')
        
        if os.path.exists(readme_path):
            shutil.copy2(readme_path, TARGET_DIR)
        
        if os.path.exists(license_path):
            shutil.copy2(license_path, TARGET_DIR)
        
        print_success("Files copied successfully")
        return True
    except Exception as e:
        print_error(f"Failed to copy files: {e}")
        return False

def set_permissions():
    """Set file permissions."""
    print_step(6, TOTAL_STEPS, "Setting file permissions")
    
    try:
        # Skip permission setting on Windows
        if os.name == 'nt':
            print_warning("Skipping permission setting on Windows")
            return True
            
        # Make scripts executable
        print_section("Making scripts executable...")
        run_command(
            f"find {TARGET_DIR}/software -type f \( -name '*.py' -o -name '*.sh' \) -exec chmod +x {{}} \;", 
            shell=True, 
            capture_output=False
        )
        
        # Make web app executable
        web_app_path = os.path.join(TARGET_DIR, 'web', 'app.py')
        if os.path.exists(web_app_path):
            os.chmod(web_app_path, 0o755)
        
        # Set directory permissions
        print_section("Setting directory permissions...")
        directories = [
            os.path.join(TARGET_DIR, 'software'),
            os.path.join(TARGET_DIR, 'web'),
            os.path.join(TARGET_DIR, 'photos'),
            os.path.join(TARGET_DIR, 'logs')
        ]
        
        for directory in directories:
            if os.path.exists(directory):
                run_command(['chmod', '-R', '755', directory], capture_output=False)
        
        # Set file permissions for CSV files
        print_section("Setting file permissions for data files...")
        run_command(
            f"find {TARGET_DIR} -type f -name '*.csv' -exec chmod 644 {{}} \;", 
            shell=True, 
            capture_output=False
        )
        
        # Set permissions for controls.txt if it exists
        controls_file = os.path.join(TARGET_DIR, 'controls.txt')
        if os.path.exists(controls_file):
            os.chmod(controls_file, 0o644)
        
        print_success("Permissions set successfully")
        return True
    except Exception as e:
        print_error(f"Failed to set permissions: {e}")
        return False

def create_symlinks():
    """Create symlinks for convenience."""
    print_step(7, TOTAL_STEPS, "Creating symlinks")
    
    try:
        # Skip symlink creation on Windows
        if os.name == 'nt':
            print_warning("Skipping symlink creation on Windows")
            return True
            
        scripts = [
            'TakePhoto.py',
            'Scheduler.py',
            'Attract_On.py',
            'Attract_Off.py',
            'StopScheduledShutdown.py'
        ]
        
        for script in scripts:
            source = os.path.join(TARGET_DIR, 'software', script)
            target = os.path.join(TARGET_DIR, script)
            
            if os.path.exists(source):
                # Remove existing symlink if it exists
                if os.path.exists(target):
                    os.remove(target)
                
                # Create symlink
                os.symlink(source, target)
                print(f"Created symlink: {target} -> {source}")
            else:
                print_warning(f"Could not create symlink for {script} (file not found)")
        
        print_success("Symlinks created successfully")
        return True
    except Exception as e:
        print_error(f"Failed to create symlinks: {e}")
        return False

def setup_web_service():
    """Set up web service."""
    print_step(8, TOTAL_STEPS, "Setting up web service")
    
    try:
        # Skip on Windows
        if os.name == 'nt':
            print_warning("Skipping web service setup on Windows")
            return True
            
        web_port = 5000
        user = os.environ.get('USER', os.environ.get('USERNAME', 'pi'))
        
        print_section("Setting up deployment files...")
        
        # Create the deployment directory in the target location
        deployment_dir = os.path.join(TARGET_DIR, 'deployment')
        os.makedirs(deployment_dir, exist_ok=True)
        
        # Copy deployment files from the install directory to the target directory
        src_deployment_dir = os.path.join(INSTALL_DIR, 'deployment')
        # Service file
        service_file = os.path.join(src_deployment_dir, 'creaturebox.service')
        if os.path.exists(service_file):
            # Copy the service file
            dest_service_file = os.path.join(deployment_dir, 'creaturebox.service')
            shutil.copy2(service_file, dest_service_file)
            
            # Customize paths in the service file
            with open(dest_service_file, 'r') as f:
                content = f.read()
            
            # Replace paths with actual installation paths
            content = content.replace('/opt/creaturebox', TARGET_DIR)
            content = content.replace('/opt/creaturebox-venv', VENV_PATH)
            content = content.replace('User=creaturebox', f'User={user}')
            content = content.replace('Group=creaturebox', f'Group={user}')
            
            # Write modified content back
            with open(dest_service_file, 'w') as f:
                f.write(content)
            
            # Copy to system location
            run_command(['sudo', 'cp', dest_service_file, '/etc/systemd/system/creaturebox-web.service'], capture_output=False)
        else:
            # Fallback to creating a basic service file
            print_section("Creating basic systemd service file...")
            service_content = f"""[Unit]
Description=CreatureBox Web Interface
After=network.target

[Service]
User={user}
WorkingDirectory={TARGET_DIR}/web
ExecStart={VENV_PATH}/bin/python {TARGET_DIR}/web/app.py
Restart=always
RestartSec=5
Environment="PATH={VENV_PATH}/bin:$PATH"

[Install]
WantedBy=multi-user.target
"""
            
            # Write service file
            temp_service_file = os.path.join(TARGET_DIR, 'creaturebox-web.service')
            with open(temp_service_file, 'w') as f:
                f.write(service_content)
            
            # Copy to system location
            run_command(['sudo', 'cp', temp_service_file, '/etc/systemd/system/'], capture_output=False)
        
        # Nginx configuration
        nginx_file = os.path.join(src_deployment_dir, 'nginx.conf')
        if os.path.exists(nginx_file):
            print_section("Configuring Nginx from deployment template...")
            # Copy the nginx config file
            dest_nginx_file = os.path.join(deployment_dir, 'nginx.conf')
            shutil.copy2(nginx_file, dest_nginx_file)
            
            # Customize paths in the nginx config file
            with open(dest_nginx_file, 'r') as f:
                nginx_content = f.read()
            
            # Replace paths with actual installation paths
            nginx_content = nginx_content.replace('/opt/creaturebox', TARGET_DIR)
            nginx_content = nginx_content.replace('127.0.0.1:5000', f'127.0.0.1:{web_port}')
            
            # Write modified content back
            with open(dest_nginx_file, 'w') as f:
                f.write(nginx_content)
            
            # Copy to nginx sites
            run_command(['sudo', 'cp', dest_nginx_file, '/etc/nginx/sites-available/creaturebox'], capture_output=False)
        else:
            # Fallback to creating a basic nginx config
            print_section("Creating basic Nginx configuration...")
            nginx_config = f"""server {{
    listen 80;
    server_name creaturebox.local;

    location / {{
        proxy_pass http://127.0.0.1:{web_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}

    # Special configuration for camera streaming
    location /api/camera/stream {{
        proxy_pass http://127.0.0.1:{web_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # Disable buffering for streaming content
        proxy_buffering off;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Increased timeouts for streaming
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }}

    client_max_body_size 100M;
}}
"""
            
            # Write nginx config to a temporary location
            temp_nginx_config = os.path.join(TARGET_DIR, 'creaturebox.nginx')
            with open(temp_nginx_config, 'w') as f:
                f.write(nginx_config)
            
            # Copy to system location
            run_command(
                ['sudo', 'cp', temp_nginx_config, '/etc/nginx/sites-available/creaturebox'], 
                capture_output=False
            )
        
        # Gunicorn configuration if available
        gunicorn_file = os.path.join(src_deployment_dir, 'gunicorn.conf.py')
        if os.path.exists(gunicorn_file):
            # Check if gunicorn package is installed
            gunicorn_installed = False
            try:
                result = run_command([f"{VENV_PATH}/bin/pip", "show", "gunicorn"])
                gunicorn_installed = result.returncode == 0
            except Exception:
                pass
                
            if not gunicorn_installed:
                print_section("Installing gunicorn...")
                run_command([f"{VENV_PATH}/bin/pip", "install", "gunicorn"], capture_output=False)
            
            # Copy the gunicorn config file
            dest_gunicorn_file = os.path.join(deployment_dir, 'gunicorn.conf.py')
            shutil.copy2(gunicorn_file, dest_gunicorn_file)
            
            # Customize paths in the gunicorn config file
            with open(dest_gunicorn_file, 'r') as f:
                gunicorn_content = f.read()
            
            # Replace paths with actual installation paths
            gunicorn_content = gunicorn_content.replace('/opt/creaturebox', TARGET_DIR)
            gunicorn_content = gunicorn_content.replace('/var/log/creaturebox', os.path.join(TARGET_DIR, 'logs'))
            
            # Write modified content back
            with open(dest_gunicorn_file, 'w') as f:
                f.write(gunicorn_content)
        
        print_section("Enabling services...")
        run_command(
            ['sudo', 'ln', '-sf', '/etc/nginx/sites-available/creaturebox', '/etc/nginx/sites-enabled/'], 
            capture_output=False
        )
        
        run_command(['sudo', 'systemctl', 'enable', 'creaturebox-web.service'], capture_output=False)
        run_command(['sudo', 'systemctl', 'start', 'creaturebox-web.service'], capture_output=False)
        run_command(['sudo', 'systemctl', 'restart', 'nginx'], capture_output=False)
        
        # Create crontab example file
        print_section("Creating crontab example file...")
        crontab_content = f"""# Example crontab entries for CreatureBox
# To install: crontab -e

# Take photo every hour
0 * * * * {VENV_PATH}/bin/python {TARGET_DIR}/TakePhoto.py

# Run scheduler at boot
@reboot {VENV_PATH}/bin/python {TARGET_DIR}/Scheduler.py

# Backup photos daily at 3 AM
0 3 * * * {VENV_PATH}/bin/python {TARGET_DIR}/software/Backup_Files.py
"""
        
        crontab_path = os.path.join(TARGET_DIR, 'crontab.example')
        with open(crontab_path, 'w') as f:
            f.write(crontab_content)
        
        print_success("Web service set up successfully")
        return True
    except Exception as e:
        print_error(f"Failed to set up web service: {e}")
        return False

def run_installation(interactive=True):
    """Run the complete installation process."""
    try:
        # Ensure all directories exist
        ensure_directories_exist()
        
        # Display setup information
        print_section("Installation Paths:")
        print(f"Installation directory: {TARGET_DIR}")
        print(f"Virtual environment: {VENV_PATH}")
        print("")
        
        # Detect Raspberry Pi model
        pi_model = detect_pi_model_details()
        
        # Install components
        steps = [
            ("Installing system packages", install_system_packages),
            ("Setting up virtual environment", setup_virtual_environment),
            ("Installing Python dependencies", lambda: install_python_dependencies(pi_model)),
            ("Creating directory structure", create_directory_structure),
            ("Copying files", copy_files),
            ("Setting permissions", set_permissions),
            ("Creating symlinks", create_symlinks),
            ("Setting up web service", setup_web_service)
        ]
        
        for i, (name, step_func) in enumerate(steps):
            if interactive:
                if i > 0 and not prompt_yes_no(f"Continue with: {name}?", "yes"):
                    print_warning("Installation paused. You can resume it later.")
                    return False
            
            result = step_func()
            if not result:
                print_error(f"Installation failed at step: {name}")
                return False
        
        print_success("\nCreatureBox installation completed successfully!")
        return True
    except Exception as e:
        print_error(f"An unexpected error occurred during installation: {e}")
        return False

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    from utils import print_banner
    print_banner()
    
    interactive = len(sys.argv) <= 1 or sys.argv[1] != "--non-interactive"
    run_installation(interactive)
