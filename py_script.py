import requests
import re
import json

url = "https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-06-23&checkOut=2024-06-24&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity"

response = requests.get(url)

if response.status_code == 200:
    # Debug
    content_type = response.headers.get('Content-Type')
    print(f"Content-Type: {content_type}")
    
    html_content = response.text
    print(html_content[:5000])

    # Get property name
    property_name_pattern = re.compile(r'<h1 data-testid="property-name" class="[^"]*">(.*?)</h1>', re.DOTALL)
    property_name_match = property_name_pattern.search(html_content)
    
    if property_name_match:
        property_name = property_name_match.group(1).strip()
        print(f"Property Name: {property_name}")
    else:
        print("Property name not found")

    # fetch property details 
    xhr_url = "https://www.qantas.com/hotels/api/ui/properties/18482"

    # Headers for the XHR request and user agent to prevent getting blocked cause of automatic request
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Host": "www.qantas.com",
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    # Send a GET request to the XHR endpoint
    xhr_response = requests.get(xhr_url, headers=headers)

    # Check the status of the XHR response
    if xhr_response.status_code == 200:
        print("XHR request successful")
    else:
        print(f"Failed to retrieve XHR data. Status code: {xhr_response.status_code}")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}") 

