@echo off
@color 2
@cls
@python --version >NUL
if errorlevel 1 (
    start https://www.python.org/downloads/
    pause
)
@pip install -r requirements.txt >NUL
if errorlevel 1 (
    pause
)