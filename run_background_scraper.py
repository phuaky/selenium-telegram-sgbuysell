import subprocess
import sys
import os
from pathlib import Path
import logging
from datetime import datetime
import psutil

# Set up logging for the background runner
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
runner_log_path = log_dir / "background_runner.log"
logging.basicConfig(filename=runner_log_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

PID_FILE = Path(__file__).parent / "carousell_scraper.pid"


def is_script_running():
    if PID_FILE.exists():
        with open(PID_FILE, 'r') as f:
            old_pid = int(f.read().strip())
        if psutil.pid_exists(old_pid):
            return True
    return False


def create_background_script(script_path):
    background_script = f"""
import time
import sys
import os
import logging
from datetime import datetime
from pathlib import Path

# Set up logging for the background script
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
bg_log_path = log_dir / "background_carousell_scraper.log"
logging.basicConfig(filename=bg_log_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Write PID to file
with open('{PID_FILE}', 'w') as f:
    f.write(str(os.getpid()))

# Add the directory containing the original script to Python's path
sys.path.append(os.path.dirname(r'{script_path}'))

# Import the main function from your original script
from carousell_scraper import main

if __name__ == '__main__':
    while True:
        try:
            logging.info("Starting Carousell scraper iteration")
            main()
            logging.info("Finished Carousell scraper iteration")
            # Sleep for 1 hour
            logging.info("Sleeping for 1 hour")
            time.sleep(3600)
        except Exception as e:
            logging.error(f"Error occurred: {{e}}")
            time.sleep(60)  # Wait for 1 minute before retrying
    """

    background_script_path = Path(script_path).with_name(
        'background_carousell_scraper.py')
    with open(background_script_path, 'w') as f:
        f.write(background_script)
    return background_script_path


# Set up logging for the background runner
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
runner_log_path = log_dir / "background_runner.log"
logging.basicConfig(filename=runner_log_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

PID_FILE = Path(__file__).parent / "carousell_scraper.pid"


def is_script_running():
    if PID_FILE.exists():
        with open(PID_FILE, 'r') as f:
            old_pid = int(f.read().strip())
        if psutil.pid_exists(old_pid):
            return True
    return False


def run_script_in_background(script_path):
    if is_script_running():
        print("The Carousell scraper is already running.")
        print(f"To stop it, run: python stop_scraper.py")
        return

    # Use pythonw.exe to run the script without a console window
    pythonw_path = str(Path(sys.executable).with_name('pythonw.exe'))

    try:
        # Start the background process
        process = subprocess.Popen([pythonw_path, str(script_path)],
                                   creationflags=subprocess.CREATE_NO_WINDOW,
                                   close_fds=True)

        logging.info(f"Background script started: {script_path}")
        print(f"Background script started: {script_path}")
        print("The Carousell scraper is now running in the background.")
        print(f"Process ID: {process.pid}")
        print(f"To stop it, run: python stop_scraper.py")
        print(f"Check the log files in the 'logs' directory for runtime information.")
        print(f"Runner log: {runner_log_path}")
    except Exception as e:
        logging.error(f"Failed to start background process: {e}")
        print(
            f"Error: Failed to start background process. Check {runner_log_path} for details.")


if __name__ == "__main__":
    carousell_script_path = Path(__file__).parent / \
        "background_carousell_scraper.py"

    if not carousell_script_path.exists():
        error_message = f"Error: Could not find {carousell_script_path}"
        logging.error(error_message)
        print(error_message)
        sys.exit(1)

    run_script_in_background(str(carousell_script_path))
