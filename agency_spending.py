import requests
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

BASE_URL = "https://api.usaspending.gov/api/v2/"
HEADERS = {"Content-Type": "application/json"}

def get_all_agencies():
    """
    Fetches a list of all top-tier government agencies.
    
    Returns:
        list: A list of agencies with their codes and names.
    """
    logging.info("Fetching all top-tier government agencies...")
    url = f"{BASE_URL}references/toptier_agencies/"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        logging.info(f"Successfully fetched {len(data.get('results', []))} agencies.")
        return data.get('results', [])
    else:
        logging.error(f"Error fetching agencies: {response.status_code}")
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
    logging.info(f"Fetching spending data for agency_code: {agency_code}, fiscal_year: {fiscal_year}...")
    url = f"{BASE_URL}agency/{agency_code}/budgetary_resources/"
    params = {"fiscal_year": fiscal_year}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        agency_data = data.get("agency_data_by_year", [])
        for year_data in agency_data:
            if year_data.get("fiscal_year") == fiscal_year:
                logging.info(f"Successfully fetched spending data for agency_code: {agency_code}.")
                return {
                    "agency_code": agency_code,
                    "fiscal_year": fiscal_year,
                    "total_budgetary_resources": year_data.get("total_budgetary_resources"),
                    "obligations_incurred": year_data.get("agency_total_obligated"),
                    "outlays": year_data.get("agency_budgetary_resources"),
                }
        logging.warning(f"No spending data found for agency_code: {agency_code} in fiscal_year: {fiscal_year}.")
    else:
        logging.error(f"Error fetching spending for agency {agency_code}: {response.status_code}")
    return None

def fetch_all_agency_spending(fiscal_year):
    """
    Fetches spending data for all top-tier government agencies.
    
    Args:
        fiscal_year (int): The fiscal year to retrieve data for.
    
    Returns:
        pd.DataFrame: A DataFrame containing spending data for all agencies.
    """
    logging.info(f"Starting to fetch spending data for all agencies for fiscal_year: {fiscal_year}...")
    agencies = get_all_agencies()
    spending_data = []
    for index, agency in enumerate(agencies):
        agency_code = agency.get("toptier_code")
        agency_name = agency.get("agency_name")
        logging.info(f"Processing agency {index + 1}/{len(agencies)}: {agency_name} (Code: {agency_code})")
        spending = get_agency_spending(agency_code, fiscal_year)
        if spending:
            spending["agency_name"] = agency_name
            spending_data.append(spending)
        else:
            spending_data.append({
                "agency_code": agency_code,
                "fiscal_year": fiscal_year,
                "total_budgetary_resources": None,
                "obligations_incurred": None,
                "outlays": None,
                "agency_name": agency_name,
            })
    
    # Create a DataFrame
    logging.info("Finished fetching data for all agencies.")
    return pd.DataFrame(spending_data)

# Example usage
if __name__ == "__main__":
    fiscal_year = 2023  # Specify the fiscal year
    logging.info("Script started.")
    spending_df = fetch_all_agency_spending(fiscal_year)
    
    if not spending_df.empty:
        logging.info(f"Saving data for {len(spending_df)} agencies to 'all_agency_spending.csv'.")
        spending_df.to_csv("all_agency_spending.csv", index=False)
    else:
        logging.warning("No data available to save.")
    
    logging.info("Script finished.")
