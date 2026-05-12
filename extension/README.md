# Chrome Extension

This folder contains a Chrome extension (Manifest V3) for the News Credibility Checker.

## What it does

- Reads the current page's URL, title, and content
- Sends them to the backend `/api/check` endpoint at `http://127.0.0.1:8001`
- Displays the credibility score and category labels in a popup

## How to install

1. Start the backend server:
   ```powershell
   cd "D:\Certificates & Projects\news-credibility-checker 1\news-credibility-checker\backend"
   & ".\venv\Scripts\python.exe" -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
   ```
2. Open Chrome and go to `chrome://extensions/`
3. Enable `Developer mode`
4. Click `Load unpacked`
5. Select the `extension/` folder

## Usage

- Open a news article in Chrome
- Click the extension icon
- Review the extracted title and content
- Click `Analyze Page`
- View the returned scores directly in the popup
