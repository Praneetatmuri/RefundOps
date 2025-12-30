import os
import time
import json
from playwright.sync_api import sync_playwright
import database
import backend
import brain

# Disable browser automation restrictions for smoother simulation
ARGS = [
    '--disable-blink-features=AutomationControlled',
    '--start-maximized',
    '--no-sandbox'
]

# --- 1. REFUND PROCESS (Indigo / Air India) ---
def run_refund_process(page, airline_name, pnr_number, customer_name):
    """
    Executes the refund flow on the airline's specific portal.
    """
    print(f"\n[REFUND AGENT] Starting Refund Process for {airline_name}...", flush=True)
    
    filename = "indigo.html" if airline_name == "Indigo" else "airindia.html"
    file_path = os.path.abspath(filename)
    
    if not os.path.exists(file_path):
        print(f"Error: {filename} not found.")
        return False

    try:
        page.goto(f"file://{file_path}", wait_until="domcontentloaded", timeout=10000)
        print(f"Loaded {airline_name} portal.", flush=True)
        time.sleep(2)

        # A. Fill Form Details
        print("Filling PNR & Name...", flush=True)
        
        # PNR (Try multiple selectors for robustness)
        for selector in ['[name="pnr-booking-ref"]', '#pnr', '#pnr-input']:
            if page.locator(selector).is_visible():
                page.locator(selector).press_sequentially(pnr_number, delay=100)
                break
        
        # Name/Email
        for selector in ['[name="email-last-name"]', '#email', '#lastname', '#lastname-input']:
            if page.locator(selector).is_visible():
                # Extract last name if needed
                val = customer_name
                if "lastname" in selector and " " in customer_name:
                    val = customer_name.split()[-1]
                page.locator(selector).press_sequentially(val, delay=100)
                break
        
        time.sleep(1)
        print("Submitting Search...", flush=True)
        
        # Click Search/Next (Try multiple text matches)
        submit_btn = None
        for text in ["Get Booking Details", "Retrieve Booking", "Search", "Next"]:
            try:
                btn = page.get_by_text(text, exact=False).first
                if btn.is_visible():
                    btn.click()
                    submit_btn = btn
                    break
            except:
                continue
        
        if not submit_btn:
             # Fallback ID
             if page.locator("#nextBtn").is_visible():
                 page.locator("#nextBtn").click()

        # Wait for Next Page (Step 2)
        time.sleep(2.5)

        # B. Detect Cancellation & Refund
        print("Detecting Flight Status...", flush=True)
        
        # Simulate "Flight Cancelled" detection
        print(f"AUTONOMOUS AGENT ({airline_name}): Flight Cancellation Detected.", flush=True)
        print("DECISION: Initiating 'Refund & Hold' protocol automatically.", flush=True)
        
        # Update DB State
        database.set_bot_state("AUTONOMOUS_WORK", {
            "airline": airline_name, 
            "pnr": pnr_number, 
            "status": "Refunding & Rebooking..."
        })

        # C. Execute Refund Form (If visible)
        try:
             if page.locator("#refund-reason").is_visible():
                 page.locator("#refund-reason").select_option("cancelled")
                 time.sleep(1)
                 page.locator("#refund-remarks").press_sequentially(f"Automated refund req PNR {pnr_number}", delay=50)
                 time.sleep(0.5)
                 if page.locator("#refund-mode").is_visible():
                     page.locator("#refund-mode").select_option("original")
                 
                 page.locator("#terms-check").check()
                 time.sleep(0.5)
                 
                 # Submit Refund
                 print("Submitting Refund Request...", flush=True)
                 if page.locator("#submitBtn").is_visible():
                     page.locator("#submitBtn").click()
                 
                 time.sleep(2)
                 
                 # Take Screenshot of Refund Success
                 page.screenshot(path=f"{airline_name.lower()}_refund_success.png")
                 print("Refund Process Complete. Screenshot saved.")
                 
                 # Increment stats
                 database.increment_refund_count()
                 
        except Exception as e:
            print(f"Refund interaction warning: {e}")

        return True

    except Exception as e:
        print(f"Refund Process Failed: {e}")
        return False


# --- 2. REBOOKING PROCESS (Skyscanner) ---
def run_rebooking_process(page, airline_name, pnr, origin, destination):
    """
    Executes the rebooking search on the Skyscanner simulation.
    """
    print(f"\n[REBOOK AGENT] Starting Rebooking on Skyscanner...", flush=True)
    
    rebook_path = os.path.abspath("rebooking.html")
    
    # Inject dynamic route
    if os.path.exists(rebook_path) and origin != "Unknown":
        try:
            with open(rebook_path, "r", encoding="utf-8") as f: content = f.read()
            if "Searching best flights..." in content:
                new_content = content.replace("Searching best flights...", f"Showing flights for {origin} -> {destination}")
                with open(rebook_path, "w", encoding="utf-8") as f: f.write(new_content)
        except: pass

    try:
        page.goto(f"file://{rebook_path}")
        time.sleep(2)
        
        # A. Fill Skyscanner Form
        print("Filling Flight Details...", flush=True)
        try:
            page.locator("#from-input").press_sequentially(origin, delay=100)
            time.sleep(0.3)
            page.locator("#to-input").press_sequentially(destination, delay=100)
            time.sleep(0.3)
            
            # Date Visuals
            page.locator("#depart-btn").click()
            time.sleep(0.5)
            tomorrow = "1 Jan 2025"
            page.evaluate(f"document.getElementById('depart-btn').innerText = '{tomorrow}'")
            page.evaluate(f"document.getElementById('depart-btn').classList.add('text-black', 'font-bold')")
            
        except Exception as e:
            print(f"Form filling warning: {e}")

        # Search
        try:
            page.locator("#search-btn").click()
            print("Searching...", flush=True)
        except: pass
        
        time.sleep(2.5) # Wait for results
        
        # B. Reasoning Engine (Select Air India)
        print("Analyzing Options...", flush=True)
        try:
            page.locator(".ai-flight-card").wait_for(state="visible", timeout=5000)
            
            # Logic: Air India is better
            reasoning_msg = "Switching to Air India. It departs at 17:00 (5 hours earlier), which is worth the small price difference."
            print(f"DECISION: {reasoning_msg}")
            
            database.set_bot_state("AUTONOMOUS_WORK", {
                "airline": airline_name, 
                "pnr": pnr, 
                "status": f"Rebooking Confirmed. Reason: {reasoning_msg}"
            })
            
            # Click Select and go to details
            time.sleep(1.5)
            print("Clicking 'Select' on Air India flight...", flush=True)
            page.locator("#hold-btn").click()
            
        except Exception as e:
            print(f"Selection step warning: {e}")

        # C. Booking Details Phase
        try:
            # Wait for details page to render
            page.locator("h2:has-text('Select Seats')").wait_for(state="visible", timeout=5000)
            print("Booking Details Loaded.", flush=True)
            time.sleep(1)

            # Scroll to "read"
            print("Reading Booking Details...", flush=True)
            page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
            time.sleep(1.5)
            
            # Check Baggage
            print("Checking Baggage...", flush=True)
            page.locator("h2:has-text('Add Baggage')").scroll_into_view_if_needed()
            time.sleep(1)
            if page.locator("label:has(input[name='baggage'])").count() > 1:
                page.locator("label:has(input[name='baggage'])").nth(1).hover()
                time.sleep(1)
                page.locator("label:has(input[name='baggage'])").nth(0).click()

            # Select Best Seat
            print("Selecting Seat...", flush=True)
            page.locator("h2:has-text('Select Seats')").scroll_into_view_if_needed()
            time.sleep(1)
            if page.locator("#best-seat-1b").is_visible():
                page.locator("#best-seat-1b").click()
                print("Selected Premium Seat 1B.")
            else:
                page.locator(".grid button:not([disabled])").nth(5).click()
            
            time.sleep(1.5) # Time to see seat selection state change
            
            # Passenger Details
            try:
                page.locator("#first-name").press_sequentially("Praneet", delay=100)
                page.locator("#last-name").press_sequentially("Atmuri", delay=100)
                time.sleep(0.5)
            except: pass
            
            # Submit Hold
            print("Clicking Hold & Pay...", flush=True)
            page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
            time.sleep(0.5)
            page.locator("#continue-payment-btn").click()
            
            # Wait for Success
            print("Waiting for Confirmation...", flush=True)
            page.locator("h1:has-text('Booking Successfully Held')").wait_for(state="visible", timeout=10000)
            print("SUCCESS: Flight Held on Skyscanner!")
            
            database.set_bot_state("COMPLETED", {
                "airline": "Skyscanner (Air India)", 
                "pnr": "SKY-HOLD-888", 
                "status": "Success. Flight held for 24h."
            })
            
        except Exception as e:
            print(f"Booking flow error: {e}")

    except Exception as e:
        print(f"Rebooking Process Failed: {e}")


# --- MAIN ORCHESTRATOR ---
def autonomous_agent(airline_name, pnr, origin="Unknown", destination="Unknown"):
    start_time = time.time()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=ARGS)
        context = browser.new_context(viewport={'width': 1500, 'height': 900})
        page = context.new_page()
        
        try:
            # PHASE 1: REFUND (Airline Portal)
            # Only run if it's Indigo or Air India
            if airline_name in ["Indigo", "Air India"]:
                run_refund_process(page, airline_name, pnr, "Praneet Atmuri")
                time.sleep(1)
            
            # PHASE 2: REBOOK (Skyscanner)
            # We assume the refund logic detected a cancellation and triggered rebooking
            run_rebooking_process(page, airline_name, pnr, origin, destination)
            
        finally:
            print("Closing Session.")
            time.sleep(5) # Pause so user can see the final 'Success' overlay
            browser.close()

# --- BACKWARD COMPATIBILITY ---
def start_indigo_process(pnr, name, origin="Unknown", dest="Unknown"):
    autonomous_agent("Indigo", pnr, origin, dest)

def start_airindia_process(pnr, name, origin="Unknown", dest="Unknown"):
    autonomous_agent("Air India", pnr, origin, dest)

if __name__ == "__main__":
    # Test directly
    autonomous_agent("Indigo", "PNR123", "Hyderabad", "Bengaluru")