# CALCULATE THE HEX GRID
from django_extensions.management.jobs import DailyJob
from requests_html import HTMLSession


# this is a weekly job that loads GHCND data for all station
class Job(DailyJob):
    help = "Calculate the Hex Grid based on the data for particular day"

    def execute(self):

        # request
        session = HTMLSession()

        r = session.get('http://127.0.0.1:8000/calculate-hexGrid/2020-05-11/')

        c = r.html.render()  # this call executes the js in the page
        print(c)

        return True
