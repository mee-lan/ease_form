// Content script for Nepal Forms Assistant
// This script runs on the web page and interacts with forms

// Variables
let formHelper = null;
let currentFormType = null;
let formFields = {};
let activeField = null;

// Initialize
init();

function init() {
  // Listen for messages from the background script or popup
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'scan_for_forms') {
      // Scan the page for forms
      detectForms();
      sendResponse({ success: true });
    } else if (message.action === 'activate_helper') {
      // Activate the form helper
      activateFormHelper(message.form_type, message.fields);
      sendResponse({ success: true });
    }
    
    // Return true to indicate we're handling response asynchronously
    return true;
  });
  
  // Add document click handler to close tooltips when clicking outside
  document.addEventListener('click', function(event) {
    // Check if click is outside any form field or tooltip
    if (!event.target.closest('input, select, textarea, .nepal-forms-tooltip')) {
      // Close all tooltips
      closeAllTooltips();
    }
  });
  
  // Automatically scan for forms when page loads
  detectForms();
}

// Function to detect forms on the page
function detectForms() {
  // Collect page HTML
  const pageHTML = document.documentElement.outerHTML;
  
  // Send to backend for processing
  fetch('http://localhost:5000/api/detect-form', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      html: pageHTML
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.detected) {
      currentFormType = data.form_type;
      formFields = data.form_fields;
      
      // Notify the extension popup about detected form
      chrome.runtime.sendMessage({
        action: 'form_detected',
        form_type: currentFormType,
        form_fields: formFields
      });
      
      // Automatically add field helpers
      addFieldHelpers();
    }
  })
  .catch(error => {
    console.error('Error detecting form:', error);
  });
}

// Add helpers to form fields
function addFieldHelpers() {
  // Create styles for form field highlights and tooltips
  addHelperStyles();
  
  // Find all input fields, select dropdowns, and textareas
  const inputs = document.querySelectorAll('input:not([type="hidden"]), select, textarea');
  
  inputs.forEach(input => {
    // Skip submit buttons
    if (input.type === 'submit' || input.type === 'button') return;
    
    // Add event listeners
    input.addEventListener('focus', onFieldFocus);
    input.addEventListener('blur', onFieldBlur);
  });
  
  // Add floating helper button
  addFloatingHelper();
}

// Event handler for field focus
function onFieldFocus(event) {
  const field = event.target;
  activeField = field;
  
  // Highlight the field
  field.classList.add('nepal-forms-highlight');
  
  // Get field information
  const fieldName = field.name || field.id || 'unknown';
  
  // Request guidance for this field
  chrome.runtime.sendMessage({
    action: 'get_field_guidance',
    field_name: fieldName,
    form_type: currentFormType
  }, response => {
    if (!response || !response.guidance) return;
    
    // Show guidance tooltip
    showGuidanceTooltip(field, response.guidance);
  });
}

// Event handler for field blur (losing focus)
function onFieldBlur(event) {
  const field = event.target;
  
  // Remove highlight
  field.classList.remove('nepal-forms-highlight');
  
  // Hide tooltip (delayed to allow clicking)
  setTimeout(() => {
    if (field.guidanceTooltip && !field.guidanceTooltip.contains(document.activeElement)) {
      field.guidanceTooltip.remove();
      field.guidanceTooltip = null;
    }
  }, 200);
  
  activeField = null;
}

// Show guidance tooltip for a field
function showGuidanceTooltip(field, guidance) {
  // Remove existing tooltip if any
  if (field.guidanceTooltip) {
    field.guidanceTooltip.remove();
  }
  
  // Create tooltip element
  const tooltip = document.createElement('div');
  tooltip.className = 'nepal-forms-tooltip';
  
  // Create tooltip content
  const content = document.createElement('div');
  content.innerHTML = `<p>${guidance}</p>`;
  tooltip.appendChild(content);
  
  // Add a chat button
  const chatButton = document.createElement('button');
  chatButton.className = 'nepal-forms-chat-btn';
  chatButton.textContent = 'Ask More Questions';
  chatButton.addEventListener('click', () => {
    // Open popup with chat focused on this field
    chrome.runtime.sendMessage({
      action: 'open_chat',
      field_name: field.name || field.id || 'unknown',
      form_type: currentFormType
    });
  });
  tooltip.appendChild(chatButton);
  
  // Position the tooltip near the field
  const fieldRect = field.getBoundingClientRect();
  tooltip.style.position = 'absolute';
  tooltip.style.left = `${fieldRect.left}px`;
  tooltip.style.top = `${fieldRect.bottom + window.scrollY + 5}px`;
  tooltip.style.zIndex = '10000';
  
  // Add the tooltip to the page
  document.body.appendChild(tooltip);
  
  // Store reference to the tooltip
  field.guidanceTooltip = tooltip;
}

// Add floating helper button
function addFloatingHelper() {
  // Create floating helper button
  const helper = document.createElement('div');
  helper.className = 'nepal-forms-floating-helper';
  helper.innerHTML = `
    <div class="nepal-forms-helper-header">
      <span>Nepal Forms Assistant</span>
      <button class="nepal-forms-helper-close">&times;</button>
    </div>
    <div class="nepal-forms-helper-body">
      <p>Need help with this ${currentFormType} form?</p>
      <button class="nepal-forms-helper-chat">Ask Assistant</button>
    </div>
  `;
  
  // Add styles
  helper.style.position = 'fixed';
  helper.style.bottom = '20px';
  helper.style.right = '20px';
  helper.style.width = '250px';
  helper.style.backgroundColor = '#fff';
  helper.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.2)';
  helper.style.borderRadius = '8px';
  helper.style.zIndex = '10000';
  helper.style.padding = '15px';
  helper.style.fontFamily = 'Arial, sans-serif';
  
  // Add event listener for close button
  const closeButton = helper.querySelector('.nepal-forms-helper-close');
  closeButton.addEventListener('click', () => {
    helper.remove();
    formHelper = null;
  });
  
  // Add event listener for chat button
  const chatButton = helper.querySelector('.nepal-forms-helper-chat');
  chatButton.addEventListener('click', () => {
    chrome.runtime.sendMessage({
      action: 'open_chat',
      form_type: currentFormType
    });
  });
  
  // Add to page
  document.body.appendChild(helper);
  formHelper = helper;
}

// Add necessary styles to the page
function addHelperStyles() {
  const styles = document.createElement('style');
  styles.textContent = `
    .nepal-forms-highlight {
      border: 2px solid #e63946 !important;
      box-shadow: 0 0 5px rgba(230, 57, 70, 0.5) !important;
      transition: all 0.3s ease;
    }
    
    .nepal-forms-tooltip {
      background-color: #f1faee;
      border: 1px solid #457b9d;
      border-radius: 6px;
      padding: 12px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
      max-width: 300px;
      font-family: Arial, sans-serif;
      font-size: 14px;
      line-height: 1.5;
      color: #1d3557;
    }
    
    .nepal-forms-tooltip p {
      margin: 0 0 10px 0;
    }
    
    .nepal-forms-chat-btn {
      background-color: #457b9d;
      color: white;
      border: none;
      border-radius: 4px;
      padding: 6px 12px;
      cursor: pointer;
      font-size: 12px;
      display: block;
      margin-top: 8px;
    }
    
    .nepal-forms-chat-btn:hover {
      background-color: #3d6987;
    }
    
    .nepal-forms-helper-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      padding-bottom: 8px;
      border-bottom: 1px solid #ddd;
      font-weight: bold;
      color: #1d3557;
    }
    
    .nepal-forms-helper-close {
      background: none;
      border: none;
      font-size: 20px;
      cursor: pointer;
      color: #666;
    }
    
    .nepal-forms-helper-body {
      font-size: 14px;
    }
    
    .nepal-forms-helper-chat {
      background-color: #e63946;
      color: white;
      border: none;
      border-radius: 4px;
      padding: 8px 16px;
      cursor: pointer;
      font-size: 14px;
      display: block;
      margin-top: 10px;
      width: 100%;
    }
    
    .nepal-forms-helper-chat:hover {
      background-color: #d1323e;
    }
  `;
  
  document.head.appendChild(styles);
}

// Activate the form helper with field information
function activateFormHelper(formType, fields) {
  currentFormType = formType;
  formFields = fields;
  
  // Add helpers to form fields
  addFieldHelpers();
}

// Send form field guidance request
function requestFieldGuidance(fieldName) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage({
      action: 'get_field_guidance',
      field_name: fieldName,
      form_type: currentFormType
    }, response => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve(response?.guidance || 'No guidance available for this field.');
      }
    });
  });
}

// Listen for context menu click
document.addEventListener('contextmenu', event => {
  // Check if clicked on form field
  if (event.target.tagName === 'INPUT' || 
      event.target.tagName === 'SELECT' || 
      event.target.tagName === 'TEXTAREA') {
    
    // Mark this field for context menu
    activeField = event.target;
  }
}); 