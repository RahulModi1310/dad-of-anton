# Screener.in Scraper

Scrapes stock market data from [screener.in](https://www.screener.in) for Indian stock indexes. Extracts company tickers from index pages, then scrapes fundamental/technical data for each company.

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

```bash
cd screener_scraper
pip install -r requirements.txt
```

### First Run

```bash
# Step 1: Scrape company tickers from index pages
python scrape_indexes.py

# Step 2: Scrape detailed data for each company
python scrape_companies.py
```

Or use the convenience scripts:

```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

Output files will be saved in the `output/` directory.

## Usage

### Scrape Specific Index

```bash
python scrape_indexes.py SMALLCAP50
python scrape_companies.py SMALLCAP50
```

### Scrape Multiple Indexes

```bash
python scrape_indexes.py SMALLCAP50 NIFTY
python scrape_companies.py SMALLCAP50 NIFTY
```

### Force Re-scrape

```bash
python scrape_companies.py --force SMALLCAP50
```

### Verbose Output

```bash
python scrape_companies.py -v SMALLCAP50
```

### Run Both Scripts

```bash
./run.sh SMALLCAP50
```

## CLI Arguments

| Script | Argument | Description |
|--------|----------|-------------|
| Both | `index` | Index name(s) to scrape. Omit for all. |
| Both | `-v, --verbose` | Enable debug logging |
| scrape_companies | `-f, --force` | Re-scrape even if output exists |

## Output

Output files are saved in `output/`:

| File | Description |
|------|-------------|
| `{INDEX}_companies.csv` | Company tickers and names |
| `{INDEX}_data.csv` | Detailed fundamental data |

## Configuration

Edit `config.py` to:

- Add new indexes (see `INDEXES` dict)
- Change data points (see `COMPANY_DATA_POINTS` list)
- Adjust request settings (delay, timeout, retries)

See [docs/config_reference.md](docs/config_reference.md) for full reference.

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/architecture.md) | System design and data flow |
| [Scrape Indexes](docs/scrape_indexes.md) | Script 1 specification |
| [Scrape Companies](docs/scrape_companies.md) | Script 2 specification |
| [Config Reference](docs/config_reference.md) | All configuration parameters |
| [Data Model](docs/data_model.md) | CSV columns and HTML selectors |
| [Proposed Changes](docs/proposed_changes.md) | XLSX migration plan |

## Troubleshooting

### "No index CSV files found"

Run Script 1 first: `python scrape_indexes.py`

### "Rate limited (429)"

The scraper handles this automatically with 30s wait. If persistent, increase `REQUEST_DELAY` in config.py.

### Failed tickers

Check `output/_failed_tickers.csv` for a list of companies that failed to scrape. Re-run with `--force` to retry.

### Empty data fields

Some ratios only appear on screener.in with a premium account or custom "Edit ratios" settings. See [docs/data_model.md](docs/data_model.md) for which fields may be empty.
