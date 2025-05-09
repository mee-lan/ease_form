# Nepal Forms Assistant - Chrome Extension

A Chrome browser extension that assists non-tech-savvy users in filling Nepali governmental forms with real-time guidance, AI-powered chatbot, and form templates.

## Important Notice
**The backend server now runs on port 5002** instead of the default port 5001.

If you're seeing "Unable to get guidance" errors in the frontend, please make sure the frontend is configured to connect to `http://localhost:5002` instead of `http://localhost:5001`.

**For AI-Powered Features**: This extension uses the Google Gemini API for its advanced features like AI-powered chat and intelligent form guidance. To enable these, you **must** set up an API key as an environment variable.

## Setting up Your Gemini API Key

To use the AI-powered features, you need a Google Gemini API key.

1.  Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Set this key as an environment variable named `NEPAL_FORMS_GEMINI_API_KEY` on the system where you will run the backend server.

    *   **Linux/macOS (bash/zsh):**
        Open your terminal and run:
        ```bash
        export NEPAL_FORMS_GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
        ```
        To make this permanent, add the line to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`, or `~/.profile`) and then source it (e.g., `source ~/.zshrc`).

    *   **Windows (Command Prompt):**
        ```cmd
        set NEPAL_FORMS_GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
        ```
        This sets it for the current session. For a permanent setting, search for "environment variables" in the Windows search bar and add it through the System Properties dialog.

    *   **Windows (PowerShell):**
        ```powershell
        $Env:NEPAL_FORMS_GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
        ```
        For a permanent setting, use the System Properties dialog as mentioned above, or add it to your PowerShell profile script.

    *   **Using a `.env` file (Recommended for local development):**
        1.  Create a file named `.env` in the root directory of this project.
        2.  Add the following line to it, replacing `YOUR_ACTUAL_API_KEY_HERE` with your actual key:
            ```
            NEPAL_FORMS_GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
            ```
        3.  Ensure `.env` is listed in your `.gitignore` file (it should be by default if you use a standard Python gitignore).
        4.  You'll need the `python-dotenv` package. If not already listed, add it to `backend/requirements.txt` and install it:
            ```bash
            pip install python-dotenv
            # Or if it's in requirements.txt
            pip install -r backend/requirements.txt
            ```
            The application will attempt to load this `.env` file automatically if `python-dotenv` is installed and used in the startup scripts.

**If the `NEPAL_FORMS_GEMINI_API_KEY` is not set or is invalid, the extension will operate in a fallback mode with limited functionality.**

## Running the Extension

### 1. Initialize the Project (First time setup)
If you haven't done so, run the initialization script:
```bash
python init.py
```
This script will create necessary directories, generate placeholder icons (if PIL/Pillow is installed), install Python requirements, and attempt to initialize form data (using the API key if available, or fallback data otherwise).

### 2. Start the Backend Server
Ensure your `NEPAL_FORMS_GEMINI_API_KEY` environment variable is set if you want AI features.
```bash
cd backend
python server.py
```
Alternatively, you can use the `run.py` script from the project root:
```bash
python run.py
```
The server will run on `http://localhost:5002`. The console output will indicate if it's running with AI features or in fallback mode.

### 3. Load the Chrome Extension
- Open Chrome and go to `chrome://extensions/`
- Enable "Developer mode" in the top right corner
- Click "Load unpacked" and select the root folder of this project

### Features Available in Fallback Mode
(If `NEPAL_FORMS_GEMINI_API_KEY` is not set or invalid)

- **Form Templates**: Access information about Nepali government forms (from local data).
- **Basic Form Detection**: The system can detect when you're on a government form page using basic pattern matching.
- **Simple Form Filling Assistance**: Get basic guidance for form fields based on predefined templates.
- **Limited Chat**: The chat feature will use pre-defined, canned responses instead of AI-generated ones.

### Features Available with Gemini AI
(If `NEPAL_FORMS_GEMINI_API_KEY` is correctly set)

- **All Fallback Features, plus:**
- **Intelligent Form Detection**: More accurate form detection and field analysis using AI.
- **AI-Powered Real-time Form Filling Assistance**: Get context-aware, AI-generated guidance for form fields.
- **Gemini-powered Chatbot**: Ask questions in simple language and get easy-to-understand, AI-generated answers about any Nepali government form or process.
- **AI-Generated Form Data**: During initialization (`init.py`), if web scraping fails, the system will attempt to use the Gemini API to generate up-to-date form information.

## Installation

### Requirements

- Python 3.7+ for the backend server
- Google Chrome browser
- A Google Gemini API key (for AI features) - see "Setting up Your Gemini API Key".

### Setting up the Backend Server

1. Clone this repository:
   ```
   git clone https://github.com/your-username/nepal-forms-assistant.git
   cd nepal-forms-assistant
   ```

2. Set up your Gemini API Key as an environment variable (see "Setting up Your Gemini API Key" section above).

3. Install the required Python packages:
   ```
   cd backend
   pip install -r requirements.txt
   ```

4. Initialize the project (if you haven't already):
    ```bash
    python init.py 
    ```

5. Start the backend server:
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

**Note**: The `/api/chat` and `/api/field-guidance` endpoints will provide enhanced responses if a valid Gemini API key is configured and the backend is running in AI mode. Otherwise, they will provide fallback responses.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Powered by Google's Gemini API
- Contains data from Nepal government websites and official resources
- Created to help simplify government form procedures for all Nepali citizens 