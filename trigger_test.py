import bot
import time

print("--- TRIGGER TEST (SMART AGENT) ---")
print("Simulating incoming email processing...")

# Test Data (matches the cancelled flight scenario we prepared)
pnr = "6E-TEST-888"
customer_name = "Praneet Atmuri" 
origin = "Bangalore"
destination = "Delhi"

print(f"Detected PNR: {pnr}")
print(f"Customer: {customer_name}")
print(f"Route: {origin} -> {destination}")
print("Launching INDIGO Bot sequence...")

# Call the bot directly with the new parameters
try:
    bot.start_indigo_process(pnr, customer_name, origin, destination)
    print("--- TEST SEQUENCE COMPLETE ---")
except Exception as e:
    print(f"Test failed: {e}")
