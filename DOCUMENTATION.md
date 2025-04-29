# Nepal Forms Assistant - Technical Documentation

This document provides detailed technical documentation for the Nepal Forms Assistant Chrome extension, explaining architecture, workflows, and implementation details.

## Architecture Overview

The extension follows a client-server architecture with these main components:

```
+------------------------+     +------------------------+
|  Chrome Extension      |     |  Python Backend        |
|  (Frontend)            |<--->|  (Server)              |
+------------------------+     +------------------------+
        |                              |
        |                              |
        v                              v
+------------------------+     +------------------------+
|  Web Page Integration  |     |  Gemini API            |
|  (Content Scripts)     |     |  (AI Assistant)        |
+------------------------+     +------------------------+
```

### Key Components

1. **Chrome Extension (Frontend)**
   - Popup UI for form templates and chatbot
   - Background service worker for event handling
   - Content scripts for web page integration

2. **Python Backend (Server)**
   - Flask REST API for data and AI services
   - Form detector for identifying governmental forms
   - Gemini integration for AI-powered guidance

## Data Flow Diagram

```
+-------------+     +--------------+     +-------------+     +-------------+
| User        |---->| Chrome       |---->| Python      |---->| Gemini AI   |
| Interaction |     | Extension    |     | Backend     |     | API         |
+-------------+     +--------------+     +-------------+     +-------------+
      ^                   |                    |                   |
      |                   v                    v                   |
      |              +--------------+     +-------------+          |
      +--------------|  Web Page    |<----| Form Data   |<---------+
                     |  Integration |     | Repository  |
                     +--------------+     +-------------+
```

## Workflow Description

### Extension Initialization
1. User installs the extension and runs the initialization script
2. Script creates necessary directories and generates icons
3. Python backend is started and serves the API endpoints
4. When extension is loaded, it checks for backend connection

### Form Template Browsing
1. User clicks on extension icon, triggering the popup UI
2. Popup loads form templates from backend API (`/api/forms`)
3. User selects a form to view detailed information
4. Backend serves form details from data repository (`/api/form/<form_id>`)

### Real-time Form Detection
```
+-------------+     +--------------+     +-------------+     +-------------+
| User visits |---->| Content      |---->| Form        |---->| Returns     |
| form page   |     | script scans |     | detector    |     | form type   |
+-------------+     | page HTML    |     | analyzes    |     | & fields    |
                    +--------------+     +-------------+     +-------------+
                          |                                       |
                          v                                       v
                    +--------------+     +-------------+     +-------------+
                    | Helper UI    |<----| Background  |<----| Form data   |
                    | injected     |     | processes   |     | sent to     |
                    +--------------+     | detection   |     | backend     |
                                         +-------------+     +-------------+
```

1. When user visits a webpage, content script runs automatically
2. Content script checks if the page contains form elements
3. If form detected, sends HTML content to backend for analysis
4. Backend identifies the form type (citizenship, passport, etc.)
5. Content script adds floating helper and field guidance capabilities

### Form Field Guidance
1. User focuses on a form field while filling a form
2. Content script highlights the field and requests guidance
3. Background script forwards request to backend API
4. Backend provides field-specific guidance (using Gemini if needed)
5. Content script displays guidance in a tooltip near the field

### Chatbot Interaction
```
+-------------+     +--------------+     +-------------+     +-------------+
| User asks   |---->| Extension    |---->| Backend     |---->| Gemini AI   |
| question    |     | formats      |     | adds form   |     | generates   |
+-------------+     | query        |     | context     |     | response    |
      ^              +--------------+     +-------------+     +-------------+
      |                                                            |
      |                                                            v
      |              +--------------+     +-------------+     +-------------+
      +--------------|  Response    |<----| Backend     |<----| AI response |
                     |  displayed   |     | processes   |     | received    |
                     +--------------+     +-------------+     +-------------+
```

1. User asks a question via chatbot interface
2. Question is sent to backend with current form context (if any)
3. Backend adds relevant form information to the prompt
4. Gemini AI generates response with simple, non-technical language
5. Response is displayed to user in chat interface

## Component Details

### 1. Manifest File (`manifest.json`)
- Defines extension properties, permissions, and components
- Specifies content scripts and background service worker
- Declares host permissions for website integration

### 2. Backend Server (`backend/server.py`)
- Flask application providing REST API endpoints
- Handles form data retrieval and AI integration
- Routes user queries to appropriate services

### 3. Form Detector (`backend/form_detector.py`)
- Analyzes webpage HTML to identify governmental forms
- Uses pattern matching and AI for form classification
- Extracts form fields for guidance provision

### 4. Form Scraper (`backend/form_scraper.py`)
- Collects form information from government websites
- Falls back to Gemini AI when web scraping fails
- Maintains up-to-date form requirements and procedures

### 5. Popup Interface (`popup.html` & `frontend/js/popup.js`)
- Provides user interface for form templates and chatbot
- Displays form requirements, processes, and locations
- Handles communication with backend API

### 6. Content Script (`content.js`)
- Injects into web pages to detect and assist with forms
- Adds field guidance and floating helper functionality
- Communicates with background script for API requests

### 7. Background Script (`background.js`)
- Manages extension state and event handling
- Coordinates between popup and content scripts
- Handles API communication with backend server

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/forms` | GET | Returns list of all available form templates |
| `/api/form/<form_id>` | GET | Returns detailed information for specific form |
| `/api/detect-form` | POST | Analyzes HTML content to detect form type |
| `/api/field-guidance` | POST | Provides guidance for specific form fields |
| `/api/chat` | POST | Handles chatbot queries with Gemini integration |

## Form Detection Logic

The extension uses a multi-layered approach to detect government forms:

1. **Pattern Matching**: Checks for form-related keywords in Nepali and English
2. **Structure Analysis**: Examines HTML structure for form elements
3. **AI Classification**: Uses Gemini to identify ambiguous forms
4. **Field Extraction**: Identifies form fields for targeted assistance

```
+---------------------+
| Webpage HTML        |
+---------------------+
           |
           v
+---------------------+
| Check for keywords  |
+---------------------+
           |
           v
+---------------------+     +---------------------+
| Analyze form        |---->| No form detected    |
| structure           |     | (Exit)              |
+---------------------+     +---------------------+
           |
           | Form detected
           v
+---------------------+
| Pattern matching    |
| for form type       |
+---------------------+
           |
           | Ambiguous form
           v
+---------------------+
| AI classification   |
| with Gemini         |
+---------------------+
           |
           v
+---------------------+
| Extract form fields |
| for guidance        |
+---------------------+
           |
           v
+---------------------+
| Return form type    |
| and field data      |
+---------------------+
```

## Gemini AI Integration

The extension leverages Google's Gemini AI for three key functions:

1. **Form Content Generation**: Creating accurate form requirements and procedures when scraping fails
2. **Field-Specific Guidance**: Providing context-aware guidance for individual form fields
3. **Chatbot Responses**: Answering user questions with simple language and accurate information

For chatbot interactions, the system uses a specialized prompt:

```
System Prompt: "You are an assistant helping non-tech-savvy users with Nepali 
governmental forms. Provide simple, clear instructions and guidance for form 
filling. Use simple language and avoid technical terms. Always provide accurate 
information about document requirements, office locations, and procedures."

User Query: [User's question]

Form Context: [Current form details if available]
```

## Python-JavaScript Integration

The extension bridges Python and JavaScript through:

1. **REST API**: Backend exposes endpoints consumed by frontend
2. **JSON Data Exchange**: Structured data format for communication
3. **Asynchronous Requests**: Non-blocking communication pattern

## Security Considerations

1. **API Key Protection**: Gemini API key should be secured in production
2. **Form Data Privacy**: Personal information is processed locally
3. **Content Script Isolation**: Limited access to webpage DOM
4. **Cross-Origin Restrictions**: Managed through permissions and CORS

## Deployment Guide

For production deployment:

1. **Backend Hosting**: Deploy Flask app on cloud service (Heroku, AWS, etc.)
2. **API Configuration**: Update API_BASE_URL in frontend code
3. **Extension Publishing**: Package for Chrome Web Store submission
4. **Database Integration**: Add persistent storage for form data

## Extending the Project

To add support for new form types:

1. Add form type detection in `form_detector.py`
2. Create form data template in `form_scraper.py`
3. Update form keywords list for detection
4. Add form-specific guidance in the AI prompt templates

To support additional languages:

1. Add language detection in backend
2. Create localized form templates
3. Modify AI prompts for multi-language support
4. Update UI text through localization system

## Troubleshooting

Common issues and solutions:

1. **Backend Connection Failure**: Check if Flask server is running on correct port
2. **Form Detection Issues**: Verify HTML structure and keywords
3. **API Key Errors**: Ensure Gemini API key is valid and properly configured
4. **Extension Loading Problems**: Check manifest permissions and content script matches

## Performance Optimization

1. **Caching**: Form data is cached to reduce API calls
2. **Lazy Loading**: Components load on demand
3. **Throttling**: API requests are throttled to prevent rate limiting
4. **Minimal DOM Manipulation**: Optimized content script injection

---

## Project Structure Diagram

```
nepal-forms-assistant/
├── manifest.json              # Extension manifest
├── popup.html                 # Main extension popup
├── background.js              # Background service worker
├── content.js                 # Content script for webpage injection
├── init.py                    # Initialization script
├── run.py                     # Server runner script
├── generate_icons.py          # Icon generator
├── README.md                  # Project overview
├── SETUP.md                   # Setup instructions
├── DOCUMENTATION.md           # This technical documentation
│
├── backend/                   # Python backend
│   ├── server.py              # Flask API server
│   ├── app.py                 # Application logic
│   ├── form_detector.py       # Form detection module
│   ├── form_scraper.py        # Form data scraper
│   ├── requirements.txt       # Python dependencies
│   └── data/                  # Data storage
│       └── forms.json         # Form templates
│
├── frontend/                  # Frontend assets
│   ├── css/
│   │   └── styles.css         # Extension styles
│   ├── js/
│   │   └── popup.js           # Popup functionality
│   └── icons/                 # Extension icons
│
├── data/                      # Shared data storage
│   └── forms.json             # Form data
│
└── icons/                     # Extension icons for manifest
``` 