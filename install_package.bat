@echo off
REM Activate the virtual environment
call .\.venv\Scripts\activate

REM Install Packages
pip install pytest
pip install selenium
pip install webdriver-manager
pip install pytest-xdist
pip install pytest-html
pip install pytest-dependency
pip install pytest-selenium
pip install pytest-ordering
pip install pandas

REM Deactivate the virtual environment
deactivate