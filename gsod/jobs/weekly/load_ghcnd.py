from django_extensions.management.jobs import WeeklyJob
from gsod.oper.ghcnd_extract import get_request
import datetime as dt


# this is a weekly job that loads GHCND data for particular station
class Job(WeeklyJob):
    help = "Extract GHCND data for particular station"

    def execute(self):

        # run a get for the past 7 days
        start_date = (dt.datetime.now() - dt.timedelta(days=7)).date()
        end_date = dt.date.today()
        # print(start_date, end_date)
        print(get_request('GHCND', 'station', ['GHCND:CA1AB000072'], None, None, str(start_date), str(end_date), 100))

        return True
