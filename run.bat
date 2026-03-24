@echo off
echo Starting Reddit Video Generator...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python main.py
pause
