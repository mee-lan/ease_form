// Configuration
const API_BASE_URL = 'http://127.0.0.1:5002/api';
let currentFormContext = null;
let currentLanguage = 'english'; // Default language

// Add Nepali translations for form names
const formTranslations = {
  'citizenship': {
    name: 'नागरिकता प्रमाणपत्र',
    requirements: [
      'दुई वटा पासपोर्ट साइजको फोटो',
      'जन्म दर्ता प्रमाणपत्र',
      'बुवा र आमाको नागरिकता प्रमाणपत्र (फोटोकपी)',
      'स्थानीय प्राधिकरणबाट चरित्र प्रमाणपत्र',
      'जग्गा मालिकी प्रमाणपत्र वा नाता प्रमाणपत्र'
    ],
    process: [
      'नागरिकता आवेदन फारम भर्नुहोस्',
      'आफ्नो जिल्ला प्रशासन कार्यालयमा आवेदन पेश गर्नुहोस्',
      'आवश्यक परेमा अन्तरवार्ता दिनुहोस्',
      'नागरिकता प्रमाणपत्र प्राप्त गर्नुहोस्'
    ],
    locations: [
      'आफ्नो जिल्लाको जिल्ला प्रशासन कार्यालय (जिप्राका)',
      'केही स्थानहरूमा क्षेत्र प्रशासन कार्यालय'
    ],
    contact: 'आफ्नो क्षेत्रको विशेष आवश्यकताहरूको लागि आफ्नो स्थानीय जिल्ला प्रशासन कार्यालयमा सम्पर्क गर्नुहोस्'
  },
  'passport': {
    name: 'राहदानी',
    requirements: [
      'नागरिकता प्रमाणपत्र (मूल र फोटोकपी)',
      'हालको पासपोर्ट साइजको फोटोहरू (एमआरपी स्पेसिफिकेसन)',
      'भरिएको आवेदन फारम'
    ],
    process: [
      'नेपालपासपोर्ट.गोभ.नेपालमा अनलाइन आवेदन पेश गर्नुहोस्',
      'निर्दिष्ट बैंकमा शुल्क तिर्नुहोस्',
      'रसिद लिएर राहदानी विभाग वा जिल्ला प्रशासन कार्यालय जानुहोस्',
      'बायोमेट्रिक डाटा प्रदान गर्नुहोस्',
      'प्रक्रिया पूरा भएपछि राहदानी संकलन गर्नुहोस्'
    ],
    locations: [
      'राहदानी विभाग, नारायणहिटी, काठमाडौं',
      'नेपाल भरका जिल्ला प्रशासन कार्यालयहरू'
    ],
    contact: 'राहदानी विभाग: ०१-४४१६०१०, ०१-४४१६०११'
  },
  'driving-license': {
    name: 'सवारी चालक अनुमतिपत्र',
    requirements: [
      'नागरिकता प्रमाणपत्र (मूल र फोटोकपी)',
      'प्राधिकृत चिकित्सकबाट चिकित्सा प्रतिवेदन',
      'रक्त समूह प्रमाणपत्र',
      'फोटो सहित आवेदन फारम'
    ],
    process: [
      'www.dotm.gov.np मा अनलाइन दर्ता गर्नुहोस्',
      'निर्धारित मितिमा लिखित परीक्षा दिनुहोस्',
      'लिखित परीक्षा पास भएमा व्यावहारिक ड्राइभिङ परीक्षा दिनुहोस्',
      'शुल्क तिरेर अनुमतिपत्र संकलन गर्नुहोस्'
    ],
    locations: [
      'नेपाल भरका यातायात व्यवस्थापन कार्यालयहरू'
    ],
    contact: 'यातायात व्यवस्थापन विभाग: ०१-४४७४९२१'
  },
  'pan': {
    name: 'स्थायी लेखा नम्बर',
    requirements: [
      'नागरिकता प्रमाणपत्र (मूल र फोटोकपी)',
      'व्यवसाय दर्ता प्रमाणपत्र (यदि लागू)',
      'दुई वटा पासपोर्ट साइजको फोटो',
      'आवेदन फारम'
    ],
    process: [
      'प्यान दर्ता फारम भर्नुहोस्',
      'नजिकैको कर कार्यालयमा पेश गर्नुहोस्',
      'दर्ता शुल्क तिर्नुहोस्',
      'प्यान प्रमाणपत्र प्राप्त गर्नुहोस्'
    ],
    locations: [
      'नेपाल भरका आन्तरिक राजस्व कार्यालयहरू'
    ],
    contact: 'आन्तरिक राजस्व विभाग: ०१-४४१५८०२, ०१-४४१०३४०'
  },
  'nid': {
    name: 'राष्ट्रिय परिचयपत्र',
    requirements: [
      'नागरिकता प्रमाणपत्र (मूल र फोटोकपी)',
      'जन्म दर्ता प्रमाणपत्र',
      'हालको पासपोर्ट साइजको फोटोहरू',
      'भरिएको आवेदन फारम'
    ],
    process: [
      'आवेदन फारम भर्नुहोस्',
      'आवश्यक कागजातहरू लिएर राष्ट्रिय परिचयपत्र व्यवस्थापन केन्द्र जानुहोस्',
      'बायोमेट्रिक डाटा सहित औंला छाप र फोटो प्रदान गर्नुहोस्',
      'प्रक्रिया पूरा भएपछि राष्ट्रिय परिचयपत्र संकलन गर्नुहोस्'
    ],
    locations: [
      'राष्ट्रिय परिचयपत्र व्यवस्थापन केन्द्र, काठमाडौं',
      'जिल्ला प्रशासन कार्यालयहरू'
    ],
    contact: 'राष्ट्रिय परिचयपत्र व्यवस्थापन केन्द्र: ०१-४२११२१४'
  },
  'loksewa': {
    name: 'लोक सेवा आयोग दरखास्त फारम',
    requirements: [
      'नागरिकता प्रमाणपत्र (मूल र फोटोकपी)',
      'हालसालै खिचिएको पासपोर्ट साइजको फोटो २ प्रति',
      'शैक्षिक योग्यताका प्रमाणपत्रहरू (मूल र फोटोकपी)',
      'कार्य अनुभवको प्रमाणपत्र (आवश्यक भएमा)',
      'तालिम वा विशेष योग्यताका प्रमाणपत्रहरू (आवश्यक भएमा)',
      'समावेशी समूहको प्रमाणपत्र (आवश्यक भएमा)'
    ],
    process: [
      'लोक सेवा आयोगको वेबसाइट psc.gov.np मा गई अनलाइन दरखास्त फारम भर्नुहोस्',
      'आवश्यक कागजातहरू स्क्यान गरी अपलोड गर्नुहोस्',
      'तोकिएको परीक्षा दस्तुर अनलाइन भुक्तानी गर्नुहोस्',
      'दरखास्त फारमको प्रिन्ट कपी लिनुहोस्',
      'तोकिएको मितिमा प्रवेशपत्र डाउनलोड गर्नुहोस्'
    ],
    locations: [
      'लोक सेवा आयोग केन्द्रीय कार्यालय, अनामनगर',
      'लोक सेवा आयोगका क्षेत्रीय कार्यालयहरू',
      'लोक सेवा आयोगका अञ्चल कार्यालयहरू'
    ],
    contact: 'लोक सेवा आयोग: ०१-४७७१५२८, टोल फ्री नम्बर: १६६०-०१-५०५५५'
  }
};

// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
  // Template grid
  const templateGrid = document.getElementById('template-grid');
  
  // Language selector
  const languageSelector = document.getElementById('language-selector');
  
  // Form detail elements
  const formDetail = document.getElementById('form-detail');
  const backButton = document.getElementById('back-btn');
  const formTitle = document.getElementById('form-title');
  const requirementsList = document.getElementById('requirements-list');
  const processList = document.getElementById('process-list');
  const locationsList = document.getElementById('locations-list');
  const contactInfo = document.getElementById('contact-info');
  const formChatButton = document.getElementById('form-chat-btn');
  
  // Chat interface elements
  const chatInterface = document.getElementById('chat-interface');
  const chatBackButton = document.getElementById('chat-back-btn');
  const chatButton = document.getElementById('chat-btn');
  const chatMessages = document.getElementById('chat-messages');
  const chatInput = document.getElementById('chat-input');
  const chatSendButton = document.getElementById('chat-send-btn');
  
  // Form helper elements
  const formHelper = document.getElementById('form-helper');
  const helperCloseButton = document.getElementById('helper-close-btn');
  const helperChatButton = document.getElementById('helper-chat-btn');
  const detectedForm = document.getElementById('detected-form');
  const fieldGuidance = document.getElementById('field-guidance');
  
  // Add debug info
  checkServerConnectivity();
  
  // Load current language preference
  loadLanguagePreference();
  
  // Load form templates
  loadFormTemplates();
  
  // Check if there is a form on the current page
  checkCurrentPageForForm();
  
  // Event Listeners
  backButton.addEventListener('click', showTemplateGrid);
  chatBackButton.addEventListener('click', () => {
    if (currentFormContext) {
      showFormDetail(currentFormContext);
    } else {
      showTemplateGrid();
    }
  });
  
  chatButton.addEventListener('click', () => {
    showChatInterface();
  });
  
  formChatButton.addEventListener('click', () => {
    showChatInterface();
  });
  
  chatSendButton.addEventListener('click', sendChatMessage);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      sendChatMessage();
    }
  });
  
  helperCloseButton.addEventListener('click', () => {
    formHelper.classList.add('hidden');
  });
  
  helperChatButton.addEventListener('click', () => {
    showChatInterface();
  });
  
  // Language toggle
  languageSelector.addEventListener('change', function() {
    const language = this.value;
    if (language === currentLanguage) {
      console.log('Language unchanged, skipping update');
      return; // No change
    }
    
    console.log(`Language changing from ${currentLanguage} to ${language}`);
    currentLanguage = language; // Update immediately
    updateUILanguage(); // Update UI immediately
    
    // Send the update to the server
    setLanguagePreference(language);
  });
  
  // Functions
  function checkServerConnectivity() {
    console.log('Checking server connectivity...');
    fetch(`${API_BASE_URL}/status`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Server status:', data);
        // Add a debug message to the page
        const debugInfo = document.createElement('div');
        debugInfo.className = 'debug-info';
        debugInfo.style.fontSize = '10px';
        debugInfo.style.color = '#666';
        debugInfo.style.marginTop = '10px';
        debugInfo.textContent = `Connected to server: ${data.status}, Mode: ${data.mode}`;
        document.querySelector('footer').appendChild(debugInfo);
      })
      .catch(error => {
        console.error('Server connectivity error:', error);
        // Add error info to the page
        const debugInfo = document.createElement('div');
        debugInfo.className = 'debug-info error';
        debugInfo.style.fontSize = '10px';
        debugInfo.style.color = 'red';
        debugInfo.style.marginTop = '10px';
        debugInfo.textContent = `Connection error: ${error.message}. Check API_BASE_URL: ${API_BASE_URL}`;
        document.querySelector('footer').appendChild(debugInfo);
      });
  }
  
  function loadLanguagePreference() {
    console.log('Loading language preference from server...');
    fetch(`${API_BASE_URL}/language`)
      .then(response => response.json())
      .then(data => {
        console.log('Received language preference:', data);
        
        // Only update if language has changed
        if (currentLanguage !== data.language) {
          currentLanguage = data.language;
          console.log('Set current language to:', currentLanguage);
          
          // Update the dropdown
          languageSelector.value = currentLanguage;
          
          // Update UI with new language
          updateUILanguage();
        } else {
          console.log('Language unchanged, keeping current settings');
        }
      })
      .catch(error => {
        console.error('Error loading language preference:', error);
      });
  }
  
  function setLanguagePreference(language) {
    console.log('Setting language preference to:', language);
    fetch(`${API_BASE_URL}/language`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        language: language
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Language preference updated:', data);
      
      // Reload the current view to apply language changes
      if (currentFormContext) {
        loadFormDetail(currentFormContext);
      } else {
        loadFormTemplates();
      }
    })
    .catch(error => {
      console.error('Error setting language preference:', error);
    });
  }
  
  function updateUILanguage() {
    // Update UI elements based on language preference
    console.log('Updating UI for language:', currentLanguage);
    const chatInput = document.getElementById('chat-input');
    const chatSendButton = document.getElementById('chat-send-btn');
    const backButtons = document.querySelectorAll('.back-btn');
    
    if (currentLanguage === 'nepali') {
      // Main interface
      document.querySelector('.form-templates h2').textContent = 'फारम प्रकार छान्नुहोस्';
      document.querySelector('.help-section h3').textContent = 'थप मद्दत चाहिन्छ?';
      
      // Chat buttons
      document.getElementById('chat-btn').textContent = 'सहायकसँग कुरा गर्नुहोस्';
      document.getElementById('form-chat-btn').textContent = 'सहायकलाई सोध्नुहोस्';
      document.getElementById('helper-chat-btn').textContent = 'मद्दतको लागि सोध्नुहोस्';
      
      // Back buttons
      backButtons.forEach(btn => {
        btn.innerHTML = '&larr; फर्कनुहोस्';
      });
      
      // Form details
      document.querySelector('#form-detail h2').textContent = 'फारम विवरण';
      document.querySelectorAll('.detail-section h3')[0].textContent = 'आवश्यकताहरू';
      document.querySelectorAll('.detail-section h3')[1].textContent = 'प्रक्रिया';
      document.querySelectorAll('.detail-section h3')[2].textContent = 'स्थानहरू';
      document.querySelectorAll('.detail-section h3')[3].textContent = 'सम्पर्क जानकारी';
      document.querySelector('.questions-section h3').textContent = 'यस फारमको बारेमा प्रश्न छ?';
      
      // Chat interface
      document.querySelector('#chat-interface h2').textContent = 'सहायकसँग कुरा गर्नुहोस्';
      chatInput.placeholder = 'यहाँ आफ्नो प्रश्न सोध्नुहोस्...';
      chatSendButton.textContent = 'पठाउनुहोस्';
    } else {
      // Main interface
      document.querySelector('.form-templates h2').textContent = 'Choose Form Type';
      document.querySelector('.help-section h3').textContent = 'Need additional help?';
      
      // Chat buttons
      document.getElementById('chat-btn').textContent = 'Chat with Assistant';
      document.getElementById('form-chat-btn').textContent = 'Ask Assistant';
      document.getElementById('helper-chat-btn').textContent = 'Ask for Help';
      
      // Back buttons
      backButtons.forEach(btn => {
        btn.innerHTML = '&larr; Back';
      });
      
      // Form details
      document.querySelector('#form-detail h2').textContent = 'Form Details';
      document.querySelectorAll('.detail-section h3')[0].textContent = 'Requirements';
      document.querySelectorAll('.detail-section h3')[1].textContent = 'Process';
      document.querySelectorAll('.detail-section h3')[2].textContent = 'Locations';
      document.querySelectorAll('.detail-section h3')[3].textContent = 'Contact Information';
      document.querySelector('.questions-section h3').textContent = 'Have questions about this form?';
      
      // Chat interface
      document.querySelector('#chat-interface h2').textContent = 'Chat with Assistant';
      chatInput.placeholder = 'Ask your question here...';
      chatSendButton.textContent = 'Send';
    }
    
    // Update welcome message in chat interface if visible
    if (!chatInterface.classList.contains('hidden')) {
      // Remove old welcome message and add new one
      chatMessages.innerHTML = '';
      addWelcomeMessage();
    }

    // Reload templates to show translations
    if (!templateGrid.parentElement.classList.contains('hidden')) {
      loadFormTemplates();
    }
    
    // Update form details if currently showing a form
    if (!formDetail.classList.contains('hidden') && currentFormContext) {
      loadFormDetail(currentFormContext);
    }
  }
  
  function loadFormTemplates() {
    console.log('Loading form templates with current language:', currentLanguage);
    
    // Show loading state
    templateGrid.innerHTML = '<div class="loading">Loading form templates...</div>';
    
    fetch(`${API_BASE_URL}/forms`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(forms => {
        console.log('Received forms data:', forms);
        templateGrid.innerHTML = '';
        
        if (!forms || forms.length === 0) {
          templateGrid.innerHTML = `
            <div class="error">
              <p>No form templates found.</p>
              <p>Make sure the backend server is properly initialized.</p>
            </div>
          `;
          return;
        }
        
        forms.forEach(form => {
          const templateItem = document.createElement('div');
          templateItem.className = 'template-item';
          templateItem.dataset.formId = form.id;
          
          // Use translated form name for Nepali language
          const formName = currentLanguage === 'nepali' && formTranslations[form.id] 
            ? formTranslations[form.id].name 
            : form.name;
            
          // Translate requirements text for Nepali language
          const requirementsText = currentLanguage === 'nepali' 
            ? `${form.requirements.length} आवश्यकताहरू` 
            : `${form.requirements.length} requirements`;
          
          console.log(`Form ${form.id} translated: ${form.name} -> ${formName}`);
            
          templateItem.innerHTML = `
            <h3>${formName}</h3>
            <p>${requirementsText}</p>
          `;
          
          templateItem.addEventListener('click', () => {
            loadFormDetail(form.id);
          });
          
          templateGrid.appendChild(templateItem);
        });
        
        // Add "More" option for chat
        const moreItem = document.createElement('div');
        moreItem.className = 'template-item';
        
        // Translate "More" text for Nepali language
        const moreTitle = currentLanguage === 'nepali' ? 'अरू...' : 'More...';
        const moreText = currentLanguage === 'nepali' ? 'अन्य फारमहरू र मद्दत' : 'Other forms and help';
        
        moreItem.innerHTML = `
          <h3>${moreTitle}</h3>
          <p>${moreText}</p>
        `;
        
        moreItem.addEventListener('click', () => {
          showChatInterface();
        });
        
        templateGrid.appendChild(moreItem);
      })
      .catch(error => {
        console.error('Error loading form templates:', error);
        templateGrid.innerHTML = `
          <div class="error">
            <p>Failed to load form templates: ${error.message}</p>
            <p>Make sure the backend server is running at ${API_BASE_URL}</p>
            <p>Check the console for more details.</p>
          </div>
        `;
      });
  }
  
  function loadFormDetail(formId) {
    fetch(`${API_BASE_URL}/form/${formId}`)
      .then(response => response.json())
      .then(form => {
        // Store current form context
        currentFormContext = form.id;
        
        // Update form details with translations if in Nepali
        const translations = formTranslations[form.id];
        formTitle.textContent = currentLanguage === 'nepali' && translations 
          ? translations.name 
          : form.name;
        
        // Requirements
        requirementsList.innerHTML = '';
        const requirements = currentLanguage === 'nepali' && translations 
          ? translations.requirements 
          : form.requirements;
        requirements.forEach(req => {
          const li = document.createElement('li');
          li.textContent = req;
          requirementsList.appendChild(li);
        });
        
        // Process
        processList.innerHTML = '';
        const process = currentLanguage === 'nepali' && translations 
          ? translations.process 
          : form.process;
        process.forEach(step => {
          const li = document.createElement('li');
          li.textContent = step;
          processList.appendChild(li);
        });
        
        // Locations
        locationsList.innerHTML = '';
        const locations = currentLanguage === 'nepali' && translations 
          ? translations.locations 
          : form.locations;
        locations.forEach(location => {
          const li = document.createElement('li');
          li.textContent = location;
          locationsList.appendChild(li);
        });
        
        // Contact
        contactInfo.textContent = currentLanguage === 'nepali' && translations 
          ? translations.contact 
          : form.contact;
        
        // Show form detail view
        showFormDetail(form.id);
      })
      .catch(error => {
        console.error('Error loading form detail:', error);
        const errorMsg = currentLanguage === 'nepali'
          ? 'फारम विवरण लोड गर्दा त्रुटि भयो। कृपया फेरि प्रयास गर्नुहोस्।'
          : 'Failed to load form details. Please try again.';
        alert(errorMsg);
      });
  }
  
  function showTemplateGrid() {
    formDetail.classList.add('hidden');
    chatInterface.classList.add('hidden');
    templateGrid.parentElement.classList.remove('hidden');
    formHelper.classList.remove('hidden'); // Show the form helper section again
    currentFormContext = null;
  }
  
  function showFormDetail(formId) {
    formDetail.classList.remove('hidden');
    chatInterface.classList.add('hidden');
    templateGrid.parentElement.classList.add('hidden');
    currentFormContext = formId;
  }
  
  function showChatInterface() {
    chatInterface.classList.remove('hidden');
    formDetail.classList.add('hidden');
    templateGrid.parentElement.classList.add('hidden');
    formHelper.classList.add('hidden'); // Hide the form helper/detection section
    chatInput.focus();
    
    // Clear any existing messages
    if (chatMessages.children.length === 0) {
      // Add welcome message based on language
      addWelcomeMessage();
    }
  }
  
  function addWelcomeMessage() {
    // Create welcome message based on current language
    const welcomeHTML = currentLanguage === 'nepali' 
      ? `<div class="message bot-message">
           <p>नमस्ते! म तपाईंलाई सरकारी फारमहरू भर्न मद्दत गर्न सक्छु। कसरी सहयोग गर्न सक्छु?</p>
         </div>`
      : `<div class="message bot-message">
           <p>Hello! I can help you with filling government forms. How can I assist you?</p>
         </div>`;
    
    chatMessages.innerHTML = welcomeHTML;
  }
  
function sendChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addChatMessage(message, 'user');
    chatInput.value = '';
    
    console.log('Sending chat message with language:', currentLanguage);
    
    // Send message to API with language preference
    // Always use the preferred language for responses, regardless of input language
    fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: message,
        form_context: currentFormContext,
        // Force the response in the selected language
        language: currentLanguage
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Received chat response in language:', currentLanguage);
      // Preprocess bot response to remove "**" and replace bullet points with Unicode bullets
      let botMessage = data.response.replace(/\*\*/g, '');
      botMessage = botMessage.split('\n').map(line => {
        if (line.trim().startsWith('* ') || line.trim().startsWith('- ')) {
          return '• ' + line.trim().substring(2);
        }
        return line;
      }).join('\n');
      // Add bot response to chat
      addChatMessage(botMessage, 'bot');
    })
    .catch(error => {
      console.error('Error sending chat message:', error);
      // Provide error message in the user's selected language
      const errorMsg = currentLanguage === 'nepali'
        ? 'माफ गर्नुहोस्, मैले एउटा त्रुटि भेटाएँ। कृपया पछि फेरि प्रयास गर्नुहोस्।'
        : 'Sorry, I encountered an error. Please try again later.';
      addChatMessage(errorMsg, 'bot');
    });
  }
  
function addChatMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}-message`;
    
    const messageText = document.createElement('p');
    if (sender === 'bot') {
      // Remove markdown bold syntax "**" from bot messages
      message = message.replace(/\*\*/g, '');
      // Replace lines starting with "* " with line breaks
      // Convert message to HTML with <br> for new lines
      const lines = message.split('\n').map(line => {
        if (line.trim().startsWith('* ')) {
          return line.replace('* ', '') + '<br>';
        }
        return line + '<br>';
      });
      messageText.innerHTML = lines.join('');
    } else {
      messageText.textContent = message;
    }
    messageElement.appendChild(messageText);
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
  
  function checkCurrentPageForForm() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      if (tabs.length === 0) return;
      
      chrome.scripting.executeScript({
        target: {tabId: tabs[0].id},
        function: getPageHTML
      }, results => {
        if (!results || chrome.runtime.lastError) return;
        
        const html = results[0].result;
        
        // Send HTML to form detection API
        fetch(`${API_BASE_URL}/detect-form`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            html: html
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.detected) {
            // Show form helper and set form name in lowercase
            detectedForm.querySelector('.form-name').textContent = data.form_type.toUpperCase();
            formHelper.classList.remove('hidden');
            currentFormContext = data.form_type;
            
            // Inject form helper script into page
            chrome.scripting.executeScript({
              target: {tabId: tabs[0].id},
              function: injectFormHelper,
              args: [data.form_type, data.form_fields]
            });
          }
        })
        .catch(error => {
          console.error('Error detecting form:', error);
        });
      });
    });
  }
  
  function getPageHTML() {
    return document.documentElement.outerHTML;
  }
  
  function injectFormHelper(formType, formFields) {
    // This function runs in the context of the web page
    // It would add event listeners to form fields to provide guidance
    
    // Create helper styles
    const style = document.createElement('style');
    style.textContent = `
      .nepal-forms-highlight {
        border: 2px solid #e63946 !important;
        box-shadow: 0 0 5px rgba(230, 57, 70, 0.5) !important;
      }
      
      .nepal-forms-tooltip {
        position: absolute;
        background: #f1faee;
        border: 1px solid #457b9d;
        padding: 10px;
        border-radius: 4px;
        max-width: 300px;
        z-index: 10000;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
      }
    `;
    document.head.appendChild(style);
    
    // Find form fields
    const formElements = document.querySelectorAll('input, select, textarea');
    
    formElements.forEach(element => {
      // Skip hidden elements
      if (element.type === 'hidden' || element.style.display === 'none') return;
      
      element.addEventListener('focus', function(e) {
        // Highlight the element
        this.classList.add('nepal-forms-highlight');
        
        // Send field info to extension
        chrome.runtime.sendMessage({
          action: 'field_focus',
          field_name: this.name || this.id || 'Unknown field',
          form_type: formType
        });
        
        // Create tooltip with guidance
        const tooltip = document.createElement('div');
        tooltip.className = 'nepal-forms-tooltip';
        tooltip.textContent = 'Loading guidance...';
        
        // Position tooltip near the field
        const rect = this.getBoundingClientRect();
        tooltip.style.left = `${rect.left}px`;
        tooltip.style.top = `${rect.bottom + 5}px`;
        
        document.body.appendChild(tooltip);
        
        // Store tooltip reference on element
        this.nepaliFormsTooltip = tooltip;
        
        // Request guidance for this field
        chrome.runtime.sendMessage({
          action: 'get_field_guidance',
          field_name: this.name || this.id || 'Unknown field',
          form_type: formType
        }, response => {
          if (response && response.guidance) {
            tooltip.textContent = response.guidance;
          }
        });
      });
      
      element.addEventListener('blur', function() {
        // Remove highlight
        this.classList.remove('nepal-forms-highlight');
        
        // Remove tooltip
        if (this.nepaliFormsTooltip) {
          this.nepaliFormsTooltip.remove();
          this.nepaliFormsTooltip = null;
        }
      });
    });
    
    // Notify extension that helper is injected
    chrome.runtime.sendMessage({
      action: 'helper_injected',
      form_type: formType,
      field_count: formElements.length
    });
  }
  
  function displayFieldGuidance(fieldName) {
    // Get field guidance from API, including language
    fetch(`${API_BASE_URL}/field-guidance`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        field_name: fieldName,
        form_type: detectedFormType,
        // Always pass the current language preference
        language: currentLanguage
      })
    })
    .then(response => response.json())
    .then(data => {
      fieldGuidance.innerHTML = `
        <h4>${data.field_name}</h4>
        <p>${data.guidance}</p>
      `;
    })
    .catch(error => {
      console.error('Error getting field guidance:', error);
      // Provide error message in the user's selected language
      const errorMsg = currentLanguage === 'nepali'
        ? '<p>यस फिल्डको लागि मार्गदर्शन प्राप्त गर्दा त्रुटि।</p>'
        : '<p>Error getting guidance for this field.</p>';
      fieldGuidance.innerHTML = errorMsg;
    });
  }
}); 