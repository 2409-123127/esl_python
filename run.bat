@echo off

:: Run python command to see if python is available 
where python >nul 2>nul
:: Check if python command did run
if %errorlevel% equ 0 (
    :: Run python program with students.csv argument
    python main.py students.csv
    :: Go to :end  
    goto :end
)

:: If python not found try python3 command
where python3 >nul 2>nul
:: Check if python3 command did run
if %errorlevel% equ 0 (
    :: Run python program with students.csv argument
    python3 main.py students.csv
    :: Go to :end  
    goto :end
)

:: Python not found
echo Error: Python installation not found. Make sure that python is added to system PATH.
echo You can install Python from https://www.python.org/downloads/

:end
pause