import os
import time
import json
from playwright.sync_api import sync_playwright
import database
import backend
import brain
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- NOTIFICATION FUNCTIONS ---

def send_confirmation_email(user_email, customer_name, airline, pnr, route, new_airline="Air India Express"):
    """
    Send confirmation email after successful refund & rebooking
    """
    try:
        import config
        import importlib
        importlib.reload(config)
        
        sender_email = config.EMAIL_USER
        sender_password = config.EMAIL_PASS
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"✅ Refund & Rebooking Complete - PNR: {pnr}"
        msg['From'] = sender_email
        msg['To'] = user_email
        
        # HTML email body
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
              <h2 style="color: #10b981;">✅ Process Complete!</h2>
              
              <p>Dear <strong>{customer_name}</strong>,</p>
              
              <p>Great news! Your refund and rebooking process has been completed automatically.</p>
              
              <div style="background: #f0f9ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #0770e3; margin-top: 0;">✅ REFUND CONFIRMED</h3>
                <ul style="list-style: none; padding: 0;">
                  <li>• <strong>Airline:</strong> {airline}</li>
                  <li>• <strong>PNR:</strong> {pnr}</li>
                  <li>• <strong>Status:</strong> Confirmed</li>
                  <li>• <strong>Reference:</strong> REF-2025-{random.randint(1000, 9999)}</li>
                </ul>
              </div>
              
              <div style="background: #f0fdf4; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #10b981; margin-top: 0;">✈️ NEW BOOKING</h3>
                <ul style="list-style: none; padding: 0;">
                  <li>• <strong>Airline:</strong> {new_airline}</li>
                  <li>• <strong>Route:</strong> {route}</li>
                  <li>• <strong>Departure:</strong> Wed, 1 Jan 2025 at 17:00</li>
                  <li>• <strong>Seat:</strong> 1B (Premium)</li>
                  <li>• <strong>Booking Ref:</strong> SKY-HOLD-888</li>
                </ul>
              </div>
              
              <div style="background: #fef3c7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h4 style="margin-top: 0;">⏰ Next Steps:</h4>
                <ol>
                  <li>Complete payment within 24 hours</li>
                  <li>Check your email for the payment link</li>
                  <li>Download your e-ticket after payment</li>
                </ol>
              </div>
              
              <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 0.9em; color: #666;">
                <p><strong>Time Saved:</strong> ~45 minutes ⏱️</p>
                <p><strong>Automation Rate:</strong> 100% 🤖</p>
                <p style="margin-top: 20px;">Thank you for using <strong>RefundOps</strong>!</p>
                <p style="font-size: 0.8em; color: #999;">Automated by RefundOps AI Agent • {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
              </div>
            </div>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"✅ Confirmation email sent to {user_email}", flush=True)
        return True
        
    except Exception as e:
        print(f"⚠️ Could not send confirmation email: {e}", flush=True)
        return False


def send_telegram_notification(customer_name, airline, pnr, route):
    """
    Send Telegram notification (optional - requires bot setup)
    """
    try:
        # Check if Telegram is configured
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not telegram_token or not telegram_chat_id:
            print("ℹ️ Telegram not configured (optional)", flush=True)
            return False
        
        import requests
        
        message = f"""
🤖 *RefundOps - Process Complete!*

✅ *Refund Confirmed*
   • Airline: {airline}
   • PNR: {pnr}
   • Status: Confirmed

✈️ *New Booking*
   • Flight: {route}
   • Airline: Air India Express
   • Time: 17:00 on Jan 1, 2025
   • Seat: 1B (Premium)
   • Ref: SKY-HOLD-888

⏰ Payment due in 23h 59m

_Automated by RefundOps AI Agent_
        """
        
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        response = requests.post(url, json={
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        })
        
        if response.status_code == 200:
            print("✅ Telegram notification sent", flush=True)
            return True
        else:
            print(f"⚠️ Telegram error: {response.status_code}", flush=True)
            return False
            
    except Exception as e:
        print(f"ℹ️ Telegram notification skipped: {e}", flush=True)
        return False


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
def run_rebooking_process(page, airline_name, pnr, origin, destination, customer_name="User"):
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
            
            # Passenger Details - Use actual customer name from email
            print(f"Filling passenger details for: {customer_name}", flush=True)
            try:
                # Split customer name into first and last
                name_parts = customer_name.strip().split()
                first_name = name_parts[0] if len(name_parts) > 0 else "Passenger"
                last_name = name_parts[-1] if len(name_parts) > 1 else "User"
                
                page.locator("#first-name").press_sequentially(first_name, delay=100)
                page.locator("#last-name").press_sequentially(last_name, delay=100)
                time.sleep(0.5)
            except Exception as e:
                print(f"Could not auto-fill passenger details: {e}")
                # Fallback
                page.locator("#first-name").press_sequentially("Passenger", delay=100)
                page.locator("#last-name").press_sequentially("User", delay=100)
                time.sleep(0.5)
            
            # Submit Hold
            print("Clicking Hold & Pay...", flush=True)
            page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
            time.sleep(0.5)
            page.locator("#continue-payment-btn").click()
            
            # Wait for Success
            print("Waiting for Confirmation...", flush=True)
            page.locator("h1:has-text('Booking Successfully Held')").wait_for(state="visible", timeout=10000)
            
            # Update email if needed (in case the file write didn't pick it up or for visual confirmation)
            # Try to fetch email from config
            user_email = "user@example.com" # default
            try:
                import config
                import importlib
                importlib.reload(config) # Ensure we have the latest
                if hasattr(config, 'EMAIL_USER'):
                    user_email = config.EMAIL_USER
            except: 
                pass

            # Inject email into the success page dynamically
            try:
                # Set via JavaScript global variable (picked up by page's own script)
                page.evaluate(f"window.BOT_USER_EMAIL = '{user_email}';")
                # Trigger the email update function
                page.evaluate("if (typeof setUserEmail === 'function') setUserEmail();")
                
                print(f"✅ Email displayed: {user_email}", flush=True)
            except Exception as e:
                print(f"Email injection warning: {e}")

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
def autonomous_agent(airline_name, pnr, origin="Unknown", destination="Unknown", customer_name="User"):
    start_time = time.time()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=ARGS)
        context = browser.new_context(viewport={'width': 1500, 'height': 900})
        page = context.new_page()
        
        try:
            # PHASE 1: REFUND (Airline Portal)
            # Only run if it's Indigo or Air India
            if airline_name in ["Indigo", "Air India"]:
                run_refund_process(page, airline_name, pnr, customer_name)
                time.sleep(1)
            
            # PHASE 2: REBOOK (Skyscanner)
            # We assume the refund logic detected a cancellation and triggered rebooking
            try:
                run_rebooking_process(page, airline_name, pnr, origin, destination, customer_name)
            except Exception as e:
                print(f"[WARN] Rebooking Phase Warning: {e}")
            
            # PHASE 3: SEND CONFIRMATIONS
            # Check if we should send email (assume if we got this far, we try)
            print("\n" + "="*60, flush=True)
            print("[INFO] SENDING CONFIRMATIONS...", flush=True)
            print("="*60, flush=True)
            
            try:
                import config
                import importlib
                importlib.reload(config)
                user_email = getattr(config, 'EMAIL_USER', 'user@example.com')
                route = f"{origin} -> {destination}"
                
                # Send Email Confirmation
                email_sent = send_confirmation_email(
                    user_email=user_email,
                    customer_name=customer_name,
                    airline=airline_name,
                    pnr=pnr,
                    route=route
                )
                
                # Send Telegram Notification (optional)
                telegram_sent = send_telegram_notification(
                    customer_name=customer_name,
                    airline=airline_name,
                    pnr=pnr,
                    route=route
                )
                
                if email_sent:
                    print(f"[OK] Email confirmation sent to: {user_email}", flush=True)
                if telegram_sent:
                    print("[OK] Telegram notification sent", flush=True)
                    
                print("="*60 + "\n", flush=True)
                
            except Exception as e:
                print(f"[WARN] Notification error: {e}", flush=True)
            
        except Exception as e:
            print(f"[ERROR] Critical Agent Error: {e}")

        finally:
            print("Closing Session.")
            time.sleep(5) # Pause so user can see the final 'Success' overlay
            browser.close()

# --- BACKWARD COMPATIBILITY ---
def start_indigo_process(pnr, name, origin="Unknown", dest="Unknown"):
    autonomous_agent("Indigo", pnr, origin, dest, name)

def start_airindia_process(pnr, name, origin="Unknown", dest="Unknown"):
    autonomous_agent("Air India", pnr, origin, dest, name)

if __name__ == "__main__":
    # Test directly
    autonomous_agent("Indigo", "PNR123", "Hyderabad", "Bengaluru")