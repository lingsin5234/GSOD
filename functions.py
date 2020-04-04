# this testing script will extract and load stations to the Models
from .oper import ghcnd_extract as ge
import json
from itertools import islice
from .models import Station
from time import sleep


# this test run grabs all FIPS:CA stations -- mostly canadian
def test_run():
    # get list of stations
    results = ge.get_stations(['CA'], 'FIPS', 0)
    results = json.loads(results)
    stations = results['results']
    count = results['metadata']['resultset']['count'] // 1000 + 1

    # setup objects for importing the Stations
    for c in range(count):
        print(c)
        results = ge.get_stations(['CA'], 'FIPS', c * 1000)
        results = json.loads(results)
        stations = results['results']
        for i in stations:
            y = Station(**i)
            y.save()
        sleep(0.5)

    return True


# this test run grabs specified Edmonton station data
def test_yeg(stations, start_date, end_date):

    # get data from specific stations
    # for s in stations:
    results = ge.get_request('GHCND', 'station', stations, '', [''], start_date, end_date)
    print(results)

    return True
