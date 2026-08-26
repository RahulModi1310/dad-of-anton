"""
Script 1: Scrape Company Endpoints from Index Pages
====================================================
Scrapes all company tickers and names from each index page.
Outputs: one CSV per index with ticker and company name.
"""

import os
import sys
import csv
import re
import time
import logging
import argparse
from bs4 import BeautifulSoup
from config import BASE_URL, INDEXES, OUTPUT_DIR, REQUEST_DELAY
from utils import get_page

logger = logging.getLogger(__name__)


def get_total_pages(soup: BeautifulSoup) -> int:
    """Extract total pages from pagination info."""
    page_info = soup.select_one("[data-page-info]")
    if not page_info:
        return 1

    text = page_info.get_text()
    # Pattern: "50 results found: Showing page 1 of 2"
    match = re.search(r"of\s+(\d+)", text)
    if match:
        return int(match.group(1))

    # Fallback: count pagination links
    pagination_links = soup.select(".pagination a[href*='page=']")
    if pagination_links:
        pages = set()
        for link in pagination_links:
            href = link.get("href", "")
            page_match = re.search(r"page=(\d+)", href)
            if page_match:
                pages.add(int(page_match.group(1)))
        return max(pages) if pages else 1

    return 1


def extract_companies(soup: BeautifulSoup) -> list[dict]:
    """Extract company tickers and names from the constituents table."""
    companies = []
    rows = soup.select("tr[data-row-company-id]")

    for row in rows:
        # Find the company link
        link = row.select_one("td.text a[href*='/company/']")
        if not link:
            continue

        href = link.get("href", "")
        name = link.get_text(strip=True)

        # Extract ticker from URL pattern: /company/TICKER/ or /company/TICKER/consolidated/
        ticker_match = re.search(r"/company/([^/]+)/", href)
        if ticker_match:
            ticker = ticker_match.group(1)
            companies.append({
                "ticker": ticker,
                "name": name,
                "url": f"{BASE_URL}{href}",
            })

    return companies


def scrape_index(index_name: str, index_slug: str) -> list[dict]:
    """Scrape all companies from an index, handling pagination."""
    logger.info("=" * 60)
    logger.info("Scraping index: %s", index_name)
    logger.info("=" * 60)

    all_companies = []
    page = 1
    total_pages = None

    while True:
        # Build URL
        if page == 1:
            url = f"{BASE_URL}/company/{index_slug}/"
        else:
            url = f"{BASE_URL}/company/{index_slug}/?page={page}"

        logger.info("  Fetching page %d...", page)
        soup = get_page(url)

        if not soup:
            logger.error("  FAILED to fetch page %d", page)
            break

        # Get total pages on first page
        if total_pages is None:
            total_pages = get_total_pages(soup)
            logger.info("  (total pages: %d)", total_pages)

        # Extract companies from this page
        companies = extract_companies(soup)
        all_companies.extend(companies)
        logger.info("  Found %d companies on page %d", len(companies), page)

        # Check if we've reached the last page
        if page >= total_pages:
            break

        page += 1
        time.sleep(REQUEST_DELAY)

    logger.info("  Total companies scraped: %d", len(all_companies))
    return all_companies


def save_to_csv(companies: list[dict], index_name: str):
    """Save companies to a CSV file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{index_name}_companies.csv")

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ticker", "name", "url"])
        writer.writeheader()
        writer.writerows(companies)

    logger.info("  Saved to: %s", filepath)
    return filepath


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Scrape company endpoints from screener.in indexes")
    parser.add_argument("index", nargs="*", help="Index name(s) to scrape (e.g. SMALLCAP50 NIFTY). If omitted, scrapes all.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
    )

    # Filter indexes if specific ones requested
    if args.index:
        indexes = {}
        for name in args.index:
            if name in INDEXES:
                indexes[name] = INDEXES[name]
            else:
                # Use the argument directly as the URL slug
                indexes[name.upper()] = name
    else:
        indexes = INDEXES

    logger.info("Screener.in Index Scraper - Script 1")
    logger.info("=" * 60)
    logger.info("Indexes to scrape: %s", list(indexes.keys()))
    logger.info("Output directory: %s", OUTPUT_DIR)

    results = {}
    for index_name, index_slug in indexes.items():
        companies = scrape_index(index_name, index_slug)
        if companies:
            filepath = save_to_csv(companies, index_name)
            results[index_name] = {
                "count": len(companies),
                "file": filepath,
            }

    # Summary
    logger.info("=" * 60)
    logger.info("SCRAPE COMPLETE")
    logger.info("=" * 60)
    for index_name, info in results.items():
        logger.info("  %s: %d companies -> %s", index_name, info["count"], info["file"])

    return results


if __name__ == "__main__":
    main()
