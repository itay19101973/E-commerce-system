import requests


def get_all_countries() -> list[str]:
    """
    Fetches a list of all country names from the CountriesNow API.

    This function sends an HTTP GET request to the CountriesNow API endpoint,
    retrieves the country and city data, and extracts only the country names.

    Returns:
        list[str]: A list containing the names of all available countries.

    Raises:
        requests.exceptions.HTTPError: If the request to the API fails (non-200 status).
        requests.exceptions.RequestException: For any network-related errors.
    """
    response = requests.get("https://countriesnow.space/api/v0.1/countries")
    response.raise_for_status()
    countries = response.json()

    allowed_countries = [
        country['country']
        for country in countries['data']
    ]
    return allowed_countries
