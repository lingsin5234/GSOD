from django_extensions.management.jobs import WeeklyJob
from gsod.oper.ghcnd_extract import get_request
from gsod.models import Station, GHCND
import datetime as dt
import json
import math
import time as t


# this is a weekly job that loads GHCND data for particular station
class Job(WeeklyJob):
    help = "Extract GHCND data for particular station"

    def execute(self):

        station = Station.objects.get(id='GHCND:CA1AB000001')

        # run a get for the 7 days of last week (not the past week)
        start_date = (dt.datetime.now() - dt.timedelta(days=14)).date()
        end_date = (dt.datetime.now() - dt.timedelta(days=7)).date()
        # print(start_date, end_date)
        response = json.loads(get_request('GHCND', 'station', ['GHCND:CA1AB000001'],
                                          None, None, str(start_date), str(end_date), 0))
        num_results = response['metadata']['resultset']['count']
        results = response['results']
        # print(num_results, results)

        # write to database if less than 1000 results
        if num_results <= 1000:
            for r in results:
                # convert datetime to date; convert station to QuerySet referencing the Station Object
                r['date'] = dt.datetime.strptime(r['date'], '%Y-%m-%dT%H:%M:%S').date()
                r['station'] = station
                # print(r)
                s = GHCND(**r)
                s.save()
            t.sleep(0.5)

        # if results over 1000, then keep going
        elif num_results > 1000:
            rmd = math.ceil(num_results / 1000)
            for i in range(0, rmd):
                response = json.loads(get_request('GHCND', 'station', ['GHCND:CA1AB000001'],
                                                  None, None, str(start_date), str(end_date), i * 1000))
                num_results = response['metadata']['resultset']['count']
                results = response['results']

                # write to database
                for r in results:
                    # convert datetime to date; convert station to QuerySet referencing the Station Object
                    r['date'] = dt.datetime.strptime(r['date'], '%Y-%m-%dT%H:%M:%S').date()
                    r['station'] = station
                    s = GHCND(**r)
                    s.save()
                t.sleep(0.5)

        return True
