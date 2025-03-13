#!/bin/bash
# CreatureBox Uninstall Script

# Set default paths (same as in the install script)
TARGET_DIR="${CREATUREBOX_HOME:-${HOME}/CreatureBox}"
VENV_PATH="${CREATUREBOX_VENV:-${HOME}/creaturebox-venv}"
ACTIVATE_SCRIPT="${HOME}/activate_venv.sh"
LOG_FILE="${HOME}/creaturebox_uninstall.log"

# Function to print colored text
print_colored() {
    echo "$1"
}

# Function to print section header
print_section() {
    print_colored "$1"
    print_colored "$(printf '%*s' ${#1} | tr ' ' '-')"
}

# Print banner
print_section "CreatureBox Uninstall Script"
echo

# Create log file
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting CreatureBox uninstallation" > "$LOG_FILE"
echo "- Target directory: ${TARGET_DIR}" >> "$LOG_FILE"
echo "- Virtual environment: ${VENV_PATH}" >> "$LOG_FILE"

# Confirm uninstallation
read -p "Are you sure you want to uninstall CreatureBox? All data will be lost. (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_colored "Uninstallation cancelled."
    exit 0
fi

# Check if running with sudo (needed for some operations)
if [ "$EUID" -ne 0 ]; then
    print_colored "Some operations may require sudo privileges. You might be prompted for your password."
fi

# Stop services
print_section "Stopping CreatureBox services"
if [ -f /etc/systemd/system/creaturebox-web.service ]; then
    sudo systemctl stop creaturebox-web.service
    sudo systemctl disable creaturebox-web.service
    print_colored "✓ CreatureBox web service stopped and disabled"
fi

# Remove nginx configuration
print_section "Removing nginx configuration"
if [ -f /etc/nginx/sites-enabled/creaturebox ]; then
    sudo rm -f /etc/nginx/sites-enabled/creaturebox
    print_colored "✓ Removed nginx symlink"
fi

if [ -f /etc/nginx/sites-available/creaturebox ]; then
    sudo rm -f /etc/nginx/sites-available/creaturebox
    print_colored "✓ Removed nginx configuration"
fi

# Restart nginx to apply changes
if command -v nginx &>/dev/null; then
    sudo systemctl restart nginx
    print_colored "✓ Restarted nginx"
fi

# Remove systemd service
print_section "Removing systemd service"
if [ -f /etc/systemd/system/creaturebox-web.service ]; then
    sudo rm -f /etc/systemd/system/creaturebox-web.service
    sudo systemctl daemon-reload
    print_colored "✓ Removed systemd service"
fi

# Remove virtual environment
print_section "Removing virtual environment"
if [ -d "$VENV_PATH" ]; then
    rm -rf "$VENV_PATH"
    print_colored "✓ Removed virtual environment at $VENV_PATH"
fi

# Remove activation script
if [ -f "$ACTIVATE_SCRIPT" ]; then
    rm -f "$ACTIVATE_SCRIPT"
    print_colored "✓ Removed activation script"
fi

# Remove installed files
print_section "Removing installed files"
if [ -d "$TARGET_DIR" ]; then
    rm -rf "$TARGET_DIR"
    print_colored "✓ Removed installation directory at $TARGET_DIR"
fi

# Check for any remaining files that might have been added outside the standard locations
EXTRA_FILES=(
    "/etc/cron.d/creaturebox"
)

for file in "${EXTRA_FILES[@]}"; do
    if [ -f "$file" ]; then
        sudo rm -f "$file"
        print_colored "✓ Removed $file"
    fi
done

# Check for entries in crontab
print_section "Checking for crontab entries"
CRON_ENTRIES=$(crontab -l 2>/dev/null | grep -c "CreatureBox")
if [ "$CRON_ENTRIES" -gt 0 ]; then
    print_colored "! Found $CRON_ENTRIES CreatureBox entries in crontab"
    print_colored "  You may want to edit your crontab with: crontab -e"
    echo "Found CreatureBox entries in crontab. Manual removal may be required." >> "$LOG_FILE"
fi

# Cleanup temp files
if [ -f "/tmp/creaturebox_temp.conf" ]; then
    rm -f /tmp/creaturebox_temp.conf
fi

# Final message
print_section "Uninstallation Complete"
print_colored "CreatureBox has been uninstalled from your system."
print_colored "Log file has been saved to: $LOG_FILE"

exit 0