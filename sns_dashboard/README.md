# SNS Dashboard

This project collects view counts from YouTube, Instagram, and TikTok and appends them to a Google Sheets dashboard.

## Setup

1. Install Python 3.11 or later.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/\bin/activate  # Windows: .\.venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Prepare `config/client_secrets.json` and `config/app_secrets.json` with your API credentials.
5. Run the CLI:
   ```bash
   python -m sns_dashboard.main setup
   ```

See the documentation for full usage instructions.
