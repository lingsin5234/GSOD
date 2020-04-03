# this script is used to test the ETL scripts
import ghcnd_extract as ge
import requests

'''
json_output = ge.get_request('GHCND', ['28801', '92604'], '2020-01-01', '2020-04-02')
print(json_output)

stations = ge.get_stations(['92604'], 'ZIP')
print(stations)
'''
loc_cat = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locationcategories?startdate=2020-01-01',
                       headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(loc_cat.text)
# locations = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=CNTRY',
locations = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locations/FIPS:CA',
                         headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(locations.text)
'''
data_type = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/datacategories',
                         headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(data_type.text)
'''
stations = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:CA&datasetid=GHCND&startdate=2020-01-01&limit=1000&offset=1000',
                        headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(stations.text)
