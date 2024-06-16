import requests
import re

url = "https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-06-23&checkOut=2024-06-24&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity"

response = requests.get(url)

if response.status_code == 200:
    # Debug
    content_type = response.headers.get('Content-Type')
    print(f"Content-Type: {content_type}")
    
    html_content = response.text
    print(html_content[:5000])

    property_name_pattern = re.compile(r'<h1 data-testid="property-name" class="[^"]*">(.*?)</h1>', re.DOTALL)
    property_name_match = property_name_pattern.search(html_content)
    
    if property_name_match:
        property_name = property_name_match.group(1).strip()
        print(f"Property Name: {property_name}")
    else:
        print("Property name not found")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}") 

