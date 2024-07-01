# Carousell Scraper

This project is a background-running web scraper for Carousell listings. It periodically checks for new listings based on specified search criteria and notifies you via Telegram.

## Table of Contents
- [Carousell Scraper](#carousell-scraper)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
    - [Adding a New Search URL](#adding-a-new-search-url)
    - [Removing Unwanted Items from Config](#removing-unwanted-items-from-config)
  - [Running the Scraper](#running-the-scraper)
  - [Managing the Scraper](#managing-the-scraper)
    - [Stopping the Scraper](#stopping-the-scraper)
    - [Checking Scraper Status](#checking-scraper-status)
  - [Checking Logs](#checking-logs)
  - [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.7+
- Chrome browser
- Windows 10

## Installation

1. Clone this repository or download the scripts to your local machine.

2. Install the required Python packages:

   ```
   pip install selenium webdriver_manager openpyxl psutil telebot
   ```

## Configuration

The scraper uses a `config.json` file for its settings. If it doesn't exist, create one in the same directory as the scripts with the following structure:

```json
{
  "TELEGRAM_BOT_TOKEN": "your_telegram_bot_token",
  "TELEGRAM_CHAT_ID": "your_telegram_chat_id",
  "BASE_URL": "https://www.carousell.sg/",
  "MAX_RETRIES": 3,
  "WAIT_TIME": 20,
  "MAX_LISTINGS_TO_SCRAPE": 48,
  "SEARCH_ITEMS": []
}
```

Replace `your_telegram_bot_token` and `your_telegram_chat_id` with your actual Telegram bot token and chat ID.

### Adding a New Search URL

To add a new search URL to the config:

1. Run the following command:

   ```
   python add_search_url.py
   ```

2. When prompted, paste the Carousell search URL.
3. The script will parse the URL, add the search parameters to your `config.json` file, and display the details of the added search item.

This process makes it easy to add new search criteria directly from Carousell search results.

### Removing Unwanted Items from Config

To remove items from the `SEARCH_ITEMS` list in the config:

1. Open `config.json` in a text editor.
2. Locate the `SEARCH_ITEMS` array.
3. Remove the entire object (enclosed in curly braces `{}`) for the search item you want to delete.
4. Save the file.

Example:
```json
"SEARCH_ITEMS": [
  {
    "category": "5704",
    "query": "apple pencil gen 1",
    "sort_by": 3,
    "price_start": 30,
    "price_end": 145,
    "tab": null
  },
  // Remove this object to delete this search item
  {
    "category": "1234",
    "query": "unwanted item",
    "sort_by": 3,
    "price_start": 10,
    "price_end": 100,
    "tab": null
  }
]
```

## Running the Scraper

The scraper runs as a background process and checks for new listings every hour.

To start the scraper:

```
python run_background_scraper.py
```

This will start the scraper process in the background. It will create a PID file and log files in a `logs` directory.

## Managing the Scraper

### Stopping the Scraper

To stop the scraper:

```
python stop_scraper.py
```

This will terminate the background scraper process.

### Checking Scraper Status

To check if the scraper is currently running:

```
python check_scraper_status.py
```

This will tell you whether the scraper is active or not, and provide additional information such as the process ID, name, and start time if it is running.

## Checking Logs

Log files are created in the `logs` directory:

- `background_runner.log`: Logs from the script that starts the background process
- `background_carousell_scraper.log`: Logs from the background scraper process
- `carousell_scraper.log`: Detailed logs of each scraping operation

You can view logs in real-time using PowerShell:

```powershell
Get-Content .\logs\background_carousell_scraper.log -Wait
```

## Troubleshooting

1. If the scraper doesn't start, check the `background_runner.log` for any error messages.
2. If you're not receiving Telegram notifications, verify your bot token and chat ID in the `config.json` file.
3. If the script crashes unexpectedly, check the `carousell_scraper.log` for detailed error information.
4. Ensure that Chrome browser is installed and up to date.
5. If you encounter issues with Selenium, try updating the `webdriver_manager` package:
   ```
   pip install --upgrade webdriver_manager
   ```
6. If you're unsure about the scraper's status, use the `check_scraper_status.py` script to get current information.

For any persistent issues, check the 'Issues' section of the project repository or create a new issue with a detailed description of the problem.