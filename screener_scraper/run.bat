@echo off
REM Run both scraping scripts for given indexes (or all if no argument)
REM Usage:
REM   run.bat                          # scrape all indexes
REM   run.bat SMALLCAP50               # scrape only SMALLCAP50
REM   run.bat SMALLCAP50 NIFTY         # scrape multiple indexes
REM   run.bat -v SMALLCAP50            # verbose/debug output

python "%~dp0scrape_indexes.py" %*
python "%~dp0scrape_companies.py" %*
