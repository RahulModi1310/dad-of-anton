# Proposed Changes: XLSX Migration

## Overview

Migrate from flat CSV output to Excel (.xlsx) with multiple sheets per stock. Each stock gets its own folder containing a single Excel file with organized data sheets.

## Current vs New Output Structure

### Current

```
output/
├── SMALLCAP50_companies.csv
├── SMALLCAP50_data.csv
├── LMIDCAP250_companies.csv
├── LMIDCAP250_data.csv
├── NIF500MO50_companies.csv
├── NIF500MO50_data.csv
└── _failed_tickers.csv
```

### Proposed

```
output/
├── SMALLCAP50/
│   ├── RELIANCE/
│   │   └── RELIANCE.xlsx
│   ├── TATAMOTORS/
│   │   └── TATAMOTORS.xlsx
│   ├── HDFCBANK/
│   │   └── HDFCBANK.xlsx
│   └── ...
├── LMIDCAP250/
│   └── ...
└── NIF500MO50/
    └── ...
```

## Excel File Structure

Each `{TICKER}.xlsx` contains 4 sheets:

### Sheet 1: Summary

Latest values + growth metrics. One row per stock.

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| Ticker | string | RELIANCE | Stock ticker |
| Company Name | string | Reliance Industries Ltd | Full company name |
| Sector | string | Energy | Industry sector |
| Industry | string | Refineries & Marketing | Specific industry |
| Market Cap | number | 1762411 | In Rs. Crores |
| Current Price | number | 1298 | In Rs. |
| Stock P/E | number | 23.6 | Price-to-earnings |
| Book Value | number | 668 | Per share |
| Dividend Yield | number | 0.46 | Percentage |
| ROCE | number | 10.3 | Percentage |
| ROE | number | 8.91 | Percentage |
| Face Value | number | 10 | Per share |
| Sales (Latest Qtr) | number | 309468 | In Rs. Crores |
| Sales (QoQ %) | number | 18.2 | Quarter-over-quarter growth |
| Sales (YoY %) | number | 29.7 | Year-over-year growth |
| Operating Profit (Latest Qtr) | number | 42246 | In Rs. Crores |
| Operating Profit (QoQ %) | number | 15.1 | QoQ growth |
| Operating Profit (YoY %) | number | 22.3 | YoY growth |
| Net Profit (Latest Qtr) | number | 18540 | In Rs. Crores |
| Net Profit (QoQ %) | number | 12.5 | QoQ growth |
| Net Profit (YoY %) | number | 18.9 | YoY growth |
| OPM (Latest Qtr) | number | 13.7 | Operating profit margin % |
| Promoter Holding | number | 50.48 | Percentage |
| Promoter QoQ Change | number | 0.1 | Percentage point change |
| FII Holding | number | 17.19 | Percentage |
| FII QoQ Change | number | -0.4 | Percentage point change |
| DII Holding | number | 21.1 | Percentage |
| DII QoQ Change | number | 0.36 | Percentage point change |
| Public Holding | number | 10.85 | Percentage |
| Pros | string | Strong Promoter... | Machine-generated |
| Cons | string | Low ROE \| Low Dividend | Machine-generated |
| URL | string | https://... | Company page URL |
| scraped_at | datetime | 2026-08-26 18:30:00 | UTC timestamp |

### Sheet 2: Quarterly

Last 8 quarters of quarterly results. One row per stock.

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| Ticker | string | RELIANCE | Stock ticker |
| Sales Mar 2024 | number | 236533 | In Rs. Crores |
| Sales Jun 2024 | number | 231784 | In Rs. Crores |
| Sales Sep 2024 | number | 231535 | In Rs. Crores |
| Sales Dec 2024 | number | 239986 | In Rs. Crores |
| Sales Mar 2025 | number | 261388 | In Rs. Crores |
| Sales Jun 2025 | number | 243632 | In Rs. Crores |
| Sales Sep 2025 | number | 254623 | In Rs. Crores |
| Sales Dec 2025 | number | 264905 | In Rs. Crores |
| Expenses Mar 2024 | number | ... | In Rs. Crores |
| ... | ... | ... | All quarterly rows |
| EPS Mar 2024 | number | ... | In Rs. |
| ... | ... | ... | ... |

### Quarterly Rows

| Row | Description |
|-----|-------------|
| Sales | Revenue from operations |
| Expenses | Total expenses |
| Operating Profit | Profit before interest, depreciation, tax |
| Other Income | Non-operating income |
| Interest | Interest expense |
| Depreciation | Depreciation and amortization |
| Net Profit | Profit after tax |
| EPS in Rs | Earnings per share |
| Dividend Payout % | Dividend as % of profit |

### Sheet 3: Annual

Last 4 years of P&L, Balance Sheet, Cash Flow, Ratios. One row per stock.

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| Ticker | string | RELIANCE | Stock ticker |
| Sales Mar 2022 | number | ... | In Rs. Crores |
| Sales Mar 2023 | number | ... | In Rs. Crores |
| Sales Mar 2024 | number | ... | In Rs. Crores |
| Sales Mar 2025 | number | ... | In Rs. Crores |
| Net Profit Mar 2022 | number | ... | In Rs. Crores |
| ... | ... | ... | All annual rows |
| Borrowings Mar 2022 | number | ... | In Rs. Crores |
| ... | ... | ... | ... |
| Cash from Operating Mar 2022 | number | ... | In Rs. Crores |
| ... | ... | ... | ... |

### Annual Rows (by section)

**Profit & Loss:**
- Sales, Expenses, Operating Profit, Other Income
- Interest, Depreciation, Net Profit, EPS in Rs

**Balance Sheet:**
- Equity Capital, Reserves, Borrowings
- Fixed Assets, Investments, Current Assets, Current Liabilities

**Cash Flows:**
- Cash from Operating Activity
- Cash from Investing Activity
- Cash from Financing Activity
- Net Cash Flow

**Ratios:**
- Debtor Days, Inventory Days, Days Payable
- Cash Conversion Cycle, Working Capital Days
- ROE %, Net Profit Margin

### Sheet 4: Shareholding

Last 8 quarters of shareholding pattern. One row per stock.

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| Ticker | string | RELIANCE | Stock ticker |
| Promoters Sep 2024 | number | 50.24 | Percentage |
| Promoters Dec 2024 | number | 50.13 | Percentage |
| Promoters Mar 2025 | number | 50.1 | Percentage |
| Promoters Jun 2025 | number | 50.07 | Percentage |
| Promoters Sep 2025 | number | 50.01 | Percentage |
| Promoters Dec 2025 | number | 50.0 | Percentage |
| Promoters Mar 2026 | number | 50.0 | Percentage |
| Promoters Jun 2026 | number | 50.48 | Percentage |
| FIIs Sep 2024 | number | 21.3 | Percentage |
| ... | ... | ... | All categories x 8 quarters |

## Code Changes Required

### config.py

```python
# New parameters
QUARTERLY_LOOKBACK = 8    # Number of quarters to scrape
ANNUAL_LOOKBACK = 4       # Number of years to scrape

# New section configs for full table extraction
QUARTERLY_ROWS = [
    "Sales", "Expenses", "Operating Profit", "Other Income",
    "Interest", "Depreciation", "Net Profit", "EPS in Rs",
    "Dividend Payout %",
]

ANNUAL_PNL_ROWS = [
    "Sales", "Expenses", "Operating Profit", "Other Income",
    "Interest", "Depreciation", "Net Profit", "EPS in Rs",
]

ANNUAL_BS_ROWS = [
    "Equity Capital", "Reserves", "Borrowings",
    "Fixed Assets", "Investments", "Current Assets", "Current Liabilities",
]

ANNUAL_CF_ROWS = [
    "Cash from Operating Activity", "Cash from Investing Activity",
    "Cash from Financing Activity", "Net Cash Flow",
]

ANNUAL_RATIO_ROWS = [
    "Debtor Days", "Inventory Days", "Days Payable",
    "Cash Conversion Cycle", "Working Capital Days",
    "ROE %", "Net Profit Margin",
]

SHAREHOLDING_CATEGORIES = [
    "Promoters", "FIIs", "DIIs", "Public", "Government", "Others",
]
```

### scrape_companies.py

**New functions:**

| Function | Purpose |
|----------|---------|
| `extract_full_table(soup, section_id, rows, lookback)` | Extract full historical table data |
| `extract_shareholding_history(soup, categories, lookback)` | Extract shareholding over time |
| `calculate_growth(current, previous)` | Calculate percentage growth |
| `write_xlsx(data, ticker, index_name)` | Write Excel file with sheets |
| `create_folder_structure(index_name, ticker)` | Create output folder |

**Modified functions:**

| Function | Change |
|----------|--------|
| `extract_company_data()` | Add new extraction calls |
| `save_company_data()` | Replace CSV with XLSX creation |
| `scrape_company()` | Return expanded data dict |

### requirements.txt

```
openpyxl>=3.1.0
```

## Migration Path

1. Add `openpyxl` to requirements.txt
2. Add new config parameters
3. Add new extraction functions
4. Add XLSX writer function
5. Modify `save_company_data()` to use XLSX
6. Update `.gitignore` for new output structure
7. Test with single index before full run

## Backward Compatibility

- Old CSV output is replaced entirely
- No fallback to CSV mode
- Old output files can be manually archived
