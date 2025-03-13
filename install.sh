#!/bin/bash
# CreatureBox Installation Script - Simplified and Robust

# Set script directory (works regardless of where the repository is cloned)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${SCRIPT_DIR}/install"
LOG_FILE="${HOME}/creaturebox_install.log"

# Installation target directories - can be overridden with environment variables
TARGET_DIR="${CREATUREBOX_HOME:-${HOME}/CreatureBox}"
VENV_PATH="${CREATUREBOX_VENV:-${HOME}/creaturebox-venv}"

# Export variables so Python scripts can use them
export CREATUREBOX_HOME="${TARGET_DIR}"
export CREATUREBOX_VENV="${VENV_PATH}"

# Function to print text
print_colored() {
    echo "$1"
}

# Function to print a section header
print_section() {
    print_colored "$1"
    print_colored "$(printf '%*s' ${#1} | tr ' ' '-')"
}

# Print the CreatureBox banner
print_banner() {
    print_colored "CreatureBox Installation"
    print_colored "----------------------"
    echo
}

# Function to check if Python is available
check_python() {
    if ! command -v python3 &>/dev/null; then
        print_colored "Python 3 is not installed or not in your PATH."
        print_colored "Please install Python 3.7 or newer and try again."
        print_colored "You can install it with: sudo apt-get update && sudo apt-get install -y python3"
        return 1
    fi
    return 0
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "OPTIONS:"
    echo "  --help              Show this help message"
    echo "  --check-only        Only run pre-installation checks"
    echo "  --install-only      Skip checks and proceed with installation"
    echo "  --verify-only       Only verify an existing installation"
    echo "  --non-interactive   Run in non-interactive mode (use defaults)"
    echo
    echo "ENVIRONMENT VARIABLES:"
    echo "  CREATUREBOX_HOME    Target installation directory (default: ~/CreatureBox)"
    echo "  CREATUREBOX_VENV    Virtual environment path (default: ~/creaturebox-venv)"
    echo
    echo "Examples:"
    echo "  $0                                  # Run full interactive installation"
    echo "  $0 --check-only                     # Only check requirements"
    echo "  CREATUREBOX_HOME=/opt/cb $0         # Install to custom location"
    echo
}

# Function to ensure directories exist
ensure_directories() {
    # Make sure installation and virtual environment directories exist
    mkdir -p "${TARGET_DIR}"
    mkdir -p "$(dirname "${VENV_PATH}")"
    
    # Create log file directory
    mkdir -p "$(dirname "$LOG_FILE")"
}

# Function to run pre-installation checks
run_pre_checks() {
    print_section "Running Pre-Installation Checks"
    
    # Run pre-check Python script
    if [ -f "${INSTALL_DIR}/pre_check.py" ]; then
        python3 "${INSTALL_DIR}/pre_check.py"
        return $?
    else
        print_colored "Pre-check script not found: ${INSTALL_DIR}/pre_check.py"
        return 1
    fi
}

# Function to run installation
run_install() {
    print_section "Running Installation"
    
    # Check if installation should be interactive
    if [ "$NON_INTERACTIVE" = "true" ]; then
        INSTALL_ARGS="--non-interactive"
    else
        INSTALL_ARGS=""
    fi
    
    # Run installer Python script
    if [ -f "${INSTALL_DIR}/installer.py" ]; then
        python3 "${INSTALL_DIR}/installer.py" $INSTALL_ARGS
        return $?
    else
        print_colored "Installer script not found: ${INSTALL_DIR}/installer.py"
        return 1
    fi
}

# Function to run verification
run_verify() {
    print_section "Verifying Installation"
    
    # Run verifier Python script
    if [ -f "${INSTALL_DIR}/verifier.py" ]; then
        python3 "${INSTALL_DIR}/verifier.py"
        return $?
    else
        print_colored "Verifier script not found: ${INSTALL_DIR}/verifier.py"
        return 1
    fi
}

# Initialize variables
CHECK_ONLY="false"
INSTALL_ONLY="false"
VERIFY_ONLY="false"
NON_INTERACTIVE="false"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            show_usage
            exit 0
            ;;
        --check-only)
            CHECK_ONLY="true"
            ;;
        --install-only)
            INSTALL_ONLY="true"
            ;;
        --verify-only)
            VERIFY_ONLY="true"
            ;;
        --non-interactive)
            NON_INTERACTIVE="true"
            ;;
        *)
            print_colored "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
    shift
done

# Print banner and installation info
print_banner
print_colored "Installation paths:"
print_colored "- Installation directory: ${TARGET_DIR}"
print_colored "- Virtual environment: ${VENV_PATH}"
echo

# Check Python availability
if ! check_python; then
    exit 1
fi

# Make sure all required directories exist
ensure_directories

# Setup Python path
export PYTHONPATH="${INSTALL_DIR}:${PYTHONPATH}"

# Log start of installation
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting CreatureBox installation" > "$LOG_FILE"
echo "- Installation directory: ${TARGET_DIR}" >> "$LOG_FILE"
echo "- Virtual environment: ${VENV_PATH}" >> "$LOG_FILE"

# Run the requested operation
if [ "$CHECK_ONLY" = "true" ]; then
    run_pre_checks
    exit $?
elif [ "$VERIFY_ONLY" = "true" ]; then
    run_verify
    exit $?
elif [ "$INSTALL_ONLY" = "true" ]; then
    run_install
    exit $?
else
    # Run full installation process
    print_colored "Starting CreatureBox installation process..."
    echo
    
    # Run pre-installation checks
    if ! run_pre_checks; then
        print_colored "Pre-installation checks failed. Please address the issues before proceeding."
        
        if [ "$NON_INTERACTIVE" = "false" ]; then
            read -p "Do you want to continue anyway? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        else
            exit 1
        fi
    fi
    
    # Run installation
    if ! run_install; then
        print_colored "Installation failed. Please check the log file: $LOG_FILE"
        exit 1
    fi
    
    # Run verification
    if ! run_verify; then
        print_colored "Verification failed. Your installation may not be complete."
        print_colored "Please check the log file: $LOG_FILE"
        exit 1
    fi
    
    # Final message
    print_colored "CreatureBox has been successfully installed!"
    print_colored "Activate the virtual environment with: source ${VENV_PATH}/bin/activate"
    print_colored "You can also use: source ~/activate_venv.sh"
    print_colored "You can now start using CreatureBox. Enjoy!"
    exit 0
fi
