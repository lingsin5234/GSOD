# CALCULATE THE HEX GRID
from django_extensions.management.jobs import DailyJob
import requests
import json


# this is a weekly job that loads GHCND data for all station
class Job(DailyJob):
    help = "Calculate the Hex Grid based on the data for particular day"

    def execute(self):

        #

        return True
