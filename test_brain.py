import brain

# Test email with flight cancellation
test_email = """
Dear Praneet Atmuri,

Your flight has been cancelled.

PNR: ABC123
Airline: Indigo
Route: Hyderabad to Bangalore
"""

print("Testing AI extraction with retry logic...\n")
result = brain.get_flight_data(test_email)
print("\n✅ Result:", result)
