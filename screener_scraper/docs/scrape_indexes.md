# Script 1: scrape_indexes.py

## Purpose

Scrapes company tickers and names from screener.in index pages. Handles pagination to collect all companies across multiple pages.

## Input

- CLI argument: optional index name(s)
- Network: fetches HTML from `screener.in/company/{SLUG}/`

## Output

CSV file per index saved to `output/{INDEX}_companies.csv` with columns:

| Column | Type | Description |
|--------|------|-------------|
| ticker | string | Stock ticker symbol (e.g., RELIANCE, TCS) |
| name | string | Company display name |
| url | string | Full URL to company page on screener.in |

## CLI Interface

```
python scrape_indexes.py [index ...] [-v]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `index` | No | Index name(s). If omitted, scrapes all indexes in config. |
| `-v, --verbose` | No | Enable debug logging output. |

## Examples

```bash
# Scrape all configured indexes
python scrape_indexes.py

# Scrape single index
python scrape_indexes.py SMALLCAP50

# Scrape multiple indexes
python scrape_indexes.py SMALLCAP50 NIFTY

# Use custom slug (not in INDEXES config)
python scrape_indexes.py NIFTY50
```

## Functions

### `get_total_pages(soup) -> int`

Extracts total page count from pagination info.

- Reads `div[data-page-info]` text
- Parses pattern "X results found: Showing page Y of Z"
- Falls back to counting pagination links if primary method fails

### `extract_companies(soup) -> list[dict]`

Extracts company tickers and names from the constituents table.

- Selects all `tr[data-row-company-id]` rows
- Finds company link in `td.text a[href*='/company/']`
- Extracts ticker from URL pattern `/company/{TICKER}/`
- Returns list of dicts with `ticker`, `name`, `url`

### `scrape_index(index_name, index_slug) -> list[dict]`

Orchestrates scraping of a single index with pagination.

- Fetches page 1 to determine total pages
- Iterates through all pages
- Collects companies from each page
- Returns combined list

### `save_to_csv(companies, index_name) -> str`

Writes companies list to CSV file.

- Creates `output/` directory if needed
- Writes with UTF-8 encoding
- Returns filepath

### `main()`

Entry point.

- Parses CLI arguments
- Configures logging
- Filters indexes if specific one requested
- Iterates through indexes, calling `scrape_index` and `save_to_csv`
- Prints summary

## Extraction Logic

### Pagination Detection

```
HTML: <div data-page-info>50 results found: Showing page 1 of 2</div>
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Regex: r"of\s+(\d+)" → matches "2"
```

### Company Link Extraction

```
HTML: <a href="/company/RELIANCE/consolidated/" target="_blank">Reliance Industries</a>
                        ^^^^^^^^^^^
Regex: r"/company/([^/]+)/" → captures "RELIANCE"
```

## Dependencies

- `config.py`: BASE_URL, INDEXES, OUTPUT_DIR, REQUEST_DELAY, HEADERS
- `utils.py`: get_page()
- `requests`: HTTP requests
- `bs4`: HTML parsing
- Standard library: os, sys, csv, re, time, logging, argparse
