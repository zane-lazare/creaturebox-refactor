#!/bin/bash
# CreatureBox Installation Script - Simplified Version

# Set script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${SCRIPT_DIR}/install"
LOG_FILE="${HOME}/creaturebox_install.log"

# Function to run pre-installation checks
run_pre_checks() {
    echo "Running Pre-Installation Checks..."
    python3 "${INSTALL_DIR}/pre_check.py"
    return $?
}

# Function to run installation
run_install() {
    echo "Running Installation..."
    python3 "${INSTALL_DIR}/installer.py" $1
    return $?
}

# Function to run verification
run_verify() {
    echo "Verifying Installation..."
    python3 "${INSTALL_DIR}/verifier.py"
    return $?
}

# Parse command line arguments
if [ "$1" = "--help" ]; then
    echo "Usage: $0 [OPTIONS]"
    echo "OPTIONS:"
    echo "  --help              Show this help message"
    echo "  --check-only        Only run pre-installation checks"
    echo "  --install-only      Skip checks and proceed with installation"
    echo "  --verify-only       Only verify an existing installation"
    echo "  --non-interactive   Run in non-interactive mode (use defaults)"
    exit 0
elif [ "$1" = "--check-only" ]; then
    run_pre_checks
    exit $?
elif [ "$1" = "--verify-only" ]; then
    run_verify
    exit $?
elif [ "$1" = "--install-only" ]; then
    run_install
    exit $?
else
    # Run full installation process
    echo "Starting CreatureBox installation process..."
    
    # Create log file directory
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting CreatureBox installation" > "$LOG_FILE"
    
    # Run pre-installation checks
    if ! run_pre_checks; then
        echo "Pre-installation checks failed."
        
        if [ "$1" != "--non-interactive" ]; then
            read -p "Continue anyway? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        else
            exit 1
        fi
    fi
    
    # Run installation
    INSTALL_ARG=""
    if [ "$1" = "--non-interactive" ]; then
        INSTALL_ARG="--non-interactive"
    fi
    
    if ! run_install "$INSTALL_ARG"; then
        echo "Installation failed. Check log: $LOG_FILE"
        exit 1
    fi
    
    # Run verification
    if ! run_verify; then
        echo "Verification failed. Check log: $LOG_FILE"
        exit 1
    fi
    
    echo "CreatureBox has been successfully installed!"
    exit 0
fi