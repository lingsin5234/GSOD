from django_extensions.management.jobs import DailyJob
from gsod.oper.ghcnd_extract import get_request
from gsod.oper import database_transactions as dbt
from gsod.models import Station, GHCND
import datetime as dt
import json
import math
import time as t


# this is an ad-hoc daily job that loads GHCND data for a single station
class Job(DailyJob):
    help = "Extract GHCND data for a single station"

    def execute(self):

        start_time = dt.datetime.now()
        station_id = 'GHCND:USW00024021'
        station = Station.objects.get(id=station_id)

        # run a get for the 7 days of two weeks (just in case it has not be updated)
        start_date = dt.date(2020, 1, 1)
        # start_date = (dt.datetime.now() - dt.timedelta(days=21)).date()
        end_date = (dt.datetime.now() - dt.timedelta(days=14)).date()

        # for the job_runs database
        query = "SELECT Id FROM jobs_dim WHERE job_name='load_ghcnd'"
        job_id = [n for (n,) in dbt.gsod_db_reader(query)][0]
        job_var = str(start_date) + ' - ' + str(end_date)

        failed = 0
        try:
            response = json.loads(get_request('GHCND', 'station', [station_id],
                                              None, None, str(start_date), str(end_date), 0))
        except Exception as e:
            print('Error Response:', station_id, e)
            failed += 1
        else:
            try:
                num_results = response['metadata']['resultset']['count']
                results = response['results']
                # print(num_results, results)
            except Exception as e2:
                print('Error in Result:', station_id, e2)
                failed += 1
            else:
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

        # once all complete, write to job_run
        if failed == 0:
            dbt.log_gsod_job_run(job_id, job_var, start_time, 'COMPLETED')
        elif failed <= 1:
            dbt.log_gsod_job_run(job_id, job_var, start_time, 'SOME FAILURES - CHECK LOGS')
        else:
            dbt.log_gsod_job_run(job_id, job_var, start_time, 'FAILED')

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
