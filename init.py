#!/usr/bin/env python3
"""
Initialization script for Nepal Forms Assistant Chrome Extension
This script sets up the necessary files and directories for the extension.
"""

import os
import subprocess
import sys
import json
import shutil

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def create_directories():
    """Create necessary directories"""
    print_header("Creating directories")
    
    dirs = [
        "data",
        "backend/data",
        "frontend/css",
        "frontend/js",
        "frontend/icons",
        "icons"
    ]
    
    for directory in dirs:
        print(f"Creating directory: {directory}")
        os.makedirs(directory, exist_ok=True)

def generate_icons():
    """Generate placeholder icons for the extension"""
    print_header("Generating placeholder icons")
    
    try:
        from PIL import Image, ImageDraw
        
        sizes = [16, 32, 48, 128]
        
        for size in sizes:
            print(f"Generating {size}x{size} icon")
            
            # Create a new image with a white background
            img = Image.new('RGBA', (size, size), color=(255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw a red square with a blue border
            border_width = max(1, size // 16)
            draw.rectangle(
                [(0, 0), (size, size)],
                fill=(230, 57, 70, 255),  # Red fill (primary color)
                outline=(69, 123, 157, 255),  # Blue outline (secondary color)
                width=border_width
            )
            
            # Save icon to frontend/icons
            frontend_icon_path = os.path.join("frontend", "icons", f"icon{size}.png")
            img.save(frontend_icon_path, "PNG")
            
            # Copy to root icons directory
            root_icon_path = os.path.join("icons", f"icon{size}.png")
            img.save(root_icon_path, "PNG")
            
    except ImportError:
        print("PIL (Python Imaging Library) not found. Icons will not be generated.")
        print("You can install it with: pip install Pillow")
        print("Or create icons manually in the frontend/icons and icons directories.")

def install_requirements():
    """Install Python requirements"""
    print_header("Installing Python requirements")
    
    try:
        print("Installing backend requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
        print("Backend requirements installed successfully!")
    except subprocess.CalledProcessError:
        print("Failed to install backend requirements.")
        print("You can install them manually with: pip install -r backend/requirements.txt")

def initialize_form_data():
    """Initialize form data"""
    print_header("Initializing form data")
    
    backend_data_path = os.path.join("backend", "data")
    os.makedirs(backend_data_path, exist_ok=True)
    
    try:
        # Try to run the form scraper
        print("Running form scraper to gather data...")
        from backend.form_scraper import FormScraper
        
        API_KEY = "AIzaSyAqQkaP_uhlveaXWLUmZvojpYFF2aP5-KI"
        scraper = FormScraper(api_key=API_KEY)
        forms = scraper.scrape_all_forms()
        
        print(f"Scraped data for {len(forms)} forms.")
        
        # Copy data to backend/data directory
        forms_json_path = os.path.join("data", "forms.json")
        backend_forms_json_path = os.path.join(backend_data_path, "forms.json")
        
        if os.path.exists(forms_json_path):
            shutil.copy(forms_json_path, backend_forms_json_path)
            print(f"Copied forms data to {backend_forms_json_path}")
    
    except ImportError:
        print("Failed to import FormScraper. Using fallback initialization.")
        create_fallback_form_data(backend_data_path)
    except Exception as e:
        print(f"Error running form scraper: {e}")
        print("Using fallback initialization.")
        create_fallback_form_data(backend_data_path)

def create_fallback_form_data(backend_data_path):
    """Create fallback form data if scraping fails"""
    print("Creating fallback form data...")
    
    # Create basic form data
    forms = [
        {
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
        },
        {
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
    ]
    
    # Write to backend/data/forms.json
    forms_json_path = os.path.join(backend_data_path, "forms.json")
    with open(forms_json_path, 'w', encoding='utf-8') as f:
        json.dump(forms, f, ensure_ascii=False, indent=2)
    
    print(f"Created fallback form data at {forms_json_path}")

def main():
    """Main initialization function"""
    print_header("Nepal Forms Assistant - Initialization")
    
    create_directories()
    generate_icons()
    install_requirements()
    initialize_form_data()
    
    print_header("Initialization Complete")
    print("\nTo start the backend server, run:")
    print("  python backend/server.py")
    print("\nTo load the extension in Chrome:")
    print("  1. Open Chrome and go to chrome://extensions/")
    print("  2. Enable Developer mode (top right)")
    print("  3. Click 'Load unpacked' and select this directory")
    
if __name__ == "__main__":
    main() 