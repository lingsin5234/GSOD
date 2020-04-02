# this script is used to test the ETL scripts
import ghcnd_extract as ge
import requests


json_output = ge.get_request('GHCND', ['28801', '92604'], '2020-03-30', '2020-04-02')
print(json_output)

stations = ge.get_stations(['92604'], 'ZIP')
print(stations)

locations = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locations/ZIP:92604',
                         headers={'token':'KbJOBjuzWvVPHMCwEoGxOCQJOCMTjHAb'})
print(locations.text)
