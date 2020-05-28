# this sets up the basic dimension and value tables in the database for the US states
import requests
import json
import time as t
import datetime as dte
import numpy as np
from . import database_schema as dsh
from . import database_transactions as dbt

# '''
#  ----------  load all 50 states + DC  ----------  #
url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=ST&limit=52&offset=0'
header = 'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'
x = requests.get(url, headers={'token': header})
results = json.loads(x.text)

# write to file
with open('static/data/gsoddata/us_stations.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

# re-write the states list of dictionaries
states = []
for s in results['results']:
    new_dict = {
        'location_id': s['id'],
        'name': s['name'],
        'location_type': 'US state'
    }
    states.append(new_dict)

# write states to database
c = dsh.engine.connect()
try:
    c.execute(dsh.locations_dim.insert(), states)
except Exception as e:
    print('States Insert Error:', e)

# check that its written
# query = 'SELECT * FROM locations_dim'
# results = dbt.gsod_db_reader(query)
# print(results)
# '''

# '''
#  ----------  grab all stations FIPS   ----------  #
# set the minimum acceptance date to 1970-01-01
minAcceptanceDate = dte.datetime.strptime('1970-01-01', '%Y-%m-%d').date()

# grab all stations FIPS
with open('static/data/gsoddata/us_stations.json', 'r') as readfile:
    jl = json.load(readfile)
FIPS = []
for s in jl['results']:
    new_dict = {
        'state': s['name'],
        'fips': s['id']
    }
    FIPS.append(new_dict)
# print(FIPS)
FIPS = [{'state': 'Wyoming', 'fips': 'FIPS:56'}]
# loop thru each state to grab first 1000 stations, then store in dim tables
url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?limit=1000&startdate=1970-01-01&locationid='
header = 'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'

for f in FIPS:
    get_url = url + f['fips']
    filename = 'static/data/gsoddata/' + f['state'] + '.json'
    x = requests.get(get_url, headers={'token': header})

    # get location primary key for current FIPS
    query = "SELECT Id FROM locations_dim WHERE location_id='" + f['fips'] + "'"
    result = dbt.gsod_db_reader(query)
    loc_id, = result[0]  # unpack a tuple, but no second value, so just put a comma

    # write to file
    with open(filename, 'w') as outfile:
        json.dump(json.loads(x.text), outfile, indent=4)

    # reshape stations for loading to database
    results = json.loads(x.text)['results']
    stations = []
    list_ids = []
    for s in results:
        if 'elevation' not in s.keys():
            s['elevation'] = None
            s['elevationUnit'] = None
        if dte.datetime.strptime(s['maxdate'], '%Y-%m-%d').date() >= minAcceptanceDate:
            new_dict = {
                'station_id': s['id'],
                'name': s['name'],
                'elevation': s['elevation'],
                'elevation_unit': s['elevationUnit'],
                'latitude': s['latitude'],
                'longitude': s['longitude'],
                'location': loc_id
            }
            list_ids.append(s['id'])
            stations.append(new_dict)
        else:
            # check that if statement works
            print(s['maxdate'])

    # write to database
    try:
        c.execute(dsh.stations_dim.insert(), stations)
    except Exception as e:
        print(f['state'], 'processing:', e)

        # find and remove dupes
        query = 'SELECT station_id from stations_dim'
        res = dbt.gsod_db_reader(query)
        st_id = [n for n, in res]
        full_list = np.setdiff1d(list_ids, st_id)
        exists = [list_ids.index(x) for x in full_list]
        dup = list(reversed(np.setdiff1d([*range(0, len(list_ids))], exists).tolist()))
        print("DUPES:", dup, type(dup))
        for d in dup:
            stations.pop(d)
        print("REMOVE DUPES:", len(full_list), len(stations))

        # write to database
        try:
            c.execute(dsh.stations_dim.insert(), stations)
        except Exception as e2:
            print(f['state'], 'processing:', e2)

    # check that its written
    query = 'SELECT * FROM stations_dim WHERE location=' + str(loc_id)
    results = dbt.gsod_db_reader(query)
    # print(results)
    if len(results) > 0:
        print(f['state'], 'completed -', len(stations), ' stations added.')
    else:
        exit()
    t.sleep(10)

c.close()
# '''
