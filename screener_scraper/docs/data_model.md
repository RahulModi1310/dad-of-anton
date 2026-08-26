# Data Model

## Current CSV Schema

### Index CSV (`{INDEX}_companies.csv`)

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| ticker | string | RELIANCE | Stock ticker symbol |
| name | string | Reliance Industries | Company display name |
| url | string | https://www.screener.in/company/RELIANCE/consolidated/ | Full company page URL |

### Data CSV (`{INDEX}_data.csv`)

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| Ticker | string | RELIANCE | Stock ticker symbol |
| Company Name | string | Reliance Industries Ltd | Full company name from page |
| Market Cap | string | 17,62,411 | Market cap in Rs. Crores |
| Current Price | string | 1,298 | Current stock price in Rs. |
| High / Low | string | ₹ 1,612 / 1,250 | 52-week high/low |
| Stock P/E | string | 23.6 | Price-to-earnings ratio |
| Book Value | string | 668 | Book value per share in Rs. |
| Dividend Yield | string | 0.46 | Dividend yield % |
| ROCE | string | 10.3 | Return on capital employed % |
| ROE | string | 8.91 | Return on equity % |
| Face Value | string | 10.0 | Face value per share in Rs. |
| Sales (Latest Qtr) | string | 309,468 | Latest quarter sales in Rs. Cr. |
| Operating Profit (Latest Qtr) | string | 42,246 | Latest quarter operating profit |
| Net Profit (Latest Qtr) | string | 18,540 | Latest quarter net profit |
| Promoter Holding | string | 50.48% | Promoter shareholding % |
| FII Holding | string | 17.19% | Foreign institutional investor % |
| DII Holding | string | 21.10% | Domestic institutional investor % |
| Public Holding | string | 10.85% | Public shareholding % |
| Government Holding | string | 0.08% | Government shareholding % |
| Others Holding | string | 0.30% | Others shareholding % |
| Pros | string | Strong Promoter... \| High Foreign... | Machine-generated pros |
| Cons | string | Low ROE \| Low Dividend | Machine-generated cons |
| Sector | string | Energy | Industry sector |
| Industry | string | Refineries & Marketing | Specific industry |
| URL | string | https://www.screener.in/company/RELIANCE/consolidated/ | Company page URL |
| scraped_at | string | 2026-08-26 18:30:00 | UTC timestamp of scrape |

## HTML Selectors Reference

### Top Ratios (`#top-ratios`)

```
Structure:
<ul id="top-ratios">
  <li class="flex flex-space-between">
    <span class="name">Market Cap</span>
    <span class="nowrap value">
      ₹ <span class="number">17,62,411</span> Cr.
    </span>
  </li>
  ...
</ul>

Selector: #top-ratios li
Name: .name text
Value: .number text (or .value text if .number absent)
```

### Quarterly Results (`#quarters`)

```
Structure:
<section id="quarters">
  <table class="data-table">
    <thead>
      <tr>
        <th></th>
        <th data-date-key="2023-06-30">Jun 2023</th>
        <th data-date-key="2023-09-30">Sep 2023</th>
        ... (13 quarters)
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="text">Sales</td>
        <td>207,559</td>
        <td>231,886</td>
        ... (13 values)
      </tr>
      ...
    </tbody>
  </table>
</section>

Selector: #quarters table
Row match: First td text contains row_name (case-insensitive)
Value: Last non-empty td (latest quarter)
```

### Quarterly Rows Available

| Row Name | Description |
|----------|-------------|
| Sales | Revenue from operations |
| Expenses | Total expenses |
| Operating Profit | Profit before interest, depreciation, tax |
| Other Income | Non-operating income |
| Interest | Interest expense |
| Depreciation | Depreciation and amortization |
| Net Profit | Profit after tax |
| EPS in Rs | Earnings per share |
| Dividend Payout % | Dividend as % of profit |

### Profit & Loss (`#profit-loss`)

```
Structure: Same as quarterly but annual data (Mar 2015 - Mar 2026)

Selector: #profit-loss table
Row match: First td text contains row_name
Value: Last non-empty td (latest year)
```

### Balance Sheet (`#balance-sheet`)

```
Structure: Same table format, annual data

Selector: #balance-sheet table
Available rows: Equity Capital, Reserves, Borrowings, Fixed Assets,
                Investments, Current Assets, Current Liabilities,
                Contingent Liabilities, Book Value
```

### Cash Flows (`#cash-flow`)

```
Structure: Same table format, annual data

Selector: #cash-flow table
Available rows: Cash from Operating Activity,
                Cash from Investing Activity,
                Cash from Financing Activity,
                Net Cash Flow
```

### Ratios (`#ratios`)

```
Structure: Same table format, annual data

Selector: #ratios table
Available rows: Debtor Days, Inventory Days, Days Payable,
                Cash Conversion Cycle, Working Capital Days,
                ROE %, Net Profit Margin, etc.
```

### Shareholding (`#shareholding`)

```
Structure:
<section id="shareholding">
  <table class="data-table">
    <thead>
      <tr>
        <th></th>
        <th>Sep 2023</th>
        <th>Dec 2023</th>
        ... (12 quarters)
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="text">
          <button>Promoters +</button>
        </td>
        <td>50.27%</td>
        <td>50.30%</td>
        ... (12 values)
      </tr>
      ...
    </tbody>
  </table>
</section>

Selector: #shareholding table
Row match: First td text contains category (case-insensitive)
Value: Last td (latest quarter)
```

### Shareholding Categories

| Category | Button Text |
|----------|-------------|
| Promoters | Promoters |
| FIIs | FIIs |
| DIIs | DIIs |
| Public | Public |
| Government | Government |
| Others | Others |

### Pros/Cons (`#analysis`)

```
Structure:
<section id="analysis">
  <div class="pros">
    <ul>
      <li>Pro item 1</li>
      <li>Pro item 2</li>
    </ul>
  </div>
  <div class="cons">
    <ul>
      <li>Con item 1</li>
    </ul>
  </div>
</section>

Selector: .pros ul li, .cons ul li
Join: " | " separator
```

### Sector/Industry (`#peers`)

```
Structure:
<section id="peers">
  <a href="/market/IN03/">Energy</a>
  <a href="/market/IN03/IN0301/">Oil, Gas & Consumable Fuels</a>
  <a href="/market/IN03/IN0301/IN030103/">Petroleum Products</a>
  <a href="/market/IN03/IN0301/IN030103/IN030103001/">Refineries & Marketing</a>
</section>

Selector: #peers a[href*='/market/']
Sector: First link text
Industry: Last link text
```

## Data Validation

Numeric fields are validated after extraction:

```python
NUMERIC_RATIOS = {
    "Market Cap", "Current Price", "Stock P/E", "Book Value",
    "Dividend Yield", "ROCE", "ROE", "Face Value",
    "Sales (Latest Qtr)", "Operating Profit (Latest Qtr)", "Net Profit (Latest Qtr)",
    "Promoter Holding", "FII Holding", "DII Holding", "Public Holding",
}
```

Non-numeric values in these fields are logged as warnings.
