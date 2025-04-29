#!/usr/bin/env python3
"""
Form Scraper for Nepal Forms Assistant
This script scrapes information about Nepali government forms from various official websites.
"""

import os
import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import time
import random

class FormScraper:
    def __init__(self, api_key=None):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9,ne;q=0.8',
        }
        
        # Initialize Gemini if API key is provided
        if api_key:
            self.api_key = api_key
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.api_key = None
            self.model = None
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
    
    def scrape_all_forms(self):
        """Scrape information for all supported forms"""
        forms = []
        
        # Scrape citizenship certificate info
        forms.append(self.scrape_citizenship_info())
        
        # Scrape passport info
        forms.append(self.scrape_passport_info())
        
        # Scrape driving license info
        forms.append(self.scrape_driving_license_info())
        
        # Scrape PAN info
        forms.append(self.scrape_pan_info())
        
        # Scrape national ID info
        forms.append(self.scrape_national_id_info())
        
        # Scrape Lok Sewa info
        forms.append(self.scrape_loksewa_info())
        
        # Save all forms to JSON file
        self.save_forms(forms)
        
        return forms
    
    def scrape_citizenship_info(self):
        """Scrape information about citizenship requirements"""
        print("Scraping citizenship information...")
        
        try:
            # Try to scrape from Department of National ID and Civil Registration
            url = "https://donidcr.gov.np/Home/CitizenshipInfo"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract info (actual implementation would parse specific elements)
                # ...
            
            # If web scraping fails or data is incomplete, use Gemini to generate data
            if self.model:
                citizenship_info = self.generate_citizenship_info()
                return citizenship_info
            
        except Exception as e:
            print(f"Error scraping citizenship info: {e}")
            if self.model:
                citizenship_info = self.generate_citizenship_info()
                return citizenship_info
        
        # Fallback to hardcoded data if both scraping and Gemini fail
        return {
            "id": "citizenship",
            "name": "Citizenship Certificate",
            "requirements": [
                "Two passport-sized photos",
                "Birth certificate",
                "Father's and mother's citizenship certificate (photocopy)",
                "Character certificate from the local authority",
                "Land ownership certificate or relationship certificate",
            ],
            "process": [
                "Fill out the citizenship application form",
                "Submit the application at your local District Administration Office",
                "Attend an interview if required",
                "Receive your citizenship certificate"
            ],
            "locations": [
                "District Administration Office (DAO) in your district",
                "Area Administration Office in some locations"
            ],
            "contact": "Contact your local District Administration Office for specific requirements in your area"
        }
    
    def scrape_passport_info(self):
        """Scrape information about passport requirements"""
        print("Scraping passport information...")
        
        try:
            # Try to scrape from Department of Passport
            url = "https://nepalpassport.gov.np/normal-passport/"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract info (actual implementation would parse specific elements)
                # ...
            
            # If web scraping fails or data is incomplete, use Gemini to generate data
            if self.model:
                passport_info = self.generate_passport_info()
                return passport_info
                
        except Exception as e:
            print(f"Error scraping passport info: {e}")
            if self.model:
                passport_info = self.generate_passport_info()
                return passport_info
        
        # Fallback to hardcoded data
        return {
            "id": "passport",
            "name": "Passport",
            "requirements": [
                "Citizenship Certificate (original and photocopy)",
                "Recent passport-sized photos (MRP specification)",
                "Filled application form"
            ],
            "process": [
                "Submit application online at nepalpassport.gov.np",
                "Pay the fee at the specified bank",
                "Visit the Passport Department or District Administration Office with receipt",
                "Provide biometric data",
                "Collect passport after processing"
            ],
            "locations": [
                "Department of Passport, Narayanhiti, Kathmandu",
                "District Administration Offices across Nepal"
            ],
            "contact": "Department of Passport: 01-4416010, 01-4416011"
        }
    
    def scrape_driving_license_info(self):
        """Scrape information about driving license requirements"""
        print("Scraping driving license information...")
        
        try:
            # Try to scrape from Department of Transport Management
            url = "https://www.dotm.gov.np/en/driving-license/"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract info (actual implementation would parse specific elements)
                # ...
            
            # If web scraping fails or data is incomplete, use Gemini to generate data
            if self.model:
                driving_license_info = self.generate_driving_license_info()
                return driving_license_info
                
        except Exception as e:
            print(f"Error scraping driving license info: {e}")
            if self.model:
                driving_license_info = self.generate_driving_license_info()
                return driving_license_info
        
        # Fallback to hardcoded data
        return {
            "id": "driving-license",
            "name": "Driving License",
            "requirements": [
                "Citizenship Certificate (original and photocopy)",
                "Medical report from authorized medical practitioner",
                "Blood group certificate",
                "Application form with photos"
            ],
            "process": [
                "Register online at www.dotm.gov.np",
                "Take written exam on the scheduled date",
                "Take practical driving test if written test is passed",
                "Pay the fee and collect your license"
            ],
            "locations": [
                "Transport Management Offices across Nepal"
            ],
            "contact": "Department of Transport Management: 01-4474921"
        }
    
    def scrape_pan_info(self):
        """Scrape information about PAN requirements"""
        print("Scraping PAN information...")
        
        try:
            # Try to scrape from Inland Revenue Department
            url = "https://ird.gov.np/pan-registration"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract info (actual implementation would parse specific elements)
                # ...
            
            # If web scraping fails or data is incomplete, use Gemini to generate data
            if self.model:
                pan_info = self.generate_pan_info()
                return pan_info
                
        except Exception as e:
            print(f"Error scraping PAN info: {e}")
            if self.model:
                pan_info = self.generate_pan_info()
                return pan_info
        
        # Fallback to hardcoded data
        return {
            "id": "pan",
            "name": "PAN Number",
            "requirements": [
                "Citizenship Certificate (original and photocopy)",
                "Business registration certificate (if applicable)",
                "Two passport-sized photos",
                "Application form"
            ],
            "process": [
                "Fill the PAN registration form",
                "Submit at the nearest Tax Office",
                "Pay the registration fee",
                "Receive PAN certificate"
            ],
            "locations": [
                "Inland Revenue Offices across Nepal"
            ],
            "contact": "Inland Revenue Department: 01-4415802, 01-4410340"
        }
    
    def scrape_national_id_info(self):
        """Scrape information about National ID requirements"""
        print("Scraping National ID information...")
        
        try:
            # Try to scrape from National ID Management Center
            url = "https://donidcr.gov.np/Home/NationalIdentity"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract info (actual implementation would parse specific elements)
                # ...
            
            # If web scraping fails or data is incomplete, use Gemini to generate data
            if self.model:
                nid_info = self.generate_national_id_info()
                return nid_info
                
        except Exception as e:
            print(f"Error scraping National ID info: {e}")
            if self.model:
                nid_info = self.generate_national_id_info()
                return nid_info
        
        # Fallback to hardcoded data
        return {
            "id": "nid",
            "name": "National ID Card",
            "requirements": [
                "Citizenship Certificate (original and photocopy)",
                "Birth certificate",
                "Recent passport-sized photos",
                "Completed application form"
            ],
            "process": [
                "Fill the application form",
                "Visit NID Management Center with required documents",
                "Provide biometric data including fingerprints and photo",
                "Collect NID card after processing"
            ],
            "locations": [
                "National ID Management Center, Kathmandu",
                "District Administration Offices"
            ],
            "contact": "National ID Management Center: 01-4211214"
        }
    
    def scrape_loksewa_info(self):
        """Scrape information about Lok Sewa requirements"""
        print("Scraping Lok Sewa information...")
        
        try:
            # Try to scrape from Public Service Commission
            url = "https://psc.gov.np/category/application-process/"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract info (actual implementation would parse specific elements)
                # ...
            
            # If web scraping fails or data is incomplete, use Gemini to generate data
            if self.model:
                loksewa_info = self.generate_loksewa_info()
                return loksewa_info
                
        except Exception as e:
            print(f"Error scraping Lok Sewa info: {e}")
            if self.model:
                loksewa_info = self.generate_loksewa_info()
                return loksewa_info
        
        # Fallback to hardcoded data
        return {
            "id": "loksewa",
            "name": "Lok Sewa Application",
            "requirements": [
                "Citizenship Certificate (original and photocopy)",
                "Recent passport-sized photos",
                "Academic certificates",
                "Training certificates (if applicable)",
                "Experience letters (if applicable)"
            ],
            "process": [
                "Check vacancy notice on psc.gov.np",
                "Fill online application form",
                "Pay application fee through bank or online payment",
                "Download admit card for exams",
                "Attend written test and interview as scheduled"
            ],
            "locations": [
                "Public Service Commission offices across Nepal"
            ],
            "contact": "Public Service Commission: 01-4771487, 01-4771915"
        }
    
    def generate_citizenship_info(self):
        """Generate citizenship info using Gemini API"""
        prompt = """
        Please provide accurate and up-to-date information about Nepal's citizenship certificate application process.
        Format the response as a JSON object with the following structure:
        {
            "id": "citizenship",
            "name": "Citizenship Certificate",
            "requirements": [list of required documents],
            "process": [step-by-step process],
            "locations": [where to apply],
            "contact": "contact information"
        }
        Ensure the information is accurate as of 2023.
        """
        
        response = self.model.generate_content(prompt)
        # Extract JSON from response
        json_str = response.text
        try:
            # Clean up the response and parse JSON
            json_str = json_str.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            
            json_data = json.loads(json_str.strip())
            return json_data
        except Exception as e:
            print(f"Error parsing Gemini response for citizenship: {e}")
            # Return default data
            return self.scrape_citizenship_info()
    
    def generate_passport_info(self):
        """Generate passport info using Gemini API"""
        prompt = """
        Please provide accurate and up-to-date information about Nepal's passport application process.
        Format the response as a JSON object with the following structure:
        {
            "id": "passport",
            "name": "Passport",
            "requirements": [list of required documents],
            "process": [step-by-step process],
            "locations": [where to apply],
            "contact": "contact information"
        }
        Ensure the information is accurate as of 2023.
        """
        
        response = self.model.generate_content(prompt)
        # Extract JSON from response
        json_str = response.text
        try:
            # Clean up the response and parse JSON
            json_str = json_str.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            
            json_data = json.loads(json_str.strip())
            return json_data
        except Exception as e:
            print(f"Error parsing Gemini response for passport: {e}")
            # Return default data
            return self.scrape_passport_info()
    
    def generate_driving_license_info(self):
        """Generate driving license info using Gemini API"""
        # Similar implementation to other generate methods
        # ...
        return {
            "id": "driving-license",
            "name": "Driving License",
            "requirements": [
                "Citizenship Certificate (original and photocopy)",
                "Medical report from authorized medical practitioner",
                "Blood group certificate",
                "Application form with photos"
            ],
            "process": [
                "Register online at www.dotm.gov.np",
                "Take written exam on the scheduled date",
                "Take practical driving test if written test is passed",
                "Pay the fee and collect your license"
            ],
            "locations": [
                "Transport Management Offices across Nepal"
            ],
            "contact": "Department of Transport Management: 01-4474921"
        }
    
    def generate_pan_info(self):
        """Generate PAN info using Gemini API"""
        # Similar implementation to other generate methods
        # ...
        return {
            "id": "pan",
            "name": "PAN Number",
            "requirements": [
                "Citizenship Certificate (original and photocopy)",
                "Business registration certificate (if applicable)",
                "Two passport-sized photos",
                "Application form"
            ],
            "process": [
                "Fill the PAN registration form",
                "Submit at the nearest Tax Office",
                "Pay the registration fee",
                "Receive PAN certificate"
            ],
            "locations": [
                "Inland Revenue Offices across Nepal"
            ],
            "contact": "Inland Revenue Department: 01-4415802, 01-4410340"
        }
    
    def generate_national_id_info(self):
        """Generate National ID info using Gemini API"""
        # Similar implementation to other generate methods
        # ...
        return {
            "id": "nid",
            "name": "National ID Card",
            "requirements": [
                "Citizenship Certificate (original and photocopy)",
                "Birth certificate",
                "Recent passport-sized photos",
                "Completed application form"
            ],
            "process": [
                "Fill the application form",
                "Visit NID Management Center with required documents",
                "Provide biometric data including fingerprints and photo",
                "Collect NID card after processing"
            ],
            "locations": [
                "National ID Management Center, Kathmandu",
                "District Administration Offices"
            ],
            "contact": "National ID Management Center: 01-4211214"
        }
    
    def generate_loksewa_info(self):
        """Generate Lok Sewa info using Gemini API"""
        # Similar implementation to other generate methods
        # ...
        return {
            "id": "loksewa",
            "name": "Lok Sewa Application",
            "requirements": [
                "Citizenship Certificate (original and photocopy)",
                "Recent passport-sized photos",
                "Academic certificates",
                "Training certificates (if applicable)",
                "Experience letters (if applicable)"
            ],
            "process": [
                "Check vacancy notice on psc.gov.np",
                "Fill online application form",
                "Pay application fee through bank or online payment",
                "Download admit card for exams",
                "Attend written test and interview as scheduled"
            ],
            "locations": [
                "Public Service Commission offices across Nepal"
            ],
            "contact": "Public Service Commission: 01-4771487, 01-4771915"
        }
    
    def save_forms(self, forms):
        """Save forms data to JSON file"""
        try:
            with open('data/forms.json', 'w', encoding='utf-8') as f:
                json.dump(forms, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(forms)} forms to data/forms.json")
        except Exception as e:
            print(f"Error saving forms: {e}")

if __name__ == "__main__":
    API_KEY = "AIzaSyAqQkaP_uhlveaXWLUmZvojpYFF2aP5-KI"
    scraper = FormScraper(api_key=API_KEY)
    forms = scraper.scrape_all_forms()
    print(f"Scraped {len(forms)} forms") 