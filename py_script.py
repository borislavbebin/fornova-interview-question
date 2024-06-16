import requests
import re
import json
import csv
from datetime import datetime, timedelta


def generate_date_combinations(start_date, num_combinations):
    date_combinations = []
    base_date = datetime.strptime(start_date, "%Y-%m-%d")
    for i in range(num_combinations):
        check_in = base_date + timedelta(days=i)
        check_out = check_in + timedelta(days=1)
        date_combinations.append((check_in.strftime("%Y-%m-%d"), check_out.strftime("%Y-%m-%d")))
    return date_combinations

# generate # number of combinations
start_date = "2024-06-23"
date_combinations = generate_date_combinations(start_date, 25)

# urls
url = "https://www.qantas.com/hotels/properties/18482?adults=2&checkIn={}&checkOut={}&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity"
xhr_url = "https://www.qantas.com/hotels/api/ui/properties/18482"
availability_base_url = "https://www.qantas.com/hotels/api/ui/properties/18482/availability?checkIn={}&checkOut={}&adults=2&children=0&infants=0&payWith=cash"

# Headers for the requests
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

# create a session
session = requests.Session()

# CSV headers
csv_file = "room_offers.csv"
csv_headers = ["Room Name", "Rate Name", "Number of Guests", "Cancellation Policy", "Price", "Currency", "Top Deal"]
 
response = requests.get(url)

if response.status_code == 200:
    # cookies ftw
    cookies = response.cookies
    # Debug
    content_type = response.headers.get("Content-Type")
    # print(f"Content-Type: {content_type}")
    
    html_content = response.text
    # print(html_content[:5000])

    # Get property name
    property_name_pattern = re.compile(r'<h1 data-testid="property-name" class="[^"]*">(.*?)</h1>', re.DOTALL)
    property_name_match = property_name_pattern.search(html_content)
    
    if property_name_match:
        property_name = property_name_match.group(1).strip()
        print(f"Property Name: {property_name}")
    else:
        print("Property name not found")

    # Send a GET request to the XHR endpoint
    xhr_response = requests.get(xhr_url, headers=headers, cookies=cookies)

    # Check the status of the XHR response
    if xhr_response.status_code == 200:
        print("XHR request successful")
        data = xhr_response.json()
        # print(json.dumps(data, indent=2))

        # Print the structure of the JSON
        '''def print_structure(data, indent=0):
            if isinstance(data, dict):
                for key, value in data.items():
                    print("  " * indent + str(key) + ":")
                    print_structure(value, indent + 1)
            elif isinstance(data, list):
                for index, item in enumerate(data):
                    print("  " * indent + f"[{index}]")
                    print_structure(item, indent + 1)
            else:
                print("  " * indent + str(type(data).__name__))

        # Print the structure of the JSON data
        print_structure(data)
        '''
        # Extract property and room details from JSON
        rooms = data.get("property", {}).get("roomTypes", [])
        room_details = []
        room_dict = {}
        # print(rooms)
        if rooms:
            # print("Room Details:")
            for room in rooms:
                room_name = room.get("name")
                rate_name = room.get("rateName")
                number_of_guests = room.get("maxOccupantCount")
                
                room_detail = {
                    "Room Name": room_name,
                    "Rate Name": rate_name,
                    "Number of Guests": number_of_guests,
                    "Offers": []
                }
                room_details.append(room_detail)
                room_dict[room_name] = room_detail
        else:
            print("No room details found")

        # print(rooms)
        # print(room_details)
        # print(f"Fetching availability data from: {availability_url}")
        availability_response = requests.get(availability_url, headers=headers, cookies=cookies, timeout=10)
        # print(availability_response)
        # Check status of availability response
        if availability_response.status_code == 200:
            availability_data = availability_response.json()
            # print(json.dumps(availability_data, indent=2))

            # Extract details from availability json
            availability_rooms = availability_data.get("roomTypes", [])
            # print(availability_rooms)
            if availability_rooms:
                for availability_room in availability_rooms:
                    # print(i, availability_room)
                    room_name = availability_room.get("name")
                    if room_name in room_dict:
                        for offer in availability_room.get("offers", []):
                            # print(offer)
                            cancellation_policy = offer.get("cancellationPolicy", {}).get("description", "N/A")
                            price_info = offer.get("charges", {}).get("total", {})
                            price = price_info.get("amount", "N/A")
                            currency = price_info.get("currency", "N/A")
                            top_deal = offer.get("promotion", {}).get("name", "") == "Top Deal"

                            offer_detail = {
                                "Cancellation Policy": cancellation_policy,
                                "Price": price,
                                "Currency": currency,
                                "Top Deal": top_deal
                            }
                            room_dict[room_name]["Offers"].append(offer_detail)
            else:
                print("No availability room details found")
        else:
            print(f"Failed to retrieve availability data. Status code: {availability_response.status_code}")
        '''        
        # print("Print all room details")
        for room_detail in room_details:
            if room_detail["Offers"]:
                print(json.dumps(room_detail, indent=2))
        '''

        # Write to csv
        csv_data = []
        for room_detail in room_details:
            if room_detail["Offers"]:
                for offer in room_detail["Offers"]:
                    csv_data.append({
                        "Room Name": room_detail["Room Name"],
                        "Rate Name": room_detail["Rate Name"],
                        "Number of Guests": room_detail["Number of Guests"],
                        "Cancellation Policy": offer["Cancellation Policy"],
                        "Price": offer["Price"],
                        "Currency": offer["Currency"],
                        "Top Deal": offer["Top Deal"]
                    })

        # Write to csv
        try:
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=csv_headers)
                writer.writeheader()
                for row in csv_data:
                    writer.writerow(row)
            print(f"Data successfully written to {csv_file}")
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")


    else:
        print(f"Failed to retrieve XHR data. Status code: {xhr_response.status_code}")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}") 

