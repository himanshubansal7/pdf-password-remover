#!/usr/bin/env python3
"""
Fetch stock distribution data from Tiingo API
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TiingoDistributionFetcher:
    BASE_URL = "https://api.tiingo.com/tiingo/corporate-actions"
    
    def __init__(self):
        self.token = os.getenv('TIINGO_API_TOKEN')
        if not self.token:
            raise ValueError("TIINGO_API_TOKEN not found in .env file")
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with headers"""
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Token {self.token}'
        })
        return session
    
    def fetch_distributions(self, tickers: List[str], start_date: str) -> Dict[str, Any]:
        """
        Fetch distributions for multiple tickers
        
        Args:
            tickers: List of stock ticker symbols
            start_date: Start date in YYYY-MM-DD format
            
        Returns:
            Dictionary with ticker data and any errors
        """
        results = {}
        errors = {}
        
        for ticker in tickers:
            try:
                # Build URL
                url = f"{self.BASE_URL}/{ticker}/distributions?startExDate={start_date}"
                
                # Make request
                response = self.session.get(url)
                response.raise_for_status()
                
                results[ticker] = response.json()
                
            except requests.exceptions.RequestException as e:
                errors[ticker] = str(e)
        
        return {
            'results': results,
            'errors': errors
        }

def main():
    # Example usage
    if len(sys.argv) < 2:
        print("Usage: python distribution_fetcher.py <ticker1> <ticker2> ... [--date YYYY-MM-DD]")
        sys.exit(1)
    
    # Parse arguments
    tickers = []
    start_date = None
    
    for arg in sys.argv[1:]:
        if arg == '--date' or arg == '-d':
            idx = sys.argv.index(arg)
            start_date = sys.argv[idx + 1]
        elif not arg.startswith('-'):
            tickers.append(arg.upper())
    
    # Default to 1 year ago if not specified
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    try:
        fetcher = TiingoDistributionFetcher()
        data = fetcher.fetch_distributions(tickers, start_date)
        
        print(json.dumps(data, indent=2))
        
    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
