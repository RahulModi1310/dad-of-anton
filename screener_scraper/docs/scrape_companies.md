# Script 2: scrape_companies.py

## Purpose

Reads company tickers from CSV files (output of Script 1), fetches each company page from screener.in, and scrapes fundamental/technical data. Supports resume capability and checkpoint saves.

## Input

- CLI argument: optional index name(s)
- CSV files: `output/{INDEX}_companies.csv` (from Script 1)
- Network: fetches HTML from `screener.in/company/{TICKER}/`

## Output

CSV file per index saved to `output/{INDEX}_data.csv` with columns:

| Column | Type | Description |
|--------|------|-------------|
| Ticker | string | Stock ticker symbol |
| Company Name | string | Full company name |
| Market Cap | string | Market capitalization |
| Current Price | string | Current stock price |
| High / Low | string | 52-week high/low |
| Stock P/E | string | Price-to-earnings ratio |
| Book Value | string | Book value per share |
| Dividend Yield | string | Dividend yield percentage |
| ROCE | string | Return on capital employed |
| ROE | string | Return on equity |
| Face Value | string | Face value per share |
| Sales (Latest Qtr) | string | Latest quarter sales |
| Operating Profit (Latest Qtr) | string | Latest quarter operating profit |
| Net Profit (Latest Qtr) | string | Latest quarter net profit |
| Promoter Holding | string | Promoter shareholding % |
| FII Holding | string | Foreign institutional investor % |
| DII Holding | string | Domestic institutional investor % |
| Public Holding | string | Public shareholding % |
| Government Holding | string | Government shareholding % |
| Others Holding | string | Others shareholding % |
| Pros | string | Machine-generated pros |
| Cons | string | Machine-generated cons |
| Sector | string | Industry sector |
| Industry | string | Specific industry |
| URL | string | Company page URL |
| scraped_at | string | UTC timestamp of scrape |

## CLI Interface

```
python scrape_companies.py [index ...] [-v] [-f]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `index` | No | Index name(s). If omitted, scrapes all available. |
| `-v, --verbose` | No | Enable debug logging output. |
| `-f, --force` | No | Delete existing output and re-scrape from scratch. |

## Examples

```bash
# Scrape all indexes
python scrape_companies.py

# Scrape single index
python scrape_companies.py SMALLCAP50

# Force re-scrape
python scrape_companies.py --force SMALLCAP50

# Verbose output
python scrape_companies.py -v SMALLCAP50
```

## Functions

### `extract_ratio_value(soup, ratio_name) -> str`

Fuzzy matches a ratio from `#top-ratios` section.

- Iterates through all `li` elements in `#top-ratios`
- Matches if `ratio_name` is contained in the ratio's name (case-insensitive)
- Extracts value from `.number` span or full `.value` span
- Returns string value or empty string

### `extract_ratio_value_by_exact(soup, ratio_name) -> str`

Exact matches a ratio from `#top-ratios` section.

- Same logic as fuzzy match but requires exact string equality

### `extract_quarterly_value(soup, row_name) -> str`

Extracts latest quarter value from `#quarters` table.

- Finds table within `#quarters` section
- Iterates rows, matches `row_name` in first `td` (case-insensitive)
- Returns last non-empty cell (latest quarter)

### `extract_shareholding(soup, category) -> str`

Extracts shareholding percentage from `#shareholding` table.

- Finds table within `#shareholding` section
- Iterates rows, matches `category` in first `td` (case-insensitive)
- Returns last cell value (latest quarter)

### `extract_pros_cons(soup) -> tuple[str, str]`

Extracts pros and cons from `#analysis` section.

- Reads `.pros ul li` items
- Reads `.cons ul li` items
- Returns tuple of (pros_text, cons_text) joined by " | "

### `extract_company_data(soup) -> dict`

Main extraction function. Calls all extractors based on `COMPANY_DATA_POINTS` config.

- Iterates through configured data points
- Routes to appropriate extractor based on `selector_type`
- Adds company name from `h1` tag
- Adds sector/industry from `#peers a[href*='/market/']`
- Returns complete data dict

### `scrape_company(ticker, url) -> dict | None`

Scrapes a single company page.

- Calls `get_page()` to fetch HTML
- Calls `extract_company_data()` to parse
- Adds ticker, URL, timestamp
- Validates numeric fields
- Logs failed tickers to `_failed_tickers.csv`

### `load_scraped_tickers(index_name) -> set[str]`

Loads tickers already scraped from existing output CSV.

- Returns empty set if no file exists
- Used for resume capability

### `scrape_index_companies(csv_path, index_name, seen_tickers) -> list[dict]`

Scrapes all companies from an index CSV, skipping already-scraped ones.

- Merges with `seen_tickers` for cross-index deduplication
- Loads existing data for checkpoint append
- Uses tqdm progress bar
- Checkpoints every 10 companies

### `save_company_data(data, index_name, dry_run=False)`

Saves company data to CSV.

- Dynamically builds column list from all records
- Ensures consistent column order
- Returns filepath

### `main()`

Entry point.

- Parses CLI arguments
- Configures logging
- Finds all `_companies.csv` files
- Filters by index if specified
- Handles `--force` flag
- Tracks seen tickers for deduplication
- Prints summary with timing

## Extraction Logic

### Ratio Extraction (Top Ratios)

```
HTML: <li class="flex flex-space-between">
        <span class="name">Market Cap</span>
        <span class="nowrap value">
          ₹ <span class="number">17,62,411</span> Cr.
        </span>
      </li>

Selector: #top-ratios li
Match: .name text contains "Market Cap"
Value: .number text = "17,62,411"
```

### Quarterly Table Extraction

```
HTML: <section id="quarters">
        <table>
          <tr>
            <td>Sales</td>
            <td>207,559</td>
            <td>231,886</td>
            ... (13 quarters)
          </tr>
        </table>
      </section>

Selector: #quarters table
Row match: First td contains "Sales" (case-insensitive)
Value: Last non-empty td = latest quarter
```

### Shareholding Extraction

```
HTML: <section id="shareholding">
        <table>
          <tr>
            <td><button>Promoters +</button></td>
            <td>50.27%</td>
            <td>50.30%</td>
            ... (12 quarters)
          </tr>
        </table>
      </section>

Selector: #shareholding table
Row match: First td contains "Promoters"
Value: Last td = latest quarter
```

### Pros/Cons Extraction

```
HTML: <section id="analysis">
        <div class="pros"><ul>
          <li>Good dividend history</li>
        </ul></div>
        <div class="cons"><ul>
          <li>Low ROE</li>
        </ul></div>
      </section>

Selector: .pros ul li, .cons ul li
Join: " | " separator
```

### Sector/Industry Extraction

```
HTML: <section id="peers">
        <a href="/market/IN03/">Energy</a>
        <a href="/market/IN03/IN0301/">Oil, Gas & Consumable Fuels</a>
      </section>

Selector: #peers a[href*='/market/']
Sector: First link text
Industry: Last link text
```

## Dependencies

- `config.py`: BASE_URL, OUTPUT_DIR, REQUEST_DELAY, COMPANY_DATA_POINTS
- `utils.py`: get_page()
- `requests`: HTTP requests
- `bs4`: HTML parsing
- `tqdm`: Progress bar
- Standard library: os, sys, csv, re, time, logging, argparse, datetime
