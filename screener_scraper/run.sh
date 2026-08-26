#!/bin/bash
# Run both scraping scripts for given indexes (or all if no argument)
# Usage:
#   ./run.sh                          # scrape all indexes
#   ./run.sh SMALLCAP50               # scrape only SMALLCAP50
#   ./run.sh SMALLCAP50 NIFTY         # scrape multiple indexes
#   ./run.sh -v SMALLCAP50            # verbose/debug output

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python "$SCRIPT_DIR/scrape_indexes.py" "$@"
python "$SCRIPT_DIR/scrape_companies.py" "$@"
