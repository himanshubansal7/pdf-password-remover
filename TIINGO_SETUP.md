# Tiingo Distribution Fetcher Setup Guide

## Overview
This script fetches stock distribution data from the Tiingo API for a list of ticker symbols.

## Requirements
- Python 3.6+
- `requests` library
- `python-dotenv` library

## Installation

1. **Install dependencies:**
   ```bash
   pip install requests python-dotenv
   ```

2. **Create a .env file:**
   ```bash
   cp .env.example .env
   ```

3. **Add your Tiingo API token to .env:**
   ```
   TIINGO_API_TOKEN=your_actual_token_here
   ```

   You can get your API token from https://www.tiingo.com/account/api/token

## Usage

### Basic Usage
Fetch distribution data for one or more tickers (default: last 365 days):
```bash
python distribution_fetcher.py AAPL GOOGL MSFT
```

### With Custom Date
Specify a start date in YYYY-MM-DD format:
```bash
python distribution_fetcher.py AAPL GOOGL --date 2024-01-01
```

### Short Format
You can also use `-d` instead of `--date`:
```bash
python distribution_fetcher.py AAPL -d 2023-06-01
```

## Output

The script returns a JSON object with:
- **results**: Dictionary of successful ticker lookups with their distribution data
- **errors**: Dictionary of any errors encountered for specific tickers

Example output:
```json
{
  "results": {
    "AAPL": [
      {
        "exDate": "2024-05-10",
        "paymentDate": "2024-05-23",
        "recordDate": "2024-05-15",
        "amount": 0.25,
        "type": "Dividend"
      }
    ]
  },
  "errors": {}
}
```

## Error Handling

The script handles:
- Missing API token in .env file
- Network/connection errors
- Invalid ticker symbols
- API response errors
- Invalid date formats

Errors are logged in the `errors` section of the output.

## API Endpoint

The script calls:
```
https://api.tiingo.com/tiingo/corporate-actions/{TICKER}/distributions?startExDate={YYYY-MM-DD}
```

## Authentication

The API token is passed in the request headers:
```
Authorization: Token {TIINGO_API_TOKEN}
Content-Type: application/json
```

## Troubleshooting

### "TIINGO_API_TOKEN not found in .env file"
- Ensure `.env` file exists in the same directory as the script
- Verify the token is set: `TIINGO_API_TOKEN=your_token`

### "No module named 'dotenv'"
- Install python-dotenv: `pip install python-dotenv`

### Connection errors
- Verify your internet connection
- Check if Tiingo API is accessible
- Ensure the API token is valid

## Enhancements for Future

- Add CSV/JSON export functionality
- Implement retry logic with exponential backoff
- Add verbose logging option
- Support for additional corporate actions (splits, mergers, etc.)
- Batch processing for large ticker lists
