import requests
import json
from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Create a cipher suite
cipher_suite = Fernet(key)

# Encrypt data
data = "YOUR_CITY".encode()  # Replace "YOUR_CITY" with your actual city
cipher_text = cipher_suite.encrypt(data)
print(f"Cipher Text: {cipher_text}")

# Decrypt data
plain_text = cipher_suite.decrypt(cipher_text)
city_name = plain_text.decode()
print(f"Plain Text: {city_name}")

# Define the Eventbrite API endpoint
url = "https://www.eventbriteapi.com/v3/events/search/"

headers = {
    "Authorization": "Bearer CNBUEXWGLRNDGWYGXR5A",  
}

params = {
    "expand": "venue",
    "location.address": city_name,  # Use the decrypted city name
}

response = requests.get(url, headers=headers, params=params)

data = response.json()

if 'events' in data:
    for event in data["events"]:
        print(f"Event Name: {event.get('name', {}).get('text', 'N/A')}")
        print(f"Event Start: {event.get('start', {}).get('local', 'N/A')}")
        print(f"Event End: {event.get('end', {}).get('local', 'N/A')}")
        print(f"Venue: {event.get('venue', {}).get('name', 'N/A')}")
        print(f"Address: {event.get('venue', {}).get('address', {}).get('address_1', 'N/A')}")
        print()
else:
    print("No events found.")
