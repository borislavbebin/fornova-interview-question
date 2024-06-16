import requests
import json

# Availability URL to fetch data
availability_url = "https://www.qantas.com/hotels/api/ui/properties/18482/availability?checkIn=2024-06-30&checkOut=2024-07-01&adults=2&children=0&infants=0&payWith=cash"

# Create a session
session = requests.Session()

# Comprehensive headers for the request
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "www.qantas.com",
    "Referer": "https://www.qantas.com/hotels/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Requested-With": "XMLHttpRequest",
}

# Fetch availability details
try:
    print(f"Fetching availability data from: {availability_url}")
    availability_response = session.get(availability_url, headers=headers, timeout=10)
    print(f"Availability response status code: {availability_response.status_code}")

    # Check status of availability response
    if availability_response.status_code == 200:
        availability_data = availability_response.json()
        print(json.dumps(availability_data, indent=2))
    else:
        print(f"Failed to retrieve availability data. Status code: {availability_response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching availability data: {e}")

