import time
import sys
import os
import logging
from datetime import datetime
from pathlib import Path
import traceback

# Set up logging for the background script
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
bg_log_path = log_dir / "background_carousell_scraper.log"
logging.basicConfig(filename=bg_log_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Write PID to file
pid_file = Path(__file__).parent / "carousell_scraper.pid"
with open(pid_file, 'w') as f:
    f.write(str(os.getpid()))

logging.info(f"Background script started. PID: {os.getpid()}")

# Add the directory containing the original script to Python's path
sys.path.append(os.path.dirname(__file__))

try:
    # Import the main function from your original script
    from carousell_scraper import main
    logging.info("Successfully imported main function from carousell_scraper")
except Exception as e:
    logging.error(f"Failed to import main function: {str(e)}")
    logging.error(traceback.format_exc())
    sys.exit(1)

if __name__ == '__main__':
    while True:
        try:
            logging.info("Starting Carousell scraper iteration")
            main()
            logging.info("Finished Carousell scraper iteration")
            # Sleep for 1 hour
            logging.info("Sleeping for 1 hour")
            for _ in range(60):  # Check every minute if we should continue
                time.sleep(60)
                if not os.path.exists(pid_file):
                    logging.info("PID file not found. Exiting.")
                    sys.exit(0)
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            logging.error(traceback.format_exc())
            time.sleep(60)  # Wait for 1 minute before retrying
