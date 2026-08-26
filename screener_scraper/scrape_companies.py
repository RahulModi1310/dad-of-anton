"""
Script 2: Scrape Company Details
=================================
Reads company tickers from CSV files (output of Script 1),
fetches each company page, and scrapes fundamental/technical data.
Outputs: one CSV per index with detailed company data.
"""

import os
import sys
import csv
import re
import time
import logging
import argparse
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from tqdm import tqdm
from config import BASE_URL, OUTPUT_DIR, REQUEST_DELAY, COMPANY_DATA_POINTS
from utils import get_page

logger = logging.getLogger(__name__)


def extract_ratio_value(soup: BeautifulSoup, ratio_name: str) -> str:
    """Extract a specific ratio value from the #top-ratios section."""
    ratios_list = soup.select_one("#top-ratios")
    if not ratios_list:
        return ""

    for li in ratios_list.select("li"):
        name_span = li.select_one(".name")
        value_span = li.select_one(".value")

        if name_span and value_span:
            name_text = name_span.get_text(strip=True)
            if ratio_name.lower() in name_text.lower():
                # Get the number from value
                number = value_span.select_one(".number")
                if number:
                    return number.get_text(strip=True)
                return value_span.get_text(strip=True)

    return ""


def extract_ratio_value_by_exact(soup: BeautifulSoup, ratio_name: str) -> str:
    """Extract ratio by exact name match."""
    ratios_list = soup.select_one("#top-ratios")
    if not ratios_list:
        return ""

    for li in ratios_list.select("li"):
        name_span = li.select_one(".name")
        value_span = li.select_one(".value")

        if name_span and value_span:
            name_text = name_span.get_text(strip=True)
            if name_text == ratio_name:
                number = value_span.select_one(".number")
                if number:
                    return number.get_text(strip=True)
                return value_span.get_text(strip=True)

    return ""


def extract_quarterly_value(soup: BeautifulSoup, row_name: str) -> str:
    """Extract the latest quarter value from #quarters table."""
    quarters_table = soup.select_one("#quarters table")
    if not quarters_table:
        return ""

    rows = quarters_table.select("tr")
    for row in rows:
        cells = row.select("td")
        if not cells:
            continue
        label_cell = cells[0]
        if row_name.lower() in label_cell.get_text(strip=True).lower():
            # Get the last non-empty cell (latest quarter)
            for cell in reversed(cells[1:]):
                text = cell.get_text(strip=True)
                if text:
                    return text

    return ""


def extract_shareholding(soup: BeautifulSoup, category: str) -> str:
    """Extract shareholding percentage from #shareholding table."""
    shareholding_table = soup.select_one("#shareholding table")
    if not shareholding_table:
        return ""

    rows = shareholding_table.select("tr")
    for row in rows:
        cells = row.select("td")
        if not cells:
            continue
        label_cell = cells[0]
        if category.lower() in label_cell.get_text(strip=True).lower():
            # Get the last cell (latest quarter)
            if len(cells) > 1:
                return cells[-1].get_text(strip=True)

    return ""


def extract_pros_cons(soup: BeautifulSoup) -> tuple[str, str]:
    """Extract pros and cons from #analysis section."""
    pros = []
    cons = []

    pros_section = soup.select_one(".pros ul")
    if pros_section:
        for li in pros_section.select("li"):
            text = li.get_text(strip=True)
            if text:
                pros.append(text)

    cons_section = soup.select_one(".cons ul")
    if cons_section:
        for li in cons_section.select("li"):
            text = li.get_text(strip=True)
            if text:
                cons.append(text)

    return " | ".join(pros), " | ".join(cons)


def extract_company_data(soup: BeautifulSoup) -> dict:
    """Extract all configured data points from a company page."""
    data = {}

    # Get pros and cons once
    pros_text, cons_text = extract_pros_cons(soup)

    for label, selector_type, selector_value in COMPANY_DATA_POINTS:
        if selector_type == "ratio":
            data[label] = extract_ratio_value(soup, selector_value)
        elif selector_type == "ratio_exact":
            data[label] = extract_ratio_value_by_exact(soup, selector_value)
        elif selector_type == "quarterly":
            data[label] = extract_quarterly_value(soup, selector_value)
        elif selector_type == "shareholding":
            data[label] = extract_shareholding(soup, selector_value)
        elif selector_type == "pros_cons":
            if selector_value == "pros":
                data[label] = pros_text
            elif selector_value == "cons":
                data[label] = cons_text

    # Also extract company name from page title
    title = soup.select_one("h1")
    if title:
        data["Company Name"] = title.get_text(strip=True)

    # Extract sector/industry from peers section
    sector_links = soup.select("#peers a[href*='/market/']")
    if sector_links:
        data["Sector"] = sector_links[0].get_text(strip=True) if len(sector_links) > 0 else ""
        data["Industry"] = sector_links[-1].get_text(strip=True) if len(sector_links) > 1 else ""

    return data


def scrape_company(ticker: str, url: str) -> dict | None:
    """Scrape a single company page."""
    soup = get_page(url)

    if not soup:
        logger.error("    FAILED to scrape %s", ticker)
        # Log failed ticker for retry
        failed_path = os.path.join(OUTPUT_DIR, "_failed_tickers.csv")
        with open(failed_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([ticker, url, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")])
        return None

    data = extract_company_data(soup)
    data["Ticker"] = ticker
    data["URL"] = url
    data["scraped_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return data


def load_companies_from_csv(csv_path: str) -> list[dict]:
    """Load company data from a CSV file."""
    companies = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)
    return companies


def load_scraped_tickers(index_name: str) -> set[str]:
    """Load tickers that have already been scraped from existing output."""
    filepath = os.path.join(OUTPUT_DIR, f"{index_name}_data.csv")
    if not os.path.exists(filepath):
        return set()

    tickers = set()
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickers.add(row.get("Ticker", ""))
    return tickers


def scrape_index_companies(csv_path: str, index_name: str, seen_tickers: set[str] | None = None) -> list[dict]:
    """Scrape all companies from a CSV file, skipping already-scraped ones."""
    companies = load_companies_from_csv(csv_path)
    scraped_tickers = load_scraped_tickers(index_name)

    # Merge with seen_tickers for cross-index deduplication
    if seen_tickers:
        scraped_tickers = scraped_tickers | seen_tickers

    # Load existing data to append to
    existing_data = []
    if scraped_tickers:
        filepath = os.path.join(OUTPUT_DIR, f"{index_name}_data.csv")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                existing_data = list(reader)
        logger.info("  Resuming: %d already scraped, skipping them", len(scraped_tickers))

    remaining = [c for c in companies if c["ticker"] not in scraped_tickers]
    logger.info("  Found %d total, %d remaining to scrape", len(companies), len(remaining))

    all_data = existing_data.copy()
    for i, company in enumerate(tqdm(remaining, desc=f"  {index_name}", unit="stock"), 1):
        ticker = company["ticker"]
        url = company["url"]

        data = scrape_company(ticker, url)

        if data:
            all_data.append(data)

        # Rate limiting
        if i < len(remaining):
            time.sleep(REQUEST_DELAY)

        # Checkpoint every 10 companies
        if i % 10 == 0 and all_data:
            save_company_data(all_data, index_name)
            logger.debug("    [checkpoint saved]")

    return all_data


def save_company_data(data: list[dict], index_name: str):
    """Save company data to a CSV file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{index_name}_data.csv")

    if not data:
        logger.info("  No data to save for %s", index_name)
        return None

    # Get all unique keys across all records
    fieldnames = ["Ticker", "Company Name"]
    data_keys = [k for d in data for k in d.keys() if k not in ["Ticker", "Company Name", "URL"]]
    fieldnames.extend(sorted(set(data_keys)))
    fieldnames.append("URL")

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)

    logger.info("  Saved to: %s", filepath)
    return filepath


def find_index_csv_files() -> dict[str, str]:
    """Find all index CSV files in the output directory."""
    csv_files = {}
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith("_companies.csv"):
            index_name = filename.replace("_companies.csv", "")
            csv_files[index_name] = os.path.join(OUTPUT_DIR, filename)
    return csv_files


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Scrape company details from screener.in")
    parser.add_argument("index", nargs="*", help="Index name(s) to scrape (e.g. SMALLCAP50 NIFTY). If omitted, scrapes all.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("-f", "--force", action="store_true", help="Re-scrape even if output file exists")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
    )

    logger.info("Screener.in Company Scraper - Script 2")
    logger.info("=" * 60)

    start_time = time.time()

    # Find index CSV files
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    index_files = find_index_csv_files()

    if not index_files:
        logger.info("\nNo index CSV files found in %s", OUTPUT_DIR)
        logger.info("Please run Script 1 (scrape_indexes.py) first.")
        return

    # Filter if specific indexes requested
    if args.index:
        filtered = {}
        for name in args.index:
            upper = name.upper()
            if upper in index_files:
                filtered[upper] = index_files[upper]
            elif name in index_files:
                filtered[name] = index_files[name]
            else:
                logger.info("\nError: No CSV file found for index '%s'", name)
                logger.info("Available: %s", list(index_files.keys()))
                logger.info("Run Script 1 first for this index.")
                sys.exit(1)
        index_files = filtered

    logger.info("Found %d index files: %s", len(index_files), list(index_files.keys()))

    results = {}
    seen_tickers = set()
    for index_name, csv_path in index_files.items():
        logger.info("=" * 60)
        logger.info("Processing index: %s", index_name)
        logger.info("=" * 60)

        # Delete existing output if --force
        if args.force:
            existing = os.path.join(OUTPUT_DIR, f"{index_name}_data.csv")
            if os.path.exists(existing):
                os.remove(existing)
                logger.info("  Deleted existing output for re-scrape")

        data = scrape_index_companies(csv_path, index_name, seen_tickers)

        # Track tickers seen across indexes for deduplication
        for d in data:
            ticker = d.get("Ticker", "")
            if ticker:
                seen_tickers.add(ticker)

        if data:
            filepath = save_company_data(data, index_name)
            results[index_name] = {
                "count": len(data),
                "file": filepath,
            }

    elapsed = time.time() - start_time

    # Summary
    logger.info("=" * 60)
    logger.info("SCRAPE COMPLETE")
    logger.info("=" * 60)
    total_companies = 0
    for index_name, info in results.items():
        logger.info("  %s: %d companies -> %s", index_name, info["count"], info["file"])
        total_companies += info["count"]
    logger.info("-" * 60)
    logger.info("  Total: %d companies scraped", total_companies)
    logger.info("  Time taken: %.1f seconds", elapsed)
    if total_companies > 0:
        logger.info("  Avg time per company: %.2f seconds", elapsed / total_companies)

    return results


if __name__ == "__main__":
    main()
