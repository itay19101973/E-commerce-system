import requests


def get_all_countries():
    response = requests.get("https://countriesnow.space/api/v0.1/countries")
    response.raise_for_status()
    countries = response.json()

    allowed_countries = [
        country['country']
        for country in countries['data']
    ]
    return allowed_countries
