import re
from bs4 import BeautifulSoup

class FormDetector:
    """
    Class to detect and analyze government forms on websites.
    Used to provide context-aware guidance for form filling.
    """
    
    def __init__(self, api_key=None, api_caller=None):
        self.api_key = api_key
        self.api_caller = api_caller
        self.has_gemini = api_caller is not None
        
        if not self.has_gemini:
            print("Google Generative AI not available - using simplified form detection")
        
        # Nepali government form keywords
        self.form_keywords = [
            'citizenship', 'नागरिकता', 'passport', 'राहदानी',
            'driving license', 'सवारी चालक अनुमतिपत्र', 'pan', 'पान',
            'tax', 'कर', 'voter', 'मतदाता', 'lok sewa', 'लोक सेवा',
            'application form', 'आवेदन फारम', 'registration', 'दर्ता',
            'national id', 'राष्ट्रिय परिचयपत्र'
        ]
    
    def detect_form(self, html_content):
        """
        Detects if the page contains a government form
        Returns form type if detected, None otherwise
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text content
        text = soup.get_text()
        
        # Check for form fields
        form_elements = soup.find_all('form')
        input_elements = soup.find_all('input')
        
        # If no form or input elements, likely not a form page
        if len(form_elements) == 0 and len(input_elements) < 3:
            return None
            
        # Check for form keywords in text
        for keyword in self.form_keywords:
            if keyword.lower() in text.lower():
                return self._identify_form_type(text, soup)
        
        # If we have form elements but no keywords matched, use AI or pattern matching
        if len(form_elements) > 0 or len(input_elements) > 5:
            return self._identify_form_type(text, soup)
            
        return None
    
    def _identify_form_type(self, text, soup):
        """
        Uses pattern matching and AI to identify the specific form type
        """
        # Extract form titles and headers
        titles = [tag.get_text() for tag in soup.find_all(['h1', 'h2', 'h3', 'title'])]
        form_titles = ' '.join(titles)
        
        # Try pattern matching first
        if re.search(r'citizenship|नागरिकता', form_titles, re.IGNORECASE):
            return "citizenship"
        elif re.search(r'passport|राहदानी', form_titles, re.IGNORECASE):
            return "passport"
        elif re.search(r'driving|license|सवारी|चालक', form_titles, re.IGNORECASE):
            return "driving-license"
        elif re.search(r'pan|पान|permanent account', form_titles, re.IGNORECASE):
            return "pan"
        elif re.search(r'national id|राष्ट्रिय परिचयपत्र', form_titles, re.IGNORECASE):
            return "nid"
        elif re.search(r'lok sewa|लोक सेवा|public service', form_titles, re.IGNORECASE):
            return "loksewa"
        
        # Use AI for more complex identification if available
        if self.has_gemini and self.api_caller:
            try:
                prompt = f"""
                The following text is from a webpage that might contain a Nepali government form.
                Based on the text, identify if this is one of the following form types:
                - Citizenship (नागरिकता)
                - Passport (राहदानी)
                - Driving License (सवारी चालक अनुमतिपत्र)
                - PAN (Permanent Account Number)
                - National ID (राष्ट्रिय परिचयपत्र)
                - Lok Sewa (Public Service Commission application)
                
                If it's one of these forms, respond with just the form type in lowercase.
                If it's not one of these forms, respond with 'unknown'.
                
                Text: {form_titles[:1000]}
                """
                
                form_type = self.api_caller(prompt)
                if form_type:
                    form_type = form_type.strip().lower()
                    valid_types = ["citizenship", "passport", "driving-license", "pan", "nid", "loksewa"]
                    if form_type in valid_types:
                        return form_type
            except Exception as e:
                print(f"Error using AI for form identification: {e}")
                
        # Fall back to unknown if pattern matching and AI fail
        return "unknown"
    
    def extract_form_fields(self, html_content):
        """
        Extracts form fields from the page for automatic filling guidance
        Returns dict of field names and types
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        form_fields = {}
        for input_element in soup.find_all('input'):
            field_name = input_element.get('name', '')
            field_id = input_element.get('id', '')
            field_placeholder = input_element.get('placeholder', '')
            field_type = input_element.get('type', 'text')
            
            # Skip hidden or submit fields
            if field_type in ['hidden', 'submit', 'button']:
                continue
                
            # Use the most informative identifier
            identifier = field_name or field_id or field_placeholder
            if identifier:
                form_fields[identifier] = {
                    'type': field_type,
                    'label': self._find_label_for_field(soup, field_id, field_name)
                }
                
        return form_fields
    
    def _find_label_for_field(self, soup, field_id, field_name):
        """Find the label text for a form field"""
        # Try to find explicit label
        if field_id:
            label = soup.find('label', {'for': field_id})
            if label:
                return label.get_text().strip()
        
        # Try to find nearby text
        if field_name:
            # This is a simplified approach - in a real implementation 
            # we would use more sophisticated proximity detection
            nearby_text = soup.find('label', string=re.compile(field_name, re.IGNORECASE))
            if nearby_text:
                return nearby_text.get_text().strip()
        
        return ""
        
    def get_field_guidance(self, field_name, form_type, language='english'):
        """
        Get AI-generated guidance for filling a specific field in a form.
        
        Args:
            field_name (str): The name of the field to get guidance for
            form_type (str): The type of form being filled
            language (str): The language for the guidance (default: 'english')
        
        Returns:
            str: Guidance text for filling out the field
        """
        try:
            # Normalize field name for more consistent lookup
            field_display = field_name.replace('_', ' ').lower()
            
            # Only proceed with AI if we have access
            if self.has_gemini and self.api_caller:
                # Create a prompt for the AI based on language
                language = language.lower()
                
                if language == 'nepali':
                    prompt = f"""
                    नेपाली भाषामा सरकारी फारमको फिल्डको लागि विशिष्ट मार्गदर्शन प्रदान गर्नुहोस्।
                    
                    फारम प्रकार: {form_type}
                    फिल्ड नाम: "{field_display}"
                    
                    निर्देशन:
                    1. यो फिल्डमा के प्रविष्ट गर्नुपर्छ भन्ने बारे विशिष्ट जानकारी प्रदान गर्नुहोस्
                    2. निर्देशन छोटो (2-3 वाक्य) र स्पष्ट राख्नुहोस्
                    3. हरेक बुँदा "• " बाट सुरु गर्नुहोस्
                    4. यो फिल्डसँग सम्बन्धित कुनै महत्त्वपूर्ण जानकारी समावेश गर्नुहोस्
                    
                    अत्यन्त महत्त्वपूर्ण: तपाईंको उत्तर अनिवार्य रूपमा र पूर्ण रूपमा नेपाली भाषामा हुनुपर्छ।
                    """
                else:  # Default to English
                    prompt = f"""
                    Provide specific guidance for filling the "{field_display}" field in a {form_type} form.
                    
                    Instructions:
                    1. Be specific about what information should be entered in this field
                    2. Keep guidance brief (2-3 sentences) and clear
                    3. Start each point with "• "
                    4. Include any important considerations related to this field
                    
                    Keep your answer focused on practical guidance for filling this specific field.
                    """
                
                # Get AI-generated guidance
                guidance = self.api_caller(prompt)
                
                # Simple validation - check if it has bullet points and is not too short
                if guidance and '•' in guidance and len(guidance) > 20:
                    return guidance.strip()
            
            # If AI is not available or returns invalid response, use field-specific fallback
            return self._get_field_specific_fallback(field_display, form_type, language)
                
        except Exception as e:
            print(f"Error generating field guidance: {e}")
            # Generic fallback in case of error
            return self._get_field_specific_fallback(field_name, form_type, language)
            
    def _get_field_specific_fallback(self, field_name, form_type, language='english'):
        """
        Provides field-specific fallback guidance based on common field types
        
        Args:
            field_name (str): The name of the field
            form_type (str): The type of form being filled
            language (str): The language for the guidance
            
        Returns:
            str: Specific guidance for the field type
        """
        field_display = field_name.replace('_', ' ').lower()
        
        # Map common field types to more specific guidance
        if language == 'nepali':
            # Detect field type from the field name
            if any(name in field_display for name in ['name', 'नाम']):
                return "• कृपया आफ्नो पूरा नाम लेख्नुहोस्\n• थर पहिले र नाम पछि लेख्नुहोस्\n• नेपाली वा अङ्ग्रेजी दुवै भाषामा हुन सक्छ"
            elif any(name in field_display for name in ['address', 'ठेगाना']):
                return "• आफ्नो पूरा ठेगाना उल्लेख गर्नुहोस्\n• प्रदेश, जिल्ला र वडा नम्बर समावेश गर्नुहोस्\n• स्थायी ठेगाना र अस्थायी ठेगाना फरक भए दुवै उल्लेख गर्नुहोस्"
            elif any(name in field_display for name in ['phone', 'mobile', 'फोन', 'मोबाइल']):
                return "• आफ्नो मोबाइल नम्बर ९८ बाट सुरु गरी १० अङ्क लेख्नुहोस्\n• एउटा मात्र फोन नम्बर उल्लेख गर्नुहोस् जुन तपाईंले नियमित रूपमा प्रयोग गर्नुहुन्छ"
            elif any(name in field_display for name in ['email', 'ईमेल']):
                return "• आफ्नो सक्रिय ईमेल ठेगाना लेख्नुहोस्\n• ईमेल ठेगानामा @ चिन्ह अनिवार्य छ\n• मान्य ईमेल प्रदायक (जस्तै gmail.com) प्रयोग गर्नुहोस्"
            elif any(name in field_display for name in ['dob', 'birth', 'date', 'जन्म']):
                return "• जन्म मिति वि.सं. अनुसार (YYYY-MM-DD) फर्म्याटमा लेख्नुहोस्\n• अङ्ग्रेजी मितिमा रूपान्तरण गर्न सरकारी वेबसाइट प्रयोग गर्न सक्नुहुन्छ"
            elif any(name in field_display for name in ['father', 'बुवा']):
                return "• बुवाको पूरा नाम लेख्नुहोस्\n• थर पहिले र नाम पछि लेख्नुहोस्\n• नागरिकता अनुसारको नाम लेख्नुहोस्"
            elif any(name in field_display for name in ['mother', 'आमा']):
                return "• आमाको पूरा नाम लेख्नुहोस्\n• थर पहिले र नाम पछि लेख्नुहोस्\n• नागरिकता अनुसारको नाम लेख्नुहोस्"
            elif any(name in field_display for name in ['citizenship', 'नागरिकता']):
                return "• नागरिकता प्रमाणपत्र नम्बर लेख्नुहोस्\n• जारी जिल्ला र मिति पनि उल्लेख गर्नुहोस्\n• नम्बरहरू स्पष्ट र सही तरिकाले लेख्नुहोस्"
            elif any(name in field_display for name in ['photo', 'तस्वीर']):
                return "• हालसालै खिचिएको पासपोर्ट साइजको फोटो अपलोड गर्नुहोस्\n• फोटो स्पष्ट, सेतो पृष्ठभूमिमा र मुख प्रष्ट देखिने हुनुपर्छ"
            elif form_type == 'citizenship':
                return f"• कृपया नागरिकता फारमको लागि यो '{field_display}' फिल्डमा सही जानकारी प्रविष्ट गर्नुहोस्\n• यो जानकारी तपाईंको पहिचान प्रमाणित गर्न प्रयोग हुनेछ"
            elif form_type == 'passport':
                return f"• राहदानी (पासपोर्ट) आवेदनमा यो फिल्ड महत्त्वपूर्ण छ\n• कृपया प्रमाणपत्रहरूसँग मिल्ने गरी सही जानकारी भर्नुहोस्"
            elif form_type == 'driving-license':
                return f"• सवारी चालक अनुमतिपत्रको लागि यस फिल्डमा आवश्यक विवरण भर्नुहोस्\n• नागरिकता/राहदानी अनुसारको जानकारी प्रविष्ट गर्नुहोस्"
            else:
                return f"• कृपया यो {field_display} फिल्डमा सही जानकारी प्रविष्ट गर्नुहोस्।\n• यो फिल्ड {form_type} फारमको लागि महत्त्वपूर्ण छ।"
        else:
            # English fallbacks
            if any(name in field_display for name in ['name']):
                return "• Enter your full name as it appears on your identity documents\n• Use the format: Last name, First name\n• Use either English or Nepali"
            elif any(name in field_display for name in ['address']):
                return "• Enter your complete address\n• Include province, district, and ward number\n• Provide both permanent and temporary addresses if different"
            elif any(name in field_display for name in ['phone', 'mobile']):
                return "• Enter your 10-digit mobile number starting with 98\n• Provide only one phone number that you use regularly"
            elif any(name in field_display for name in ['email']):
                return "• Enter your active email address\n• Make sure it includes the @ symbol\n• Use a valid email provider (like gmail.com)"
            elif any(name in field_display for name in ['dob', 'birth', 'date']):
                return "• Enter date in Bikram Sambat (B.S.) format: YYYY-MM-DD\n• You can use government websites to convert from English calendar"
            elif any(name in field_display for name in ['father']):
                return "• Enter your father's full name as it appears on his citizenship\n• Use the format: Last name, First name"
            elif any(name in field_display for name in ['mother']):
                return "• Enter your mother's full name as it appears on her citizenship\n• Use the format: Last name, First name"
            elif any(name in field_display for name in ['citizenship']):
                return "• Enter your citizenship certificate number\n• Include issuing district and date\n• Write numbers clearly and accurately"
            elif any(name in field_display for name in ['photo']):
                return "• Upload a recent passport-size photo\n• Photo should be clear with white background and face clearly visible"
            elif form_type == 'citizenship':
                return f"• Please enter the correct information for this {field_display} field on the citizenship form\n• This information will be used to verify your identity"
            elif form_type == 'passport':
                return f"• This field is important for your passport application\n• Enter information exactly as it appears on your supporting documents"
            elif form_type == 'driving-license':
                return f"• Enter the required information for your driving license application\n• Information should match your citizenship/passport"
            else:
                return f"• Please enter the correct information for the {field_display} field.\n• Make sure it matches your official documents." 