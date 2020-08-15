# CALCULATE THE HEX GRID
from django_extensions.management.jobs import DailyJob
from selenium.common.exceptions import TimeoutException
from gsod.oper import database_transactions as dbt
from gsod.oper import hexgrid_constructor as hc
from gsod.models import Station, GHCND
import datetime as dte
import json


# this is a weekly job that loads GHCND data for all station
class Job(DailyJob):
    help = "Calculate the Hex Grid based on the data for particular day"

    def execute(self):

        # for the job_runs database
        start_time = dte.datetime.now()
        query = "SELECT Id FROM jobs_dim WHERE job_name='calculate_hexGrid_migrate'"
        job_id = [n for (n,) in dbt.gsod_db_reader(query)][0]
        log_file = 'gsod/seleniumLog/' + str(dte.datetime.now().date()) + '.log'

        bbox = [-126, 24, -66.5, 50]  # USA
        cellSide = 15

        # get ALL Weather Stations
        stations = Station.objects.all()
        data_types = ['TMAX', 'TMIN']  # ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN']

        # get ghcnd info for specific day: 2020-05-16 and datatype=TMAX
        this_date = '2020-01-02'

        st_json = []
        for s in stations:
            if s.us_state == 'Alaska' or s.us_state == 'Hawaii':
                continue
            # if s.us_state != 'Alaska':  # only get alaska
            #     continue

            # create dictionary to load info to template view
            new_dict = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        s.longitude,
                        s.latitude
                    ]
                },
                'properties': {}
            }

            # generate dict based on all listed data types
            for d in data_types:
                try:
                    ghcnd = GHCND.objects.get(station__id=s.id, date=this_date, datatype=d)
                except Exception as e:
                    continue
                else:
                    new_dict['properties'][d] = ghcnd.value / 10

                    # add dict to list
                    st_json.append(new_dict)

        try:
            hexGrid = hc.hexgrid_constructor(bbox, cellSide, st_json, 8, (24 + 50) / 2)
            print("Calculations completed!")
            filename = 'hexGrid_' + str(this_date) + '.json'
            try:
                with open('gsod/posts/' + filename, 'w') as outfile:
                    json.dump(hexGrid, outfile, indent=4)
            except Exception as e:
                print('POST write to file: Failed', e)
                with open(log_file, 'a') as outfile:
                    outfile.write('POST write to file: Failed' + str(e) + '\n')
                status = False
            else:
                print('POST write to file: Success!')
                with open(log_file, 'a') as outfile:
                    outfile.write('POST write to file: Success!' + '\n')
                status = True
        except TimeoutException:
            print("Loading took too much time!", this_date)
            dbt.log_gsod_job_run(job_id, str(this_date), start_time, 'FAILED')
            status = False
        else:
            # after each completion, take a 10 minute break
            dbt.log_gsod_job_run(job_id, str(this_date), start_time, 'COMPLETED')

        return status
