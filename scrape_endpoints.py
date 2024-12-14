import requests
from bs4 import BeautifulSoup
import json
import datetime

# Fetch the webpage
url = "https://api.usaspending.gov/docs/endpoints"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the relevant information based on the provided field mappings
data = {}
api_endpoints = []

# Locate the table containing API endpoint information
table = soup.find('table')

# Iterate over each row in the table to extract endpoint details
if table:
    for row in table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        if len(columns) >= 3:
            endpoint_url = columns[0].get_text(strip=True)
            methods = columns[1].get_text(strip=True)
            description = columns[2].get_text(strip=True)
            api_endpoints.append({
                "endpoint_url": endpoint_url,
                "methods": methods,
                "description": description
            })

if api_endpoints:
    data['api_endpoints'] = api_endpoints

# Output to a timestamped JSON file
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
with open(f"api_endpoints_{timestamp}.json", "w") as outfile:
    json.dump(data, outfile, indent=4)

