import requests
import json

BASE_URL = "https://api.usaspending.gov/api/v2/"
HEADERS = {"Content-Type": "application/json"}

def get_all_agencies():
    """
    Fetches a list of all top-tier government agencies and returns the raw JSON response.
    
    Returns:
        dict: Raw JSON response with agency details.
    """
    url = f"{BASE_URL}references/toptier_agencies/"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching agencies: {response.status_code}")
        return response.text

def get_agency_spending(agency_code, fiscal_year):
    """
    Fetches spending data for a specific government agency and returns the raw JSON response.
    
    Args:
        agency_code (str): The top-tier agency code.
        fiscal_year (int): The fiscal year to retrieve data for.
    
    Returns:
        dict: Raw JSON response with spending data.
    """
    url = f"{BASE_URL}agency/{agency_code}/budgetary_resources/"
    params = {"fiscal_year": fiscal_year}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching spending for agency {agency_code}: {response.status_code}")
        return response.text

# Example usage
if __name__ == "__main__":
    # Fetch all agencies
    agencies_response = get_all_agencies()
    print("Raw Agencies Response:")
    print(json.dumps(agencies_response, indent=2))
    
    # Fetch spending data for a specific agency (replace with a valid agency code from the list)
    example_agency_code = "020"  # Example: Department of Education
    fiscal_year = 2023
    spending_response = get_agency_spending(example_agency_code, fiscal_year)
    print("\nRaw Spending Response for Agency:")
    print(json.dumps(spending_response, indent=2))
