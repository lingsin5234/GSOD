from django_extensions.management.jobs import DailyJob
from gsod.models import Station
import json


# this is an ad-hoc daily job that adds a single station to the database
class Job(DailyJob):
    help = "Add Single Station to Database."

    def execute(self):

        station_id = 'GHCND:USW00024021'
        state = 'Wyoming'

        filename = 'static/data/gsoddata/' + state + '.json'
        with open(filename, 'r') as readfile:
            jl = json.load(readfile)

        for x in jl[0]['results']:
            if station_id == x['id']:
                new_station = {
                    'name': x['name'],
                    'id': x['id'],
                    'latitude': x['latitude'],
                    'longitude': x['longitude'],
                    'elevation': x['elevation'],
                    'elevation_unit': x['elevationUnit'],
                    'us_state': state
                }
                break

        try:
            s = Station(**new_station)
        except Exception as e:
            print("FAILED TO ADD:", new_station['name'], "\n", e)
        else:
            s.save()
            print("Successfully added new station:", new_station['name'])

        return True
