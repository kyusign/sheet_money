@echo off
python -m pip install -r requirements.txt
pyinstaller --noconfirm --onefile --add-data "config;config" ^
  --name sns-dashboard main.py
echo Build complete → dist\sns-dashboard.exe
pause
