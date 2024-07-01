import os
import psutil
from pathlib import Path
import logging

# Set up logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
stop_log_path = log_dir / "stop_scraper.log"
logging.basicConfig(filename=stop_log_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

PID_FILE = Path(__file__).parent / "carousell_scraper.pid"


def stop_scraper():
    if PID_FILE.exists():
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        try:
            process = psutil.Process(pid)
            process.terminate()
            message = f"Stopped Carousell scraper process (PID: {pid})"
            print(message)
            logging.info(message)
            os.remove(PID_FILE)
        except psutil.NoSuchProcess:
            message = f"No process found with PID {pid}"
            print(message)
            logging.warning(message)
            os.remove(PID_FILE)
    else:
        message = "No running Carousell scraper found (PID file does not exist)"
        print(message)
        logging.info(message)


if __name__ == "__main__":
    stop_scraper()
    print(f"Check {stop_log_path} for detailed log information.")
