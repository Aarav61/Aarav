@echo off
echo Building PC Shutdown Timer...
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --name PC-Shutdown-Timer shutdown_timer.py
echo.
echo Done. Your EXE is in the dist folder.
pause
