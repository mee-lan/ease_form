# Nepal Forms Assistant - Setup Instructions

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- Internet connection for API access

## Quick Setup

1. Initialize the project:

   ```bash
   python init.py
   ```
   
   This script will:
   - Create necessary directories
   - Generate placeholder icons
   - Install Python requirements
   - Initialize form data

2. Start the backend server:

   ```bash
   python run.py
   ```

3. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" in the top-right corner
   - Click "Load unpacked" and select this project directory

## Manual Setup

If the quick setup doesn't work, you can follow these manual steps:

1. Install Python dependencies:

   ```bash
   pip install -r backend/requirements.txt
   ```

2. Create required directories:
   - `data/`
   - `backend/data/`
   - `frontend/css/`
   - `frontend/js/`
   - `frontend/icons/`
   - `icons/`

3. Generate placeholder icons:

   ```bash
   python generate_icons.py
   ```

4. Start the backend server:

   ```bash
   python backend/server.py
   ```

## Additional Options

- Run the server in debug mode:

  ```bash
  python run.py --debug
  ```

- Get help on available options:

  ```bash
  python run.py --help
  ```

## Troubleshooting

- **Server won't start**: Make sure you've installed all required dependencies and have Python 3.7+
- **Extension not loading**: Verify that you've selected the correct directory and that all files are in their proper locations
- **API errors**: Check that your Gemini API key is valid and configured correctly in the backend files

## Project Structure

- `/backend/` - Python backend server
  - `server.py` - Main Flask application
  - `form_detector.py` - Form detection and analysis
  - `form_scraper.py` - Data scraping module
  - `requirements.txt` - Python dependencies

- `/frontend/` - Frontend assets
  - `/css/` - Stylesheets
  - `/js/` - JavaScript files
  - `/icons/` - Extension icons

- `/icons/` - Icon files used by manifest.json
- `manifest.json` - Chrome extension manifest
- `popup.html` - Extension popup UI
- `background.js` - Extension background script
- `content.js` - Content script for web page integration 