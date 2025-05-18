from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import sys
import requests
from form_detector import FormDetector
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the Gemini API
GEMINI_API_KEY = os.environ.get('NEPAL_FORMS_GEMINI_API_KEY')
GEMINI_MODEL = "gemini-1.5-flash"  # Model verified to exist

# Global language preference
DEFAULT_LANGUAGE = "english"

# Nepali translations for common responses - used in fallback
NEPALI_FALLBACK_CITIZENSHIP = """• नेपाली नागरिकता प्राप्त गर्नको लागि तपाईंले निम्न कदमहरू चाल्नु पर्दछ:

• आवश्यक कागजातहरू संकलन गर्नुहोस्:
  • जन्म दर्ता प्रमाणपत्र
  • बुवा/आमाको नागरिकता प्रमाणपत्रको प्रतिलिपि
  • हालसालै खिचिएको पासपोर्ट साइजको फोटोहरू (४ वटा)
  • स्थानीय वडा कार्यालयबाट सिफारिस पत्र
  • बसोबास प्रमाणपत्र

• प्रक्रिया:
  • स्थानीय वडा कार्यालयबाट सिफारिस लिनुहोस्
  • नागरिकता आवेदन फारम प्राप्त गर्नुहोस् र भर्नुहोस्
  • सबै आवश्यक कागजातहरू जिल्ला प्रशासन कार्यालयमा पेश गर्नुहोस्
  • आवश्यक भएमा अन्तरवार्ताको लागि उपस्थित हुनुहोस्
  • प्रक्रिया पूरा भएपछि नागरिकता प्रमाणपत्र संकलन गर्नुहोस्

• कार्यालय स्थानहरू:
  • तपाईंको जिल्लाको जिल्ला प्रशासन कार्यालय (DAO)
  • काठमाडौंको लागि, कार्यालय बाबरमहलमा अवस्थित छ

• समय र शुल्क:
  • शुल्क: अनिवार्य शुल्क लगभग रु. ५०० (यो परिवर्तन हुन सक्छ)
  • समय: प्रक्रिया सामान्यतया १-२ हप्ता लिन्छ, तर यो कार्यालयको कार्यबोझ अनुसार फरक हुन सक्छ

• महत्त्वपूर्ण सुझावहरू:
  • सबै कागजातहरूको फोटोकपी बनाई राख्नुहोस्
  • आवेदन दिनु अघि सबै कागजातहरू व्यवस्थित गर्नुहोस्
  • कुनै कागजात गुम्यो भने, तुरुन्तै सम्बन्धित कार्यालयमा रिपोर्ट गर्नुहोस्
  • आवश्यक परेमा कानूनी सल्लाहकारको सहयोग लिनुहोस्

थप जानकारीको लागि, कृपया तपाईंको नजिकको जिल्ला प्रशासन कार्यालयमा सम्पर्क गर्नुहोस्।"""

# Function to directly call Gemini API
def call_gemini_api(prompt, system_message=None, language="english", form_type=None, field_display=None):
    if not GEMINI_API_KEY:
        print("ERROR: NEPAL_FORMS_GEMINI_API_KEY environment variable not set. Cannot call Gemini API.")
        if language.lower() == "nepali":
            return "API कुञ्जी कन्फिगर गरिएको छैन। कृपया प्रशासकलाई सम्पर्क गर्नुहोस्।"
        else:
            return "API key is not configured. Please contact the administrator."

    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}

        # Combine system message and prompt for the API call
        if system_message:
            if language.lower() == "nepali":
                full_prompt = f"{system_message}\n\nप्रश्न: {prompt}"
            else:
                full_prompt = f"{system_message}\n\nQuestion: {prompt}"
        else:
            full_prompt = prompt

        contents = [
            {
                "parts": [{"text": full_prompt}],
                "role": "user"
            }
        ]
        
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": 1024
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                content = result["candidates"][0]["content"]
                if "parts" in content and len(content["parts"]) > 0:
                    return content["parts"][0]["text"]
        return None
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

# Check if Gemini API is available
has_gemini = False
try:
    # Test API with a simple call
    print("\n=== Testing Gemini API ===")
    print(f"API Key present: {bool(GEMINI_API_KEY)}")
    print(f"Model: {GEMINI_MODEL}")
    
    # Use a simple test prompt
    test_prompt = """
    You are a helpful assistant. Please respond with 'API is working' if you can read this message.
    This is a test to verify the API connection.
    """
    
    url = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    contents = [
        {
            "parts": [{"text": test_prompt}],
            "role": "user"
        }
    ]
    
    data = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.95,
            "topK": 40,
            "maxOutputTokens": 1024
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"Test API response status: {response.status_code}")
    print(f"Test API response body: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if "candidates" in result and len(result["candidates"]) > 0:
            content = result["candidates"][0]["content"]
            if "parts" in content and len(content["parts"]) > 0:
                result = content["parts"][0]["text"]
                print(f"Test API response: {result}")
                
                if "API is working" in result:
                    has_gemini = True
                    print("\n==================================================")
                    print("✅ Gemini API initialized successfully using direct API calls")
                    print("==================================================\n")
                    print("Server is running with FULL AI features enabled.")
                else:
                    raise Exception("Test API call failed - unexpected response")
            else:
                raise Exception("Test API call failed - no content parts")
        else:
            raise Exception("Test API call failed - no candidates")
    else:
        raise Exception(f"Test API call failed - status code {response.status_code}")
except Exception as e:
    print("\n==================================================")
    print(f"⚠️  RUNNING IN FALLBACK MODE - Gemini API not available: {e}")
    print("==================================================\n")
    print("The server is running in fallback mode without AI features.")
    print("This means:")
    print("  - Form detection works with basic pattern matching")
    print("  - Field guidance uses predefined templates")
    print("  - Chat responds with canned answers instead of AI-generated ones")
    print("\nTo enable AI features, check your API key and internet connection.")
    print("See README.md for details.\n")

# Create form detector (modified to use our API function)
form_detector = FormDetector(GEMINI_API_KEY, api_caller=call_gemini_api if has_gemini else None)

# Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def load_form_data():
    """Load form templates and guidance data"""
    forms_path = os.path.join(DATA_DIR, 'forms.json')
    if not os.path.exists(forms_path):
        return []
    with open(forms_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/api/status', methods=['GET'])
def get_status():
    """Return server status"""
    return jsonify({
        "status": "running", 
        "gemini_available": has_gemini,
        "mode": "AI-powered" if has_gemini else "fallback",
        "model": GEMINI_MODEL if has_gemini else None
    })

@app.route('/api/language', methods=['POST'])
def set_language():
    """Set the preferred language"""
    try:
        data = request.json
        language = data.get('language', DEFAULT_LANGUAGE)
        
        print(f"Setting language preference to: {language}")
        
        # Validate language (only accept 'english' or 'nepali')
        if language not in ['english', 'nepali']:
            language = DEFAULT_LANGUAGE
            print(f"Invalid language provided, defaulting to: {language}")
        
        # Store in a file so it persists across requests
        language_file = os.path.join(DATA_DIR, 'language_preference.json')
        with open(language_file, 'w', encoding='utf-8') as f:
            json.dump({"language": language}, f)
        
        print(f"Saved language preference to file: {language}")
        return jsonify({"status": "success", "language": language})
    except Exception as e:
        print(f"Error setting language: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/language', methods=['GET'])
def get_language():
    """Get the current language preference"""
    try:
        language_file = os.path.join(DATA_DIR, 'language_preference.json')
        if os.path.exists(language_file):
            with open(language_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                language = data.get("language", DEFAULT_LANGUAGE)
                print(f"Retrieved language preference: {language}")
                return jsonify({"language": language})
        print(f"No language preference found, using default: {DEFAULT_LANGUAGE}")
        return jsonify({"language": DEFAULT_LANGUAGE})
    except Exception as e:
        print(f"Error getting language: {str(e)}")
        return jsonify({"error": str(e)}), 500

def get_current_language():
    """Helper to get current language setting"""
    try:
        language_file = os.path.join(DATA_DIR, 'language_preference.json')
        if os.path.exists(language_file):
            with open(language_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                language = data.get("language", DEFAULT_LANGUAGE)
                print(f"Using language from settings: {language}")
                return language
        print(f"No language file found, using default: {DEFAULT_LANGUAGE}")
        return DEFAULT_LANGUAGE
    except Exception as e:
        print(f"Error in get_current_language: {str(e)}")
        return DEFAULT_LANGUAGE

@app.route('/api/forms', methods=['GET'])
def get_forms():
    """Return list of available form templates"""
    try:
        forms = load_form_data()
        return jsonify(forms)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/form/<form_id>', methods=['GET'])
def get_form_details(form_id):
    """Return details for a specific form"""
    try:
        forms = load_form_data()
        for form in forms:
            if form['id'] == form_id:
                return jsonify(form)
        return jsonify({"error": "Form not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/detect-form', methods=['POST'])
def detect_form():
    """Detect form type from HTML content"""
    try:
        data = request.json
        html_content = data.get('html', '')
        
        if not html_content:
            return jsonify({"error": "No HTML content provided"}), 400
            
        form_type = form_detector.detect_form(html_content)
        
        if not form_type:
            return jsonify({"detected": False})
            
        form_fields = form_detector.extract_form_fields(html_content)
        
        return jsonify({
            "detected": True,
            "form_type": form_type,
            "form_fields": form_fields
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/field-guidance', methods=['POST'])
def get_field_guidance():
    """Get guidance for filling a specific field"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Extract parameters
    field_name = data.get('field_name', '')
    form_type = data.get('form_type', '')
    language = data.get('language', 'english').lower()
    
    if not field_name or not form_type:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        # Delegate all guidance logic to FormDetector
        guidance = form_detector.get_field_guidance(field_name, form_type, language)
        return jsonify({'guidance': guidance})
    except Exception as e:
        print(f"Error getting field guidance: {e}")
        # Return a generic error message in the appropriate language
        error_msg = "• कृपया यो फिल्ड सावधानीपूर्वक भर्नुहोस्।" if language == "nepali" else "• Please fill this field carefully."
        return jsonify({'guidance': error_msg})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with the Gemini-powered assistant"""
    try:
        data = request.json
        user_message = data.get('message', '')
        form_context = data.get('form_context', None)
        
        # Get language from request payload first (priority)
        language = data.get('language', None)
        print(f"Chat request with language parameter: {language}")
        
        # If not specified in request, use the stored preference
        if not language:
            language = get_current_language()
            print(f"No language in request, using stored preference: {language}")
        
        # Validate language
        if language not in ['english', 'nepali']:
            language = DEFAULT_LANGUAGE
            print(f"Invalid language provided, defaulting to: {language}")
            
        print(f"Final language for chat response: {language}")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Special case for citizenship questions in Nepali - use direct fallback
        if language.lower() == "nepali" and any(term in user_message.lower() for term in 
                                            ["citizenship", "certificate", "how do i get", 
                                             "how to get", "obtain", "apply", "application",
                                             "document", "process"]):
            print("Direct citizenship question detected with Nepali response requested. Using pre-translated response.")
            return jsonify({"response": NEPALI_FALLBACK_CITIZENSHIP})
        
        if has_gemini:
            try:
                # Prepare context for the model
                if language.lower() == "nepali":
                    system_prompt = """
                    तपाईं नेपाली सरकारी फारमहरूमा सहयोग गर्ने सहायक हुनुहुन्छ।
                    तपाईंको उत्तर केवल नेपाली भाषामा, देवनागरी लिपिमा दिनुहोस्।
                    अंग्रेजी शब्दहरू प्रयोग नगर्नुहोस्।
                    प्रत्येक बुँदा "• " बाट सुरु गर्नुहोस्।
                    उत्तर छोटो र स्पष्ट राख्नुहोस् (१-२ वाक्य)।
                    सबै जानकारी नेपालीमा अनुवाद गर्नुहोस्।
                    """
                else:
                    system_prompt = """
                    You are an assistant helping non-tech-savvy users with Nepali governmental forms.
                    Provide simple, clear instructions and guidance for form filling.
                    Use simple language and avoid technical terms.
                    The response should be in point form not in paragraph.
                    Always provide accurate information about document requirements, office locations, and procedures.
                    YOU MUST RESPOND IN ENGLISH LANGUAGE ONLY. Do not use Nepali.
                    """
                
                prompt = user_message
                if form_context:
                    # Add form context if available
                    forms = load_form_data()
                    form_info = next((f for f in forms if f['id'] == form_context), None)
                    
                    if form_info:
                        # Extract relevant form info for context
                        if language.lower() == "nepali":
                            context_details = f"""
                            फारम: {form_info['name']}
                            आवश्यकताहरू: {', '.join(form_info['requirements'])}
                            प्रक्रिया: {', '.join(form_info['process'])}
                            स्थानहरू: {', '.join(form_info['locations'])}
                            सम्पर्क: {form_info['contact']}
                            """
                        else:
                            context_details = f"""
                            Form: {form_info['name']}
                            Requirements: {', '.join(form_info['requirements'])}
                            Process: {', '.join(form_info['process'])}
                            Locations: {', '.join(form_info['locations'])}
                            Contact: {form_info['contact']}
                            """
                        prompt = f"Context: User is filling a {form_info['name']} form.\nForm details: {context_details}\nQuestion: {user_message}"
                    else:
                        prompt = f"Context: User is filling a {form_context} form.\nQuestion: {user_message}"
                
                # Call Gemini API directly with language preference
                print(f"Calling Gemini API with language: {language}")
                
                # First attempt
                response_text = call_gemini_api(prompt, system_prompt, language)
                
                # Check if we need to force a retry with stronger language instructions
                if response_text:
                    is_nepali_text = any('\u0900' <= c <= '\u097F' for c in response_text)
                    
                    # If language is Nepali but response doesn't contain Nepali script
                    if language.lower() == "nepali" and not is_nepali_text:
                        print("Response not in Nepali despite request, trying one more time with stronger prompt")
                        
                        # Add a stronger instruction
                        reinforced_system_prompt = system_prompt + """
                        महत्त्वपूर्ण निर्देशन: तपाईंको उत्तर नेपाली भाषामा मात्र हुनुपर्छ।
                        सबै जानकारी नेपालीमा अनुवाद गर्नुहोस्।
                        अंग्रेजी प्रयोग नगर्नुहोस्।
                        प्रत्येक बुँदा "• " बाट सुरु गर्नुहोस्।
                        """
                        
                        # Retry with reinforced prompt
                        response_text = call_gemini_api(prompt, reinforced_system_prompt, language)
                        
                        # Check again
                        is_nepali_text = any('\u0900' <= c <= '\u097F' for c in response_text) if response_text else False
                        if not is_nepali_text:
                            print("Still not getting Nepali response, using fallback")
                            return get_fallback_response(user_message, language)
                    
                    # If language is English but response contains Nepali script
                    elif language.lower() == "english" and is_nepali_text:
                        print("Response not in English despite request, trying one more time")
                        
                        # Add a stronger instruction
                        reinforced_system_prompt = system_prompt + """
                        CRITICAL INSTRUCTION: Your response MUST be in English only.
                        DO NOT use Nepali script in your response at all.
                        """
                        
                        # Retry with reinforced prompt
                        response_text = call_gemini_api(prompt, reinforced_system_prompt, language)
                        
                        # Check again
                        is_nepali_text = any('\u0900' <= c <= '\u097F' for c in response_text) if response_text else False
                        if is_nepali_text:
                            print("Still getting Nepali in English response, using fallback")
                            return get_fallback_response(user_message, language)
                    
                    print(f"Got valid response from Gemini in {language}")
                    return jsonify({"response": response_text})
                else:
                    # Fall through to fallback if API call failed
                    print("API call returned no result, using fallback")
                    return get_fallback_response(user_message, language)
            except Exception as e:
                print(f"Error using Gemini API: {e}")
                # Fall through to fallback responses
                return get_fallback_response(user_message, language)
        
        # If Gemini not available, use fallback
        return get_fallback_response(user_message, language)
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500
        
def get_fallback_response(user_message, language):
    """Get fallback response based on language and query"""
    print(f"Getting fallback response in {language}")
    
    if language.lower() == "nepali":
        # Nepali fallback responses
        if "requirements" in user_message.lower() or "need" in user_message.lower() or "document" in user_message.lower():
            response_text = NEPALI_FALLBACK_CITIZENSHIP
        elif "process" in user_message.lower() or "step" in user_message.lower() or "how" in user_message.lower():
            response_text = """• नागरिकताको प्रक्रिया:
• स्थानीय वडा कार्यालयबाट सिफारिस लिनुहोस्
• आवेदन फारम भर्नुहोस्
• जिल्ला प्रशासन कार्यालयमा कागजातहरू पेश गर्नुहोस्
• अन्तरवार्ता दिनुहोस्
• नागरिकता प्रमाणपत्र संकलन गर्नुहोस्"""
        elif "where" in user_message.lower() or "location" in user_message.lower() or "office" in user_message.lower():
            response_text = """• तपाईंले आफ्नो जिल्ला प्रशासन कार्यालयमा आवेदन दिन सक्नुहुन्छ
• काठमाडौंको लागि, कार्यालय बाबरमहलमा छ"""
        elif "cost" in user_message.lower() or "fee" in user_message.lower() or "price" in user_message.lower() or "money" in user_message.lower():
            response_text = """• नागरिकता प्रमाणपत्रको शुल्क न्यून छ (लगभग रु ५००)
• राहदानी शुल्क फरक-फरक छ:
• नियमित प्रक्रियाको लागि रु ५,०००
• द्रुत सेवाको लागि रु १०,०००"""
        elif "time" in user_message.lower() or "duration" in user_message.lower() or "long" in user_message.lower():
            response_text = """• प्रक्रिया समय फरक-फरक हुन्छ:
• नागरिकता सामान्यतया १-२ हप्ता लिन्छ
• राहदानी नियमित प्रक्रियामा ३-४ हप्ता लाग्छ
• सवारी चालक अनुमति परीक्षा पास गरेपछि ४-६ हप्ता लाग्छ"""
        else:
            response_text = """• म हाल सीमित क्षमताहरूसहित चलिरहेको छु।
• मैले नेपाली सरकारी फारामहरूको बारेमा निम्न जानकारी प्रदान गर्न सक्छु:
  • आवश्यक कागजातहरू
  • प्रक्रियाहरू
  • कार्यालय स्थानहरू
  • लागत र शुल्क
  • प्रक्रिया समय
• कृपया यी विषयहरू सम्बन्धी प्रश्नहरू सोध्नुहोस्।"""
    else:
        # English fallback responses in bullet points
        if "requirements" in user_message.lower() or "need" in user_message.lower() or "document" in user_message.lower():
            response_text = """• For Nepali citizenship, you need:
• Birth certificate
• Father/mother's citizenship certificate
• Recent passport photos
• Ward recommendation letter"""
        elif "process" in user_message.lower() or "step" in user_message.lower() or "how" in user_message.lower():
            response_text = """• Citizenship process:
• Get a recommendation from your local ward office
• Fill application form
• Submit documents at District Administration Office
• Attend the interview
• Collect your citizenship certificate"""
        elif "where" in user_message.lower() or "location" in user_message.lower() or "office" in user_message.lower():
            response_text = """• You can apply at your District Administration Office (DAO)
• For Kathmandu, the office is at Babar Mahal"""
        elif "cost" in user_message.lower() or "fee" in user_message.lower() or "price" in user_message.lower() or "money" in user_message.lower():
            response_text = """• Citizenship certificate fee is minimal (around NPR 500)
• Passport fees vary:
• NPR 5,000 for regular processing
• NPR 10,000 for expedited service"""
        elif "time" in user_message.lower() or "duration" in user_message.lower() or "long" in user_message.lower():
            response_text = """• Processing times vary:
• Citizenship usually takes 1-2 weeks
• Passport takes 3-4 weeks for regular processing
• Driving license takes 4-6 weeks after passing the test"""
        else:
            response_text = """• I'm running with limited capabilities.
• I can answer questions about Nepali government forms, including:
  • Required documents
  • Procedures
  • Office locations
  • Costs and fees
  • Processing times
• Please try asking about these topics."""
    
    print(f"Returning fallback response in {language}")
    return jsonify({"response": response_text})

if __name__ == '__main__':
    # Run without debug mode to avoid the reloader which causes issues with Cursor.AppImage
    app.run(debug=False, port=5002) 