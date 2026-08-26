# Configuration Reference

All configuration is in `config.py`.

## Base Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `BASE_URL` | `"https://www.screener.in"` | Base URL for screener.in |
| `OUTPUT_DIR` | `./output` | Directory for output CSVs |

## Indexes

```python
INDEXES = {
    "SMALLCAP50": "SMALLCAP50",
    "LMIDCAP250": "LMIDCAP250",
    "NIF500MO50": "NIF500MO50",
}
```

| Key | Value | Description |
|-----|-------|-------------|
| Key | string | Output CSV name (e.g., `SMALLCAP50_data.csv`) |
| Value | string | URL slug from screener.in (part after `/company/`) |

### Adding a New Index

1. Find the index URL on screener.in (e.g., `screener.in/company/NIFTY50/`)
2. Add to `INDEXES` dict:
   ```python
   INDEXES = {
       ...,
       "NIFTY50": "NIFTY50",
   }
   ```
3. Run: `python scrape_indexes.py NIFTY50`

**Note:** You can also pass any slug directly without adding to config:
```bash
python scrape_indexes.py NIFTY50
```

## Request Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `REQUEST_DELAY` | `1.5` | Seconds between requests (polite crawling) |
| `REQUEST_TIMEOUT` | `30` | Seconds before request timeout |
| `MAX_RETRIES` | `3` | Maximum retry attempts per request |

### Rate Limiting Behavior

- Default: 1.5s delay between requests
- On failure: exponential backoff (1.5s, 3s, 6s, 12s)
- On 429 response: 30s wait before retry

## Pagination

| Parameter | Default | Description |
|-----------|---------|-------------|
| `RESULTS_PER_PAGE` | `25` | Results per page on screener.in |

**Note:** This is a reference value. The scraper reads the actual page count from the HTML.

## Data Points

```python
COMPANY_DATA_POINTS = [
    ("Market Cap", "ratio", "Market Cap"),
    ("Current Price", "ratio", "Current Price"),
    ...
]
```

| Index | Type | Description |
|-------|------|-------------|
| 0 | string | Output column label |
| 1 | string | Extraction method (see below) |
| 2 | string | Selector value (ratio name, row name, etc.) |

### Selector Types

| Type | Description | Source |
|------|-------------|--------|
| `"ratio"` | Fuzzy match from top ratios | `#top-ratios li` |
| `"ratio_exact"` | Exact match from top ratios | `#top-ratios li` |
| `"quarterly"` | Latest quarter value | `#quarters table` |
| `"shareholding"` | Shareholding percentage | `#shareholding table` |
| `"pros_cons"` | Pros or cons text | `#analysis` |

### Adding a New Data Point

1. Identify the section on the company page
2. Find the exact row/ratio name
3. Add to `COMPANY_DATA_POINTS`:
   ```python
   COMPANY_DATA_POINTS = [
       ...,
       ("New Metric", "ratio", "Exact Ratio Name"),
   ]
   ```

### Available Ratios (Default)

These are guaranteed to exist on any company page:

- Market Cap
- Current Price
- High / Low
- Stock P/E
- Book Value
- Dividend Yield
- ROCE
- ROE
- Face Value

**Note:** Other ratios (EPS, Debt to Equity, EV/EBITDA, etc.) must be added via "Edit ratios" on screener.in account first.

### Quarterly Row Names

These match rows in `#quarters` table:

- Sales
- Expenses
- Operating Profit
- Other Income
- Interest
- Depreciation
- Net Profit
- EPS in Rs
- Dividend Payout %

### Shareholding Categories

These match rows in `#shareholding` table:

- Promoters
- FIIs
- DIIs
- Public
- Government
- Others

## Request Headers

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 ...",
    "Accept": "text/html,...",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}
```

**Note:** Changing `User-Agent` may affect response behavior. Keep as browser-like string.
