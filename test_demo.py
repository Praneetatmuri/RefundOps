"""
Quick Demo Test Script
Simulates the entire refund + rebook flow without needing an actual email
"""
import bot

# Simulate extracted data from an email
test_data = {
    "customer_name": "Praneet Atmuri",
    "pnr": "ABC123",
    "airline": "Indigo",
    "origin": "Hyderabad",
    "destination": "Bangalore"
}

print("=" * 60)
print("🚀 DEMO TEST - Direct Bot Execution")
print("=" * 60)
print(f"\nTest Data:")
print(f"  Customer: {test_data['customer_name']}")
print(f"  PNR: {test_data['pnr']}")
print(f"  Airline: {test_data['airline']}")
print(f"  Route: {test_data['origin']} → {test_data['destination']}")
print("\n" + "=" * 60)
print("Starting autonomous agent...\n")

# Call the bot directly with test data
bot.autonomous_agent(
    airline_name=test_data['airline'],
    pnr=test_data['pnr'],
    origin=test_data['origin'],
    destination=test_data['destination'],
    customer_name=test_data['customer_name']
)

print("\n" + "=" * 60)
print("✅ Demo test complete!")
print("=" * 60)
