# this testing script will extract and load stations to the Models
from .oper import ghcnd_extract as ge
import json
from itertools import islice
from .models import Station, GHCND
import time as t


# this test run grabs all FIPS:CA stations -- mostly canadian
def test_run():
    # get list of stations
    results = ge.get_stations(['CA'], 'FIPS', 0)
    results = json.loads(results)
    # stations = results['results']
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
        t.sleep(0.5)

    return True


# this test run grabs specified Edmonton station data
def test_yeg(station_objs, start_date, end_date):

    # pull the names of stations from stations QuerySet
    stations = []
    for s in station_objs:
        stations.append(s.id)

    # get data from specific stations
    results = ge.get_request('GHCND', 'station', stations, '', [''], start_date, end_date, 0)
    results = json.loads(results)
    # data = results['results']
    count = results['metadata']['resultset']['count'] // 1000 + 1

    # setup objects for importing the Stations
    for c in range(count):
        # figure out timing
        st = t.time()

        results = ge.get_request('GHCND', 'station', stations, '', [''], start_date, end_date, c * 1000)
        results = json.loads(results)
        data = results['results']
        for i in data:
            # save only the date; ignore the time
            i['date'] = i['date'][0:10]

            # get the corresponding station
            this_station = Station.objects.get(id=i['station'])
            i['station'] = this_station

            # create object and save to database
            y = GHCND(**i)
            # print(y)
            y.save()

        et = t.time()
        print(c, str(et - st))
        t.sleep(0.1)  # process above takes a bit of time since it's saving one by one

    return True
