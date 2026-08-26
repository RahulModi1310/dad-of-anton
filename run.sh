#!/bin/bash
# Run both scraping scripts for a given index (or all if no argument)
# Usage:
#   ./run.sh              # scrape all indexes
#   ./run.sh SMALLCAP50   # scrape only SMALLCAP50

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python "$SCRIPT_DIR/scrape_indexes.py" "$@"
python "$SCRIPT_DIR/scrape_companies.py" "$@"
