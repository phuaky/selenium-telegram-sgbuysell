import os
import psutil
from pathlib import Path

PID_FILE = Path(__file__).parent / "carousell_scraper.pid"


def check_scraper_status():
    if PID_FILE.exists():
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        try:
            process = psutil.Process(pid)
            if process.is_running():
                print(f"Carousell scraper is running (PID: {pid})")
                print(f"Process name: {process.name()}")
                print(f"Started at: {process.create_time()}")
                return
        except psutil.NoSuchProcess:
            pass

    print("Carousell scraper is not running")


if __name__ == "__main__":
    check_scraper_status()
