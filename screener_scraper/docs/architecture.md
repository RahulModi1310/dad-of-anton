# Architecture

## Overview

The scraper operates in two stages:

1. **Script 1** (`scrape_indexes.py`) — Scrapes index pages to get company tickers
2. **Script 2** (`scrape_companies.py`) — Scrapes each company page for detailed data

## System Diagram

```
screener.in Index Page
        |
        v
+---------------------+
| scrape_indexes.py   |
| - Fetches paginated |
|   index pages       |
| - Extracts company  |
|   tickers & names   |
+---------------------+
        |
        v
output/{INDEX}_companies.csv
        |
        v
+---------------------+
| scrape_companies.py |
| - Reads CSV         |
| - Fetches each      |
|   company page      |
| - Extracts ratios,  |
|   quarterly, etc.   |
+---------------------+
        |
        v
output/{INDEX}_data.csv
```

## File Structure

```
screener_scraper/
├── README.md                 # Quick start + usage
├── docs/                     # Documentation
│   ├── architecture.md       # This file
│   ├── scrape_indexes.md     # Script 1 spec
│   ├── scrape_companies.md   # Script 2 spec
│   ├── config_reference.md   # Config parameters
│   ├── data_model.md         # CSV columns + selectors
│   └── proposed_changes.md   # XLSX migration plan
├── config.py                 # All configuration
├── utils.py                  # Shared utilities
├── scrape_indexes.py         # Script 1
├── scrape_companies.py       # Script 2
├── run.sh / run.bat          # Run both scripts
├── requirements.txt          # Dependencies
└── output/                   # Generated CSVs (gitignored)
    ├── {INDEX}_companies.csv
    ├── {INDEX}_data.csv
    └── _failed_tickers.csv
```

## Module Dependencies

```
config.py
    |
    +---> utils.py (uses REQUEST_DELAY, REQUEST_TIMEOUT, etc.)
    |         |
    |         +---> scrape_indexes.py (imports get_page)
    |         |
    |         +---> scrape_companies.py (imports get_page)
    |
    +---> scrape_indexes.py (imports INDEXES, OUTPUT_DIR, etc.)
    |
    +---> scrape_companies.py (imports COMPANY_DATA_POINTS, OUTPUT_DIR, etc.)
```

## Data Flow Detail

### Script 1 Flow

1. Parse CLI args (optional index filter)
2. For each index:
   - Fetch page 1 from `screener.in/company/{SLUG}/`
   - Parse pagination: extract total pages from `div[data-page-info]`
   - For each page:
     - Extract company rows from `tr[data-row-company-id]`
     - Parse ticker from `a[href*='/company/']` link
     - Append to list
3. Write CSV with columns: `ticker, name, url`

### Script 2 Flow

1. Parse CLI args (optional index filter, --force, --verbose)
2. Find all `*_companies.csv` files in output/
3. For each index CSV:
   - Load tickers already scraped (for resume)
   - Load existing data (for checkpoint append)
   - For each remaining company:
     - Fetch company page from screener.in
     - Extract ratios from `#top-ratios`
     - Extract quarterly data from `#quarters table`
     - Extract shareholding from `#shareholding table`
     - Extract pros/cons from `#analysis`
     - Extract sector/industry from `#peers`
     - Append to data list
     - Checkpoint every 10 companies
4. Write CSV with all extracted columns

## Rate Limiting

- Default delay: 1.5 seconds between requests
- Exponential backoff on failure: 1.5s, 3s, 6s, 12s
- 30 second wait on 429 (rate limit) responses
- Session reuse for connection pooling

## Error Handling

- Failed requests logged to `output/_failed_tickers.csv`
- Resume capability: re-run skips already-scraped tickers
- Checkpoint saves every 10 companies prevent data loss
- 429 rate limit responses handled with extended wait
