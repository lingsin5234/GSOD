# this is a new extract script for the noaa site using the cdc api
import requests
header = 'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'


def get_request(dataset, locations, start_date, end_date):

    json_data = []
    url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?'
    loc = ''

    # ...data?datasetid=GHCND&locationid=ZIP:28801&startdate=2010-05-01&enddate=2010-05-01
    for l in locations:
        loc += l + '&'

    url += 'datasetid=' + dataset + '&locationid=ZIP:' + loc + 'startdate=' + start_date + '&enddate=' + end_date

    x = requests.get(url, headers={'token': header})
    json_data = x.text

    return json_data


def get_stations(locations, location_type, offset):

    json_data = []
    url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
    loc = ''

    # ...data?datasetid=GHCND&locationid=ZIP:28801&startdate=2010-05-01&enddate=2010-05-01
    if location_type == 'ALL':
        x = requests.get(url, headers={'token': header})
    else:
        for l in locations:
            loc += l + '&'
        url += '?locationid=' + location_type + ':' + loc + 'limit=1000&offset=' + str(offset)
        print(url, location_type, loc)
        x = requests.get(url, headers={'token': header})

    json_data = x.text

    return json_data
