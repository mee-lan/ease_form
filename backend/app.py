# from flask import Flask, request, jsonify
# import google.generativeai as genai
# import requests
# from bs4 import BeautifulSoup
# import json
# import os

# app = Flask(__name__)

# # Configure the Gemini API
# GEMINI_API_KEY = "AIzaSyAqQkaP_uhlveaXWLUmZvojpYFF2aP5-KI"
# genai.configure(api_key=GEMINI_API_KEY)

# # Load form data from JSON files
# def load_form_data():
#     with open('data/forms.json', 'r', encoding='utf-8') as f:
#         return json.load(f)

# # Initialize Gemini model
# def get_gemini_model():
#     return genai.GenerativeModel('gemini-pro')

# @app.route('/api/forms', methods=['GET'])
# def get_forms():
#     try:
#         forms = load_form_data()
#         return jsonify(forms)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/api/form/<form_id>', methods=['GET'])
# def get_form_details(form_id):
#     try:
#         forms = load_form_data()
#         for form in forms:
#             if form['id'] == form_id:
#                 return jsonify(form)
#         return jsonify({"error": "Form not found"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/api/chat', methods=['POST'])
# def chat():
#     try:
#         data = request.json
#         user_message = data.get('message', '')
#         form_context = data.get('form_context', None)
        
#         # Prepare context for the model
#         system_prompt = """
#         You are an assistant helping non-tech-savvy users with Nepali governmental forms.
#         Provide simple, clear instructions and guidance for form filling.
#         Use simple language and avoid technical terms.
#         Always provide accurate information about document requirements, office locations, and procedures.
#         """
        
#         prompt = user_message
#         if form_context:
#             prompt = f"Context: User is filling a {form_context} form. Question: {user_message}"
        
#         model = get_gemini_model()
#         response = model.generate_content(
#             [system_prompt, prompt],
#             generation_config={
#                 "temperature": 0.7,
#                 "top_p": 0.95,
#                 "top_k": 40,
#                 "max_output_tokens": 1024,
#             }
#         )
        
#         return jsonify({"response": response.text})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/api/scrape', methods=['POST'])
# def scrape_form_data():
#     """Admin endpoint to scrape and update form data"""
#     try:
#         # This would be a protected endpoint in production
#         form_data = []
        
#         # Example: Scrape citizenship data
#         citizenship_data = scrape_citizenship_info()
#         form_data.append(citizenship_data)
        
#         # Save scraped data
#         os.makedirs('data', exist_ok=True)
#         with open('data/forms.json', 'w', encoding='utf-8') as f:
#             json.dump(form_data, f, ensure_ascii=False, indent=2)
            
#         return jsonify({"status": "success", "message": "Form data updated"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# def scrape_citizenship_info():
#     """Scrape information about citizenship requirements from Nepal government websites"""
#     # This would be implemented with proper scraping logic
#     # For now, we'll return mock data
#     return {
#         "id": "citizenship",
#         "name": "Citizenship Certificate",
#         "requirements": [
#             "Two passport-sized photos",
#             "Birth certificate",
#             "Father's and mother's citizenship certificate (photocopy)",
#             "Character certificate from the local authority",
#             "Land ownership certificate or relationship certificate",
#         ],
#         "process": [
#             "Fill out the citizenship application form",
#             "Submit the application at your local District Administration Office",
#             "Attend an interview if required",
#             "Receive your citizenship certificate"
#         ],
#         "locations": [
#             "District Administration Office (DAO) in your district",
#             "Area Administration Office in some locations"
#         ],
#         "contact": "Contact your local District Administration Office for specific requirements in your area"
#     }

# if __name__ == '__main__':
#     # Create initial data directory if it doesn't exist
#     os.makedirs('data', exist_ok=True)
    
#     # If forms.json doesn't exist, create it with initial data
#     if not os.path.exists('data/forms.json'):
#         initial_forms = [
#             scrape_citizenship_info(),
#             {
#                 "id": "passport",
#                 "name": "Passport",
#                 "requirements": [
#                     "Citizenship Certificate (original and photocopy)",
#                     "Recent passport-sized photos (MRP specification)",
#                     "Filled application form"
#                 ],
#                 "process": [
#                     "Submit application online at nepalpassport.gov.np",
#                     "Pay the fee at the specified bank",
#                     "Visit the Passport Department or District Administration Office with receipt",
#                     "Provide biometric data",
#                     "Collect passport after processing"
#                 ],
#                 "locations": [
#                     "Department of Passport, Narayanhiti, Kathmandu",
#                     "District Administration Offices across Nepal"
#                 ],
#                 "contact": "Department of Passport: 01-4416010, 01-4416011"
#             },
#             {
#                 "id": "driving-license",
#                 "name": "Driving License",
#                 "requirements": [
#                     "Citizenship Certificate (original and photocopy)",
#                     "Medical report from authorized medical practitioner",
#                     "Blood group certificate",
#                     "Application form with photos"
#                 ],
#                 "process": [
#                     "Register online at www.dotm.gov.np",
#                     "Take written exam on the scheduled date",
#                     "Take practical driving test if written test is passed",
#                     "Pay the fee and collect your license"
#                 ],
#                 "locations": [
#                     "Transport Management Offices across Nepal"
#                 ],
#                 "contact": "Department of Transport Management: 01-4474921"
#             },
#             {
#                 "id": "pan",
#                 "name": "PAN Number",
#                 "requirements": [
#                     "Citizenship Certificate (original and photocopy)",
#                     "Business registration certificate (if applicable)",
#                     "Two passport-sized photos",
#                     "Application form"
#                 ],
#                 "process": [
#                     "Fill the PAN registration form",
#                     "Submit at the nearest Tax Office",
#                     "Pay the registration fee",
#                     "Receive PAN certificate"
#                 ],
#                 "locations": [
#                     "Inland Revenue Offices across Nepal"
#                 ],
#                 "contact": "Inland Revenue Department: 01-4415802, 01-4410340"
#             },
#             {
#                 "id": "nid",
#                 "name": "National ID Card",
#                 "requirements": [
#                     "Citizenship Certificate (original and photocopy)",
#                     "Birth certificate",
#                     "Recent passport-sized photos",
#                     "Completed application form"
#                 ],
#                 "process": [
#                     "Fill the application form",
#                     "Visit NID Management Center with required documents",
#                     "Provide biometric data including fingerprints and photo",
#                     "Collect NID card after processing"
#                 ],
#                 "locations": [
#                     "National ID Management Center, Kathmandu",
#                     "District Administration Offices"
#                 ],
#                 "contact": "National ID Management Center: 01-4211214"
#             },
#             {
#                 "id": "loksewa",
#                 "name": "Lok Sewa Application",
#                 "requirements": [
#                     "Citizenship Certificate (original and photocopy)",
#                     "Recent passport-sized photos",
#                     "Academic certificates",
#                     "Training certificates (if applicable)",
#                     "Experience letters (if applicable)"
#                 ],
#                 "process": [
#                     "Check vacancy notice on psc.gov.np",
#                     "Fill online application form",
#                     "Pay application fee through bank or online payment",
#                     "Download admit card for exams",
#                     "Attend written test and interview as scheduled"
#                 ],
#                 "locations": [
#                     "Public Service Commission offices across Nepal"
#                 ],
#                 "contact": "Public Service Commission: 01-4771487, 01-4771915"
#             }
#         ]
        
#         with open('data/forms.json', 'w', encoding='utf-8') as f:
#             json.dump(initial_forms, f, ensure_ascii=False, indent=2)
    
#     app.run(debug=True, port=5000) 