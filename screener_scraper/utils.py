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
    """Fetch a page and return BeautifulSoup object with retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.warning("Attempt %d failed: %s", attempt + 1, e)
            if attempt < MAX_RETRIES - 1:
                time.sleep(REQUEST_DELAY * (attempt + 1))
    return None
