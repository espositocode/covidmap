import json
import requests
import statistics

API_KEY = "3e298e6f4f944fd2ab9d5a88e6d09ea8"

def gather(data, key, average=None):
    begin = True
    for idx, entry in enumerate(data):
        if begin and entry.get(key) == None:
            continue
        else:
            begin = False
        if average:
            history = [e[key] if e.get(key) else 0 for e in data[idx-average if idx > average else 0:idx+1]]
            yield statistics.mean(history)
        else:
            yield entry.get(key)


def get_country():
    print(f"Downloading country")
    r = requests.get(f'https://api.covidactnow.org/v2/country/US.timeseries.json?apiKey={API_KEY}')
    country = r.json()

    data = {
        "cd": [value for value in gather(country["metricsTimeseries"], "caseDensity")],
        "vcr": [value for value in gather(country["metricsTimeseries"], "vaccinationsCompletedRatio")],
        "nd": [value for value in gather(country["actualsTimeseries"], "newDeaths")]
    }

    with open('data/covidactnow/country.json', 'w') as f:
        f.write(json.dumps(data))


def get_counties():
    print(f"Downloading counties")
    r = requests.get(f'https://api.covidactnow.org/v2/counties.timeseries.json?apiKey={API_KEY}')
    counties = r.json()

    # build metricsTimeseries/vaccinationsCompletedRatio
    data = {}
    for county in counties:
        data[county["fips"]] = {
            "max": 1,
            "vcr": [value for value in gather(county["metricsTimeseries"], "vaccinationsCompletedRatio")]
        }

    with open("data/covidactnow/counties.vcr.json", "w") as f:
        f.write(json.dumps(data))

get_counties()
