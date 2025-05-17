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
  fetch('http://127.0.0.1:5002/api/detect-form', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      html: pageHTML
    })
  })
  .then(response => response.json())      //Converts {"x": 1} to { x: 1 }
  .then(data => {
    if (data.detected && typeof data.form_type === 'string') {
      currentFormType = data.form_type.toLowerCase(); // Normalize to lowercase
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
  // Close all existing tooltips
  closeAllTooltips();
  
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
  
  // Create a container for the buttons
  const buttonContainer = document.createElement('div');
  buttonContainer.style.display = 'flex';
  buttonContainer.style.justifyContent = 'space-between';
  buttonContainer.style.alignItems = 'center';
  buttonContainer.style.marginTop = '8px';

  // Add a chat button
  const chatButton = document.createElement('button');
  chatButton.className = 'nepal-forms-chat-btn';
  chatButton.textContent = 'Ask More Questions';
  chatButton.addEventListener('click', () => {
    chrome.runtime.sendMessage({
      action: 'open_chat',
      field_name: field.name || field.id || 'unknown',
      form_type: currentFormType
    });
  });

  // Add a close button
  const closeButton = document.createElement('button');
  closeButton.innerHTML = '&times;';
  closeButton.className = 'nepal-forms-tooltip-close';
  closeButton.style.background = 'none';
  closeButton.style.border = 'none';
  closeButton.style.fontSize = '18px';
  closeButton.style.cursor = 'pointer';
  closeButton.style.color = '#666';
  closeButton.style.marginLeft = '12px';
  closeButton.addEventListener('click', () => {
    tooltip.remove();
    field.guidanceTooltip = null;
  });

  // Add both buttons to the container
  buttonContainer.appendChild(chatButton);
  buttonContainer.appendChild(closeButton);

  // Add the button container to the tooltip
  tooltip.appendChild(buttonContainer);
  
  // Position the tooltip near the field
  const fieldRect = field.getBoundingClientRect();
  const margin = 16; // More space below the field
  let left = fieldRect.left + window.scrollX;

  // Temporarily add tooltip off-screen to measure its height
  tooltip.style.position = 'absolute';
  tooltip.style.left = '-9999px';
  tooltip.style.top = '-9999px';
  document.body.appendChild(tooltip);
  const tooltipRect = tooltip.getBoundingClientRect();

  // Default: show below the field
  let top = fieldRect.bottom + window.scrollY + margin;

  // If not enough space below, show above the field
  if (top + tooltipRect.height > window.scrollY + window.innerHeight) {
    top = fieldRect.top + window.scrollY - tooltipRect.height - margin;
    if (top < window.scrollY + margin) top = window.scrollY + margin;
  }

  // Prevent overflow right
  if (left + tooltipRect.width > window.scrollX + window.innerWidth) {
    left = window.scrollX + window.innerWidth - tooltipRect.width - margin;
    if (left < margin) left = margin;
  }

  // Set final position
  tooltip.style.left = `${left}px`;
  tooltip.style.top = `${top}px`;
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
      <p>Need help with this ${currentFormType ? currentFormType.toUpperCase() : 'UNKNOWN'} form?</p>
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
    // Close the floating helper
    helper.remove();
    formHelper = null;
    
    // Open chat
    chrome.runtime.sendMessage({
      action: 'open_chat',
      form_type: currentFormType
    }, (response) => {
      if (response && response.success) {
        console.log('Chat interface opened successfully');
      } else {
        console.error('Failed to open chat interface');
      }
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
      z-index: 10001 !important;
    }
    
    .nepal-forms-tooltip-close {
      opacity: 0.7;
      transition: opacity 0.2s;
    }
    
    .nepal-forms-tooltip-close:hover {
      opacity: 1;
    }
    
    .nepal-forms-tooltip-header {
      border-bottom: 1px solid #ddd;
      margin: -8px -8px 8px -8px;
      padding: 4px 8px;
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
    
    .nepal-forms-floating-helper {
      z-index: 10000 !important;
    }
  `;
  
  document.head.appendChild(styles);
}

// Activate the form helper with field information
function activateFormHelper(formType, fields) {
  if (typeof formType === 'string') {
    currentFormType = formType.toLowerCase(); // Normalize to lowercase
    formFields = fields;
    
    // Add helpers to form fields
    addFieldHelpers();
  }
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

function closeAllTooltips() {
  document.querySelectorAll('.nepal-forms-tooltip').forEach(tip => tip.remove());
}

function autofillFormFields() {
  chrome.storage.sync.get(['userDetails'], function(result) {
    if (result.userDetails) {
      const { name, phone, mobile, address } = result.userDetails;
      
      // Autofill logic
      document.querySelectorAll('input').forEach(input => {
        if (input.name.toLowerCase().includes('name')) {
          input.value = name;
        } else if (input.name.toLowerCase().includes('district')) {
          input.value = district;
        } else if (input.name.toLowerCase().includes('municipality')) {
          input.value = municipality;
        } else if (input.name.toLowerCase().includes('ward')) {
          input.value = ward;
        } else if (input.name.toLowerCase().includes('mobile')) {
          input.value = mobile;
        } else if (input.name.toLowerCase().includes('address')) {
          input.value = address;
        }
      });
    }
  });
} 