@echo off
@color 3
@cls
@echo Checking for the python installation...
@python --version >NUL
if errorlevel 1 (
    color 4
    @echo The python is not istalled.
    start https://www.python.org/downloads/
    pause
    exit
)
@echo The python is installed. Checking for the requirements. Please wait...
@pip install -r requirements.txt >NUL
if errorlevel 1 (
    color 4
    @echo Can't install requirements
    pause
    exit
)
@echo Everything is installed correctly.
@pause