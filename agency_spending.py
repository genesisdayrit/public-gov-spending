import requests
import pandas as pd

BASE_URL = "https://api.usaspending.gov/api/v2/"
HEADERS = {"Content-Type": "application/json"}

def get_all_agencies():
    """
    Fetches a list of all top-tier government agencies.
    
    Returns:
        list: A list of agencies with their codes and names.
    """
    url = f"{BASE_URL}references/toptier_agencies/"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data.get('results', [])
    else:
        print(f"Error fetching agencies: {response.status_code}")
        return []

def get_agency_spending(agency_code, fiscal_year):
    """
    Fetches spending data for a specific government agency.
    
    Args:
        agency_code (str): The top-tier agency code.
        fiscal_year (int): The fiscal year to retrieve data for.
    
    Returns:
        dict: Spending data for the specified agency and year.
    """
    url = f"{BASE_URL}agency/{agency_code}/budgetary_resources/"
    params = {"fiscal_year": fiscal_year}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "agency_code": agency_code,
            "fiscal_year": fiscal_year,
            "total_budgetary_resources": data.get("total_budgetary_resources"),
            "obligations_incurred": data.get("obligations_incurred"),
            "outlays": data.get("outlays"),
        }
    else:
        print(f"Error fetching spending for agency {agency_code}: {response.status_code}")
        return None

def fetch_all_agency_spending(fiscal_year):
    """
    Fetches spending data for all top-tier government agencies.
    
    Args:
        fiscal_year (int): The fiscal year to retrieve data for.
    
    Returns:
        pd.DataFrame: A DataFrame containing spending data for all agencies.
    """
    agencies = get_all_agencies()
    spending_data = []
    for agency in agencies:
        agency_code = agency.get("toptier_code")
        agency_name = agency.get("agency_name")
        spending = get_agency_spending(agency_code, fiscal_year)
        if spending:
            spending["agency_name"] = agency_name
            spending_data.append(spending)
    
    # Create a DataFrame
    return pd.DataFrame(spending_data)

# Example usage
if __name__ == "__main__":
    fiscal_year = 2023  # Specify the fiscal year
    spending_df = fetch_all_agency_spending(fiscal_year)
    
    if not spending_df.empty:
        print(spending_df.head())
        # Save to CSV
        spending_df.to_csv("all_agency_spending.csv", index=False)

