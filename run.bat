@echo off
REM Activate the virtual environment
call .\.venv\Scripts\activate

REM Run pytest
pytest -s -v

REM Deactivate the virtual environment
deactivate
