import json
import requests

states = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]

COUNTRY_URL = 'https://api.covidactnow.org/v2/country/US.timeseries.json?apiKey=3e298e6f4f944fd2ab9d5a88e6d09ea8'
COUNTY_URL = 'https://api.covidactnow.org/v2/county/{state}.timeseries.json?apiKey=3e298e6f4f944fd2ab9d5a88e6d09ea8'

def get_country_data():
    print(f"Downloading country")
    r = requests.get(COUNTRY_URL)
    country = r.json()

    data = {
        "metrics": [entry["caseDensity"] for entry in country['metricsTimeseries']]
    }

    with open('data/country.json', 'w') as f:
        f.write(json.dumps(data))

def get_county_data():
    with open("resources/geo.json", "r") as f:
        data = json.loads(f.read())

    # {
    #     "testPositivityRatio": 0.032, 
    #     "caseDensity": 22.9, 
    #     "contactTracerCapacityRatio": null, 
    #     "infectionRate": 0.78, 
    #     "infectionRateCI90": 0.77, 
    #     "icuCapacityRatio": null, 
    #     "vaccinationsInitiatedRatio": 0.393, 
    #     "vaccinationsCompletedRatio": 0.343, 
    #     "vaccinationsAdditionalDoseRatio": null, 
    #     "date": "2021-11-25"
    #  }

    for state in states:
        print(f"Downloading {state}".format(state=state))
        r = requests.get(COUNTY_URL.format(state=state))
        counties = r.json()
        for county in counties:
            for feature in data["features"]:
                if feature['properties']['fips'] == county['fips']:
                    break
            else:
                print(f"Error: could not find {county['fips']}")
            feature["properties"]["metrics"] = [entry["caseDensity"] for entry in county['metricsTimeseries']]

    with open("data/county.geo.json", "w") as f:
        f.write(json.dumps(data))

get_country_data()
get_county_data()
