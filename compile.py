import json
import requests
import statistics

COUNTRY_URL = 'https://api.covidactnow.org/v2/country/US.timeseries.json?apiKey=3e298e6f4f944fd2ab9d5a88e6d09ea8'
COUNTIES_URL = 'https://api.covidactnow.org/v2/counties.timeseries.json?apiKey=3e298e6f4f944fd2ab9d5a88e6d09ea8'

def get_country():
    print(f"Downloading country")
    r = requests.get(COUNTRY_URL)
    country = r.json()

    data = {}
   
    data["cd"] = []
    begin = True
    for entry in country["metricsTimeseries"]:
        if begin and entry.get("caseDensity") == None:
            continue
        else:
            begin = False
        data["cd"].append(entry.get("caseDensity"))

    data["vr"] = []
    begin = True 
    for entry in country["metricsTimeseries"]:
        if begin and entry.get("vaccinationsCompletedRatio") == None:
            continue
        else:
            begin = False
        data["vr"].append(entry.get("vaccinationsCompletedRatio"))

    data["nd"] = []
    begin = True
    history = 7
    for idx, entry in enumerate(country["actualsTimeseries"]):
        if begin and entry.get("newDeaths") == None:
            continue
        else:
            begin = False
        week = [actuals["newDeaths"] if actuals.get("newDeaths") else 0 for actuals in country["actualsTimeseries"][idx-history if idx > history else 0:idx+1]]
        data["nd"].append(statistics.mean(week))

    with open('data/country.json', 'w') as f:
        f.write(json.dumps(data))

def get_counties():
    with open("resources/geo.json", "r") as f:
        data = json.loads(f.read())
        
    print(f"Downloading counties")
    r = requests.get(COUNTIES_URL)
    counties = r.json()
    for county in counties:
        # print(county)
        for feature in data["features"]:
            if feature['properties']['fips'] == county['fips']:
                break
        else:
            print(f"Error: could not find {county['fips']}")
        feature["properties"]["cd"] = [round(entry["caseDensity"]) if entry.get("caseDensity") != None else None for entry in county['metricsTimeseries']]

    with open("data/county.geo.json", "w") as f:
        f.write(json.dumps(data))

get_country()
get_counties()
