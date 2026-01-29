import google.generativeai as genai
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("ERROR: GOOGLE_API_KEY not found in environment variables!")
    print("Please add GOOGLE_API_KEY to your .env file")

genai.configure(api_key=GOOGLE_API_KEY)

# Using Gemini 2.5 Flash
model = genai.GenerativeModel(
    'models/gemini-2.5-flash',
    generation_config={"response_mime_type": "application/json"}
)

def get_flight_data(email_text, max_retries=3):
    """
    Extract flight data from email text using Gemini AI.
    Includes retry logic for robustness.
    """
    print("BRAIN: Reading email...", flush=True)
    
    # Prompt specifically asks for the Airline Name now
    prompt = f"""
    You are a data extraction agent.
    Extract the following details from this email. Return ONLY a single JSON object (not an array).
    
    Required format (must be an object, not an array):
    {{
        "pnr": "ABC123",
        "airline": "Air India",
        "customer_name": "John Doe",
        "origin": "Mumbai",
        "destination": "Delhi"
    }}
    
    Fields to extract:
    - pnr (string) -> The booking reference (usually 6 chars)
    - airline (string) -> Example: "Indigo", "Air India", "Vistara"
    - customer_name (string) -> The full name of the passenger/customer
    - origin (string) -> The city the flight departs from
    - destination (string) -> The city the flight arrives at
    
    Email Text:
    "{email_text}"
    
    Return ONLY the JSON object, nothing else.
    """
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            result = json.loads(response.text)
            
            # If result is a list, take the first item
            if isinstance(result, list):
                result = result[0] if len(result) > 0 else None
            
            # Validate required fields
            if result and all(key in result for key in ["pnr", "airline", "customer_name"]):
                print(f"BRAIN: Successfully extracted data on attempt {attempt + 1}", flush=True)
                return result
            else:
                print(f"BRAIN: Incomplete data extracted, retrying... (attempt {attempt + 1}/{max_retries})", flush=True)
                
        except json.JSONDecodeError as e:
            print(f"BRAIN: JSON parsing error on attempt {attempt + 1}: {e}", flush=True)
        except Exception as e:
            print(f"BRAIN: Error on attempt {attempt + 1}: {e}", flush=True)
        
        # Exponential backoff before retry
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"BRAIN: Waiting {wait_time}s before retry...", flush=True)
            time.sleep(wait_time)
    
    print("BRAIN: Failed to extract data after all retries", flush=True)
    return None