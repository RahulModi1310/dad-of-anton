"""
Configuration for Screener.in Scraper
======================================
Add/remove indexes and data points here.
"""

import os

BASE_URL = "https://www.screener.in"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Index configurations: name -> URL slug
INDEXES = {
    "SMALLCAP50": "SMALLCAP50",
    "LMIDCAP250": "LMIDCAP250",
    "NIF500MO50": "NIF500MO50",
}

# Request settings
REQUEST_DELAY = 1.5  # seconds between requests (be polite)
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3

# Pagination
RESULTS_PER_PAGE = 25  # screener.in default

# Data points to scrape from company pages
# Format: (label, selector_type, selector_value)
# selector_type: "ratio" = fuzzy match from #top-ratios li elements
#               "ratio_exact" = exact match from #top-ratios li elements
#               "quarterly" = latest quarter value from #quarters table
#               "shareholding" = from #shareholding table
#               "pros_cons" = from #analysis section
COMPANY_DATA_POINTS = [
    # Default ratios on company pages
    ("Market Cap", "ratio", "Market Cap"),
    ("Current Price", "ratio", "Current Price"),
    ("High / Low", "ratio", "High / Low"),
    ("Stock P/E", "ratio", "Stock P/E"),
    ("Book Value", "ratio", "Book Value"),
    ("Dividend Yield", "ratio", "Dividend Yield"),
    ("ROCE", "ratio", "ROCE"),
    ("ROE", "ratio", "ROE"),
    ("Face Value", "ratio", "Face Value"),
    # Quarterly results (latest quarter)
    ("Sales (Latest Qtr)", "quarterly", "Sales"),
    ("Operating Profit (Latest Qtr)", "quarterly", "Operating Profit"),
    ("Net Profit (Latest Qtr)", "quarterly", "Net Profit"),
    # Shareholding pattern
    ("Promoter Holding", "shareholding", "Promoter"),
    ("FII Holding", "shareholding", "FII"),
    ("DII Holding", "shareholding", "DII"),
    ("Public Holding", "shareholding", "Public"),
    ("Government Holding", "shareholding", "Government"),
    ("Others Holding", "shareholding", "Others"),
    # Pros/Cons
    ("Pros", "pros_cons", "pros"),
    ("Cons", "pros_cons", "cons"),
]

# Headers for requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}
