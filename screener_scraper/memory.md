# Screener.in Scraper — Memory & Learnings

## Project Structure
```
screener_scraper/
├── config.py           # Indexes, data points, request settings
├── utils.py            # Shared: get_page(), session, logging
├── scrape_indexes.py   # Script 1: scrape company endpoints from index pages
├── scrape_companies.py # Script 2: scrape detailed data per company
├── run.sh / run.bat    # Run both scripts for given indexes
├── requirements.txt    # requests, beautifulsoup4, tqdm
└── .gitignore
```

## Key Learnings

### Screener.in HTML Structure
- Index pages: companies listed in `table` inside `#constituents` section
- Company rows: `tr[data-row-company-id]`
- Company link: `td.text a[href*='/company/']` → href pattern `/company/TICKER/` or `/company/TICKER/consolidated/`
- Pagination info: `div[data-page-info]` text "X results found: Showing page Y of Z"
- Default ratios: `#top-ratios li` → `.name` span + `.value .number` span
- Quarterly results: `#quarters table` → rows with `td` cells, last cell = latest quarter
- Shareholding: `#shareholding table` → rows with category in first `td`, last `td` = latest
- Pros/Cons: `#analysis .pros ul li` and `#analysis .cons ul li`
- Sector/Industry: `#peers a[href*='/market/']` → first = sector, last = industry

### Scraping Behavior
- Default 25 results per page
- Use `?page=N` for pagination, `?limit=50` for more per page (but 25 is safest)
- Rate limit: 1.5s delay between requests is respectful
- 429 responses need 30s+ wait
- Session reuse saves ~0.5s per request via connection pooling

### Data Points That DON'T Exist by Default
- "ROE 3yr avg", "EPS (ttm)", "Debt to Equity", "Promoter Holding", "EV/EBITDA" — NOT in default `#top-ratios`
- Must be added via "Edit ratios" on screener.in account first
- Only scrape what's actually on the page

### Windows-Specific
- Use `cmd /c` for chained commands (PowerShell doesn't support `&&`)
- Path separators: use forward slashes in Python, backslashes in cmd

## Completed Improvements
1. ✅ Extract shared code to utils.py
2. ✅ Session reuse (connection pooling)
3. ✅ Resume capability (skip scraped tickers)
4. ✅ Proper logging module
5. ✅ Progress bar (tqdm)
6. ✅ Multiple indexes in one run
7. ✅ --force flag
8. ✅ --verbose / -v flag
9. ✅ Timestamp (scraped_at) per record
10. ✅ Checkpoint saves every 10 stocks
11. ✅ Failed tickers log (_failed_tickers.csv)
12. ✅ More data points (quarterly, shareholding, pros/cons)
13. ✅ Cross-index deduplication
14. ✅ Summary report with timing
15. ✅ Exponential backoff for retries
16. ✅ 429 rate limit handling
17. ✅ Data validation (numeric checks)

## Pending Improvements
- [ ] Dry run mode (--dry-run)
- [ ] Async/concurrent requests
- [ ] Compare with previous run (detect changes)
- [ ] Quarterly results (full historical)
- [ ] Balance sheet data
- [ ] Peer comparison table
- [ ] Excel output support
- [ ] YAML/TOML config
- [ ] Unit tests
- [ ] Scheduling (cron/task scheduler)
- [ ] Email/notification on completion
- [ ] Auto-archival of old outputs

## Pending Improvements
- [ ] Dry run mode (--dry-run)
- [ ] Async/concurrent requests
- [ ] Data validation (numeric checks)
- [ ] Compare with previous run (detect changes)
- [ ] Quarterly results (full historical)
- [ ] Balance sheet data
- [ ] Peer comparison table
- [ ] Excel output support
- [ ] YAML/TOML config
- [ ] Unit tests
- [ ] Scheduling (cron/task scheduler)
- [ ] Email/notification on completion
- [ ] Auto-archival of old outputs
