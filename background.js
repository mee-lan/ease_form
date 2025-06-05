
const API_BASE_URL = 'http://127.0.0.1:5002/api';


function debounce(func, wait) {
  let timeout;
  return function(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Debounced version of field guidance update
const debouncedUpdateFieldGuidance = debounce((fieldName, formType) => {
  chrome.runtime.sendMessage({
    action: 'update_guidance',
    field_name: fieldName,
    form_type: formType
  }).catch(error => {
    // Popup might not be open, ignore this error
    if (!error.message.includes('receiving end does not exist')) {
      console.error('Error updating field guidance:', error);
    }
  });
}, 300); // 300ms debounce

// Track ongoing requests to prevent duplicates
let pendingGuidanceRequests = {};

// Listen for messages from content scripts or popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'field_focus') {
    // Handle when a form field is focused - use debounced version
    debouncedUpdateFieldGuidance(message.field_name, message.form_type);
  } else if (message.action === 'get_field_guidance') {
    // Create a unique key for this request
    const requestKey = `${message.field_name}_${message.form_type}_${message.language || 'default'}`;
    
    // Check if we already have a pending request for this exact field
    if (pendingGuidanceRequests[requestKey]) {
      console.log('Duplicate request detected, using existing promise');
      pendingGuidanceRequests[requestKey]
        .then(guidance => {
          sendResponse({ guidance: guidance });
        })
        .catch(error => {
          console.error('Error getting field guidance:', error);
          sendResponse({ guidance: 'Unable to get guidance for this field.' });
        });
    } else {
      // Create new request
      const guidancePromise = fetchFieldGuidance(message.field_name, message.form_type, message.language);
      pendingGuidanceRequests[requestKey] = guidancePromise;
      
      guidancePromise
        .then(guidance => {
          sendResponse({ guidance: guidance });
          // Clean up after request completes
          delete pendingGuidanceRequests[requestKey];
        })
        .catch(error => {
          console.error('Error getting field guidance:', error);
          sendResponse({ guidance: 'Unable to get guidance for this field.' });
          // Clean up after request fails
          delete pendingGuidanceRequests[requestKey];
        });
    }
    
    // Return true to indicate we will send a response asynchronously
    return true;
  } else if (message.action === 'helper_injected') {
    // Log that the helper was injected successfully
    console.log(`Form helper injected for ${message.form_type} with ${message.field_count} fields`);
  } else if (message.action === 'get_language') {
    // Get current language preference from API
    fetchLanguagePreference()
      .then(language => {
        sendResponse({ language: language });
      })
      .catch(error => {
        console.error('Error getting language preference:', error);
        sendResponse({ language: 'english' }); // Default to English on error
      });
      
    // Return true to indicate we will send a response asynchronously
    return true;
  }
});


function updateFieldGuidance(fieldName, formType) {

  debouncedUpdateFieldGuidance(fieldName, formType);
}

// Fetch language preference from API
async function fetchLanguagePreference() {
  try {
    const response = await fetch(`${API_BASE_URL}/language`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.language || 'english';
  } catch (error) {
    console.error('Error fetching language preference:', error);
    return 'english'; // Default to English on error
  }
}

// Fetch field guidance from API
async function fetchFieldGuidance(fieldName, formType, language = null) {
  try {
    // If language not provided, fetch it
    if (!language) {
      language = await fetchLanguagePreference();
    }
    
    const response = await fetch(`${API_BASE_URL}/field-guidance`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        field_name: fieldName,
        form_type: formType,
        language: language
      })
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.guidance;
  } catch (error) {
    console.error('Error fetching field guidance:', error);
    return 'Unable to get guidance for this field at the moment.';
  }
}

// Check if the Python backend is running
async function checkBackendStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/forms`);
    return response.ok;
  } catch (error) {
    return false;
  }
}

// Listen for tab updates to detect forms
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && tab.url.startsWith('http')) {
    // Check if the page contains a form
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      function: detectFormsOnPage,
    }).catch(error => {
      // Ignore errors for pages we can't inject into
      console.log('Could not inject script into this page.');
    });
  }
});

// Function to run in the content script context to detect forms
function detectFormsOnPage() {
  // Simple detection of forms
  const forms = document.querySelectorAll('form');
  const inputs = document.querySelectorAll('input:not([type="hidden"])');
  
  if (forms.length > 0 || inputs.length > 5) {
    // Page likely has a form, notify the background script
    chrome.runtime.sendMessage({
      action: 'form_detected',
      url: window.location.href,
      form_count: forms.length,
      input_count: inputs.length
    });
  }
}


checkBackendStatus().then(isRunning => {
  if (!isRunning) {
    console.warn('Backend server is not running. Some features may not work.');
  } else {
    console.log('Successfully connected to backend server.');
  }
}); 
