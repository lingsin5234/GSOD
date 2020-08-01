from django_extensions.management.jobs import WeeklyJob
from gsod.oper.ghcnd_extract import get_request
from gsod.models import Station, GHCND
import datetime as dt
import json
import math
import time as t


# this is a weekly job that loads GHCND data for all station
class Job(WeeklyJob):
    help = "Extract GHCND data for every station"

    def execute(self):

        stations = Station.objects.all()

        for station in stations:

            # station id
            station_id = str(station.id)

            # run a get for the 7 days of two weeks (just in case it has not be updated)
            start_date = (dt.datetime.now() - dt.timedelta(days=21)).date()
            end_date = (dt.datetime.now() - dt.timedelta(days=14)).date()

            try:
                response = json.loads(get_request('GHCND', 'station', [station_id],
                                                  None, None, str(start_date), str(end_date), 0))
            except Exception as e:
                print('Error Response:', station_id, e)
            else:
                num_results = response['metadata']['resultset']['count']
                results = response['results']
                # print(num_results, results)

                # write to database if less than 1000 results
                if num_results <= 1000:
                    write_to_db(results, station)

                # if results over 1000, then keep going
                elif num_results > 1000:
                    rmd = math.ceil(num_results / 1000)
                    for i in range(0, rmd):
                        response = json.loads(get_request('GHCND', 'station', [station_id],
                                                          None, None, str(start_date), str(end_date), i * 1000))
                        results = response['results']

                        # write to database
                        write_to_db(results, station)

        return True


# write to database function
def write_to_db(results, station):
    for r in results:
        # convert datetime to date; convert station to QuerySet referencing the Station Object
        r['date'] = dt.datetime.strptime(r['date'], '%Y-%m-%dT%H:%M:%S').date()
        r['station'] = station
        # print(r)
        try:
            s = GHCND(**r)
            s.save()
        except Exception as e:
            print(e)
    t.sleep(0.5)
