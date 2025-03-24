import subprocess
import sys
import os
import importlib.util

# Paths to the three extraction scripts (same folder)
SCRIPT_V1 = "extractv1.py"
SCRIPT_V2 = "extractv2.py"
SCRIPT_V3 = "extractv3.py"

def check_dependencies():
    """Check for required Python libraries and system tools."""
    print("Running dependency check...")

    # Check Python version
    if sys.version_info.major < 3:
        print("Error: Python 3.x is required. Current version:", sys.version)
        return False

    # Check for requests library
    if importlib.util.find_spec("requests") is None:
        print("Error: 'requests' library is not installed.")
        print("Install it with: pip install requests (or pip3 install requests)")
        return False

    # Check script files exist
    for script in [SCRIPT_V1, SCRIPT_V2, SCRIPT_V3]:
        if not os.path.exists(script):
            print(f"Error: {script} not found in the current directory!")
            return False

    # Check system-specific tools
    if sys.platform == "linux" or sys.platform == "linux2":
        try:
            subprocess.run(["which", "xterm"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print("Error: 'xterm' is not installed on Linux.")
            print("Install it with: sudo apt-get install xterm (Ubuntu/Debian) or equivalent for your distro")
            return False

    print("All dependencies satisfied.")
    return True

def run_in_terminal(script_path):
    """Run a Python script in a new terminal window."""
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found!")
        return
    
    # Platform-specific terminal commands
    if sys.platform == "win32":  # Windows
        cmd = f'start cmd /k python "{script_path}"'
    elif sys.platform == "darwin":  # macOS
        cmd = f'osascript -e \'tell app "Terminal" to do script "python3 {script_path}"\''
    elif sys.platform == "linux" or sys.platform == "linux2":  # Linux
        cmd = f'xterm -e python3 "{script_path}"'
    else:
        print(f"Unsupported platform: {sys.platform}")
        return
    
    try:
        subprocess.Popen(cmd, shell=True)
        print(f"Launched {script_path} in a new terminal.")
    except Exception as e:
        print(f"Failed to launch {script_path}: {e}")

def main():
    # Run dependency check
    if not check_dependencies():
        print("Dependency check failed. Please resolve issues and try again.")
        sys.exit(1)
    
    print("\nStarting all extraction scripts in separate terminals...")
    
    # Run each script in a new terminal
    run_in_terminal(SCRIPT_V1)
    run_in_terminal(SCRIPT_V2)
    run_in_terminal(SCRIPT_V3)
    
    print("All scripts launched. Check the terminals for output.")

if __name__ == "__main__":
    main()