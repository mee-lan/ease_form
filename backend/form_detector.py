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
        
    def get_field_guidance(self, field_name, form_type, language="english"):
        """
        Provide guidance for filling a specific field
        """
        # Simplified guidance as fallback
        form_guidance = {
            "citizenship": {
                "english": {
                    "name": "• Enter your full name as it appears on your birth certificate",
                    "address": "• Enter your permanent address registered in Nepal",
                    "dob": "• Enter your date of birth in BS (Bikram Sambat) format",
                    "father_name": "• Enter your father's full name",
                    "mother_name": "• Enter your mother's full name"
                },
                "nepali": {
                    "name": "• तपाईंको जन्म दर्ता प्रमाणपत्रमा भएको पूरा नाम लेख्नुहोस्",
                    "address": "• नेपालमा दर्ता भएको तपाईंको स्थायी ठेगाना लेख्नुहोस्",
                    "dob": "• तपाईंको जन्म मिति बि.स. (बिक्रम सम्बत) मा लेख्नुहोस्",
                    "father_name": "• तपाईंको बुवाको पूरा नाम लेख्नुहोस्",
                    "mother_name": "• तपाईंको आमाको पूरा नाम लेख्नुहोस्"
                }
            },
            "passport": {
                "english": {
                    "name": "• Enter your full name in CAPITAL LETTERS exactly as in your citizenship",
                    "address": "• Enter your permanent address as registered in your citizenship",
                    "phone": "• Enter your mobile number that's actively in use"
                },
                "nepali": {
                    "name": "• तपाईंको नागरिकतामा भएको जस्तै CAPITAL LETTERS मा पूरा नाम लेख्नुहोस्",
                    "address": "• तपाईंको नागरिकतामा दर्ता भएको स्थायी ठेगाना लेख्नुहोस्",
                    "phone": "• तपाईंको सक्रिय रूपमा प्रयोग भइरहेको मोबाइल नम्बर लेख्नुहोस्"
                }
            },
            "driving-license": {
                "english": {
                    "name": "• Enter your full name as it appears on your citizenship",
                    "blood_group": "• Enter your blood group (A+, B+, AB+, O+, A-, B-, AB-, O-)",
                    "vehicle_type": "• Select the type of vehicle you're applying for"
                },
                "nepali": {
                    "name": "• तपाईंको नागरिकतामा भएको पूरा नाम लेख्नुहोस्",
                    "blood_group": "• तपाईंको रक्त समूह लेख्नुहोस् (A+, B+, AB+, O+, A-, B-, AB-, O-)",
                    "vehicle_type": "• तपाईंले आवेदन दिन चाहेको सवारी साधनको प्रकार छान्नुहोस्"
                }
            },
            "pan": {
                "english": {
                    "name": "• Enter your full legal name as in your citizenship",
                    "address": "• Enter your current business or residence address",
                    "business_name": "• Enter your business name if applicable"
                },
                "nepali": {
                    "name": "• तपाईंको नागरिकतामा भएको पूरा कानूनी नाम लेख्नुहोस्",
                    "address": "• तपाईंको हालको व्यापार वा आवासीय ठेगाना लेख्नुहोस्",
                    "business_name": "• लागू भएमा तपाईंको व्यापारको नाम लेख्नुहोस्"
                }
            }
        }
        
        # Try AI-powered guidance if available
        if self.has_gemini and self.api_caller:
            try:
                # Add language instruction
                lang_instruction = ""
                if language.lower() == "nepali":
                    lang_instruction = "Provide your response in Nepali language. Use bullet points."
                else:
                    lang_instruction = "Provide your response in English. Use bullet points."
                
                prompt = f"""
                {lang_instruction}
                
                Provide simple guidance for filling out the "{field_name}" field 
                in a Nepali {form_type} form. Keep it very brief, 1-2 sentences only.
                Be specific about what information should go in this field.
                """
                
                guidance = self.api_caller(prompt)
                if guidance:
                    return guidance.strip()
            except Exception as e:
                print(f"Error using AI for field guidance: {e}")
        
        # Try to find guidance for this field in our fallback data
        lang = language.lower()
        if lang not in ["english", "nepali"]:
            lang = "english"  # Default to English if the language is not supported
            
        if form_type in form_guidance and field_name.lower() in form_guidance[form_type].get(lang, {}):
            return form_guidance[form_type][lang][field_name.lower()]
        
        # Generic fallback
        if lang == "nepali":
            return f"• तपाईंको {field_name} जानकारी भर्नुहोस्।"
        else:
            return f"• Fill in your {field_name} information." 