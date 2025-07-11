# SNS Dashboard Setup

This repository contains the source code for a simple SNS view-count dashboard. The project fetches statistics from YouTube, Instagram and TikTok and stores them in a Google Sheets document.

Follow the steps below to get the project running on Windows using a virtual environment.

## 1. Create and activate a virtual environment
```powershell
cd C:\Users\yesun\OneDrive\바탕 화면\깃허브\sheet_money
python -m venv .venv
.\.venv\Scripts\activate
```

## 2. Install dependencies
Upgrade `pip` and install all required packages. If you plan to freeze the environment later, update `requirements.txt` using `pip freeze`.
```powershell
pip install --upgrade pip
pip install -r sns_dashboard\requirements.txt
```

## 3. Configure credentials
Prepare the following files:
- `sns_dashboard\config\client_secrets.json` – Google OAuth credentials
- `sns_dashboard\config\app_secrets.json` – Instagram and TikTok keys

## 4. Run the CLI
Execute the initial setup command which stores credentials and sheet ID:
```powershell
python -m sns_dashboard.main setup
```

Later you can collect data with:
```powershell
python -m sns_dashboard.main update --help
```

## 5. Building an executable
After verifying that the program runs correctly, you can package it using PyInstaller:
```powershell
cd sns_dashboard
build.bat
```
The final executable will appear in `dist\sns-dashboard.exe`.
