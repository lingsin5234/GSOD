# this testing script will extract and load stations to the Models
from .oper import ghcnd_extract as ge
import json
from itertools import islice
from .models import Station


def test_run():
    # get list of stations
    results = ge.get_stations(['CA'], 'FIPS')
    results = json.loads(results)
    stations = results['results']

    # setup objects for importing the Stations
    for i in stations:
        y = Station(**i)
        y.save()

    return True
