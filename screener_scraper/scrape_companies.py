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
import argparse
import requests
from bs4 import BeautifulSoup, Tag
from config import (
    BASE_URL, OUTPUT_DIR, REQUEST_DELAY, REQUEST_TIMEOUT,
    MAX_RETRIES, HEADERS, COMPANY_DATA_POINTS
)


def get_page(url: str) -> BeautifulSoup | None:
    """Fetch a page and return BeautifulSoup object."""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"    Attempt {attempt + 1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(REQUEST_DELAY * (attempt + 1))
    return None


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


def extract_company_data(soup: BeautifulSoup) -> dict:
    """Extract all configured data points from a company page."""
    data = {}

    for label, selector_type, selector_value in COMPANY_DATA_POINTS:
        if selector_type == "ratio":
            value = extract_ratio_value(soup, selector_value)
            data[label] = value
        elif selector_type == "ratio_exact":
            value = extract_ratio_value_by_exact(soup, selector_value)
            data[label] = value

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
    print(f"    Scraping {ticker}...", end=" ")
    soup = get_page(url)

    if not soup:
        print("FAILED")
        return None

    data = extract_company_data(soup)
    data["Ticker"] = ticker
    data["URL"] = url
    print("OK")
    return data


def load_companies_from_csv(csv_path: str) -> list[dict]:
    """Load company data from a CSV file."""
    companies = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)
    return companies


def scrape_index_companies(csv_path: str) -> list[dict]:
    """Scrape all companies from a CSV file."""
    companies = load_companies_from_csv(csv_path)
    all_data = []

    print(f"\n  Found {len(companies)} companies to scrape")

    for i, company in enumerate(companies, 1):
        ticker = company["ticker"]
        url = company["url"]

        print(f"  [{i}/{len(companies)}]", end="")
        data = scrape_company(ticker, url)

        if data:
            all_data.append(data)

        # Rate limiting
        if i < len(companies):
            time.sleep(REQUEST_DELAY)

    return all_data


def save_company_data(data: list[dict], index_name: str):
    """Save company data to a CSV file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{index_name}_data.csv")

    if not data:
        print(f"  No data to save for {index_name}")
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

    print(f"  Saved to: {filepath}")
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
    parser.add_argument("index", nargs="?", help="Index name to scrape (e.g. SMALLCAP50). If omitted, scrapes all.")
    args = parser.parse_args()

    print("Screener.in Company Scraper - Script 2")
    print("=" * 60)

    # Find index CSV files
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    index_files = find_index_csv_files()

    if not index_files:
        print(f"\nNo index CSV files found in {OUTPUT_DIR}")
        print("Please run Script 1 (scrape_indexes.py) first.")
        return

    # Filter if specific index requested
    if args.index:
        upper = args.index.upper()
        if upper in index_files:
            index_files = {upper: index_files[upper]}
        elif args.index in index_files:
            index_files = {args.index: index_files[args.index]}
        else:
            print(f"\nError: No CSV file found for index '{args.index}'")
            print(f"Available: {list(index_files.keys())}")
            print("Run Script 1 first for this index.")
            sys.exit(1)

    print(f"Found {len(index_files)} index files: {list(index_files.keys())}")

    results = {}
    for index_name, csv_path in index_files.items():
        print(f"\n{'='*60}")
        print(f"Processing index: {index_name}")
        print(f"{'='*60}")

        data = scrape_index_companies(csv_path)
        if data:
            filepath = save_company_data(data, index_name)
            results[index_name] = {
                "count": len(data),
                "file": filepath,
            }

    # Summary
    print(f"\n{'='*60}")
    print("SCRAPE COMPLETE")
    print(f"{'='*60}")
    for index_name, info in results.items():
        print(f"  {index_name}: {info['count']} companies -> {info['file']}")

    return results


if __name__ == "__main__":
    main()
