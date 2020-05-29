# this script is used to test the ETL scripts
import requests
import json
import collections
import time as t
import numpy as np
from . import database_schema as dsh
from . import database_transactions as dbt

'''
json_output = ge.get_request('GHCND', ['28801', '92604'], '2020-01-01', '2020-04-02')
print(json_output)

stations = ge.get_stations(['92604'], 'ZIP')
print(stations)

loc_cat = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locationcategories?startdate=2020-01-01',
                       headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(loc_cat.text)

locations = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locations/FIPS:CA',
                         headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(locations.text)
'''
'''
data_type = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/datacategories',
                         headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(data_type.text)
'''
'''
stations = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:CA&datasetid=GHCND&startdate=2020-01-01&limit=1000&offset=1000',
                        headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(stations.text)

stations = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=CNTRY',
                        headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(stations.text)
'''
'''
stations = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:CA',
                        headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(stations.text)

stations = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/stations/GHCND:CA1AB000064',
                        headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(stations.text)
'''
'''
data = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid=GHCND:CA1AB000001&stationid=GHCND:CA1AB000002&startdate=2020-03-31&enddate=2020-04-04',
                       headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(data.text)
'''
'''
dataset = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets/GHCND',
                       headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(dataset.text)

dataset = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets?stationid=GHCND:CA1AB000001',
                       headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(dataset.text)
'''

'''
# check errors in STATE.json loads
with open('static/data/gsoddata/Delaware.json', 'r') as readfile:
    jl = json.load(readfile)
ids = []
for s in jl['results']:
    ids.append(s['id'])
print([item for item, count in collections.Counter(ids).items() if count > 1])

query = 'SELECT station_id from stations_dim'
results = dbt.gsod_db_reader(query)
stations = [n for n, in results]

# get duplicates
full_list = np.setdiff1d(ids, stations)
exists = [ids.index(x) for x in full_list]
dups = np.setdiff1d([*range(0, len(ids))], exists).tolist()
print(len(full_list), len(ids), len(stations))
print(exists)
print(type(dups), list(reversed(dups)))
print(ids[124])

query = "SELECT * FROM stations_dim WHERE station_id='COOP:071200'"
results = dbt.gsod_db_reader(query)
print(results)
'''
'''
# run a request for a particular station
param = 'datasetid=GHCND&stationid=GHCND:USW00094274&startdate=2020-01-01&enddate=2020-05-29&limit=200'
get_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?' + param
header = 'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'
x = requests.get(get_url, headers={'token': header})
print(x.text)
'''
