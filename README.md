# Webcrawler

## Hotel Room Offers Scraper

This Python script scrapes hotel room offers from Qantas Hotels for a specific property over a range of dates. It collects details such as room name, rate name, number of guests, cancellation policy, price, currency, and whether it is a top deal. The results are saved in a CSV file.

### Features

- Scrapes room details and offers from Qantas Hotels.
- Generates date combinations for 25 consecutive days starting from a specified start date.
- Saves the scraped data to a CSV file.
- Adds a delay between requests to avoid being blocked by the server.

### Requirements
- Python 3.x
- requests library

### Installation
1. Clone the repository:
git clone https://github.com/borislavbebin/webcrawler
cd hotel-room-offers-scraper

2.pip install requests

### Usage
1. Set the start date:
Change the start_date variable to the desired start date in the format YYYY-MM-DD.
```
start_date = "2024-06-23"
```
2. Run the script:
```
python scrape_hotel_offers.py
```
3. Check the output:
The script will create a CSV file named room_offers.csv containing the scraped data.

### Code Explanation
The script performs the following steps:

1. Generate Date Combinations:

The generate_date_combinations function generates date combinations for 25 consecutive days starting from the specified start_date.

2. Set URLs and Headers:

The script sets the URLs for fetching room details and availability, as well as the headers for the HTTP requests.

3. Create a Session:

A requests session is created to handle the HTTP requests.

4. Fetch Data for Each Date Combination:

The script iterates over the date combinations, fetching room details and availability data for each date range. It adds a delay between requests to avoid being blocked.

5. Extract Room and Offer Details:

The script extracts room details from the room details URL and offer details from the availability URL. It maps the offers to the corresponding rooms.

6. Write Data to CSV:

The script writes the extracted data to a CSV file named room_offers.csv.

### Example Output

The CSV file room_offers.csv will have the following columns:

- check_in
- check_out
- hotels_id
- Room Name
- Rate Name
- Number of Guests
- Cancellation Policy
- Price
- Currency
- Top Deal

Each row represents an offer for a room on a specific date.

### Notes

- Adjust the time.sleep(2) delay if you need to make the crawling less or more noticeable.
- Ensure the start_date is in the correct format (YYYY-MM-DD).

### License
This project is licensed under the GPL-3.0 license - see the LICENSE file for details.
