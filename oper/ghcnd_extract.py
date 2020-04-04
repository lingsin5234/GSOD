# this is a new extract script for the noaa site using the cdc api
import requests
header = 'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'


# getting a regular data request using data
def get_request(dataset, loc_or_sta, stations, location_type, locations, start_date, end_date):

    json_data = []
    url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?'
    loc = ''

    if loc_or_sta == 'location':
        # ...data?datasetid=GHCND&locationid=ZIP:28801&startdate=2010-05-01&enddate=2010-05-01
        for l in locations:
            loc += l + '&'

        url += 'datasetid=' + dataset + '&locationid=' + location_type + ':' + loc + \
               'startdate=' + start_date + '&enddate=' + end_date
    else:
        for s in stations:
            loc += '&stationid=' + s

        url += 'datasetid=' + dataset + loc + '&startdate=' + start_date + '&enddate=' + end_date
        print(url)

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
