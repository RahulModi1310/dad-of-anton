"""Shared utilities for screener scraper."""

import logging
import time
import requests
from bs4 import BeautifulSoup
from config import REQUEST_DELAY, REQUEST_TIMEOUT, MAX_RETRIES, HEADERS

logger = logging.getLogger(__name__)

# Reuse TCP connections to the same domain
session = requests.Session()
session.headers.update(HEADERS)


def get_page(url: str) -> BeautifulSoup | None:
    """Fetch a page and return BeautifulSoup object with exponential backoff."""
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT)
            # Handle rate limiting (429)
            if response.status_code == 429:
                wait = 30  # Wait 30s on rate limit
                logger.warning("Rate limited (429) — waiting %ds", wait)
                time.sleep(wait)
                continue
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            wait = REQUEST_DELAY * (2 ** attempt)  # 1.5, 3, 6, 12...
            logger.warning("Attempt %d failed: %s — retrying in %.1fs", attempt + 1, e, wait)
            if attempt < MAX_RETRIES - 1:
                time.sleep(wait)
    return None
