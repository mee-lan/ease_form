# Nepal Forms Assistant - Chrome Extension

A Chrome browser extension that assists non-tech-savvy users in filling Nepali governmental forms with real-time guidance, AI-powered chatbot, and form templates.

## Important Notice
**The backend server now runs on port 5002** instead of the default port 5001.

If you're seeing "Unable to get guidance" errors in the frontend, please make sure the frontend is configured to connect to `http://localhost:5002` instead of `http://localhost:5001`.

## Running the Extension (Current Setup)

The extension is currently running in fallback mode without Gemini AI integration. This means:
- Form detection works
- Basic field guidance is provided
- The chat feature uses pre-defined responses instead of AI-generated ones

### How to Run

1. Start the backend server:
   ```
   cd backend
   python server.py
   ```

2. Load the Chrome extension:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" in the top right corner
   - Click "Load unpacked" and select the root folder of this project

3. The server will run on http://localhost:5002 and the extension will connect to it.

### Features Available in Fallback Mode

- **Form Templates**: Access information about Nepali government forms
- **Basic Form Detection**: The system can detect when you're on a government form page
- **Simple Form Filling Assistance**: Get basic guidance for form fields
- **Limited Chat**: Ask about requirements, process, or locations (limited to pre-defined responses)

### To Enable Gemini AI Features (Advanced)

To get the full AI-powered experience, you would need to:
1. Install Google's Generative AI package in a Python environment (not within the Cursor IDE)
2. Configure with a valid Gemini API key
3. Run the server from that environment

## Features

- **Form Templates**: Access comprehensive information about requirements, processes, and locations for common Nepali government forms:
  - Citizenship Certificate
  - Passport
  - Driving License
  - PAN Number
  - National ID Card
  - Lok Sewa Application
  - And more...

- **Intelligent Form Detection**: Automatically detects when you're on a government form page and provides context-aware guidance.

- **Real-time Form Filling Assistance**: Get field-by-field guidance while filling out forms.

- **Gemini-powered Chatbot**: Ask questions in simple language and get easy-to-understand answers about any Nepali government form or process.

## Installation

### Requirements

- Python 3.7+ for the backend server
- Google Chrome browser
- Gemini API key (provided in the extension)

### Setting up the Backend Server

1. Clone this repository:
   ```
   git clone https://github.com/your-username/nepal-forms-assistant.git
   cd nepal-forms-assistant
   ```

2. Install the required Python packages:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```
   python server.py
   ```

### Installing the Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" in the top right corner
3. Click "Load unpacked" and select the root folder of this project
4. The extension should now be installed and visible in your extensions toolbar

## Usage

### Viewing Form Templates

1. Click on the extension icon in your browser toolbar
2. Browse the available form templates
3. Click on any form to view detailed requirements, processes, and locations

### Using the Chatbot

1. Click "Chat with Assistant" from the main screen or form detail page
2. Type your question in simple language
3. Receive easy-to-understand guidance about form procedures

### Getting Help with Form Filling

When filling out a supported form online:
1. The extension will automatically detect the form type
2. Click on any form field to get specific guidance
3. Use the floating helper for additional assistance

## Development

### Project Structure

- `/backend/` - Python backend server
  - `server.py` - Main Flask application
  - `form_detector.py` - Form detection and analysis
  - `requirements.txt` - Python dependencies

- `/frontend/` - Frontend assets
  - `/css/` - Stylesheets
  - `/js/` - JavaScript files
  - `/icons/` - Extension icons

- `manifest.json` - Chrome extension manifest
- `popup.html` - Extension popup UI
- `background.js` - Extension background script
- `content.js` - Content script for web page integration

### API Endpoints

- `GET /api/forms` - Get list of all form templates
- `GET /api/form/<form_id>` - Get details for a specific form
- `POST /api/detect-form` - Detect form type from HTML content
- `POST /api/field-guidance` - Get guidance for filling a specific field
- `POST /api/chat` - Send a message to the Gemini-powered assistant

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Powered by Google's Gemini API
- Contains data from Nepal government websites and official resources
- Created to help simplify government form procedures for all Nepali citizens 