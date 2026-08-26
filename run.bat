@echo off
REM Run both scraping scripts for a given index (or all if no argument)
REM Usage:
REM   run.bat              # scrape all indexes
REM   run.bat SMALLCAP50   # scrape only SMALLCAP50

python "%~dp0scrape_indexes.py" %*
python "%~dp0scrape_companies.py" %*
