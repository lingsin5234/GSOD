# this script runs thru each state obtain at least 1 airport station
import requests
import json
import datetime as dte
from operator import itemgetter as ig
from gsod.models import Station


# load the states
with open('static/data/gsoddata/us_stations.json', 'r') as readfile:
    jl = json.load(readfile)

states = []
for s in jl['results']:
    states.append(s['name'])

# loop thru each state and search stations with "AIRPORT" or "WEATHER"
airports = []
airport_lst = []
weather = []
weather_lst = []
for s in states:
    filename = 'static/data/gsoddata/' + s + '.json'
    with open(filename, 'r') as readfile:
        jl = json.load(readfile)

    for x in jl[0]['results']:
        max_date = dte.datetime.strptime(x['maxdate'], '%Y-%m-%d').date()
        max_date_value = dte.datetime.strptime('2020-05-01', '%Y-%m-%d').date()
        if ("AIRPORT" in x['name']) and (max_date >= max_date_value):
            airports.append(x['name'])
            airport_lst.append({
                'name': x['name'],
                'id': x['id'],
                'latitude': x['latitude'],
                'longitude': x['longitude'],
                'elevation': x['elevation'],
                'elevation_unit': x['elevationUnit'],
                'state': s
            })
        elif ("WEATHER" in x['name']) and (max_date >= max_date_value):
            weather.append(x['name'])
            weather_lst.append({
                'name': x['name'],
                'id': x['id'],
                'latitude': x['latitude'],
                'longitude': x['longitude'],
                'elevation': x['elevation'],
                'elevation_unit': x['elevationUnit'],
                'state': s
            })

# print("AIRPORTS:", airports)
# print("AIRPORT_LST:", airport_lst)
# print("WEATHER:", weather)
# print("WEATHER_LST:", weather_lst)
print(len(airports), len(airport_lst), len(weather), len(weather_lst))

# write airports, then write weather stations
with open('static/data/gsoddata/airports.json', 'w') as outfile:
    json.dump(airport_lst, outfile, indent=4)
with open('static/data/gsoddata/weather_stations.json', 'w') as outfile:
    json.dump(weather_lst, outfile, indent=4)


#  ----------  ADD Airports / Weather Station Models  ----------  #
# loop thru each state and check which airports and weather stations to add
for s in states:

    # list the airports for US state, then user inputs which ones to add to Models
    lst_count = 1
    for a in airport_lst:
        if a['state'] == s:
            print((str(lst_count) + '.'), a['name'])
            lst_count += 1
    usr_input = input("Type number(s) to write to model, separate by space for more than one.\n")
    selected = [int(n)-1 for n in usr_input.split(' ') if n != '']
    print("SELECTED: ", ig(*selected)(airports))

    # adding the specified airport to Models
    for l in selected:
        apt_details = airport_lst[l]
        new_dict = {
            'id': apt_details['id'],
            'name': apt_details['name'],
            'latitude': apt_details['latitude'],
            'longitude': apt_details['longitude'],
            'elevation': apt_details['elevation'],
            'elevation_unit': apt_details['elevation_unit'],
            'state': apt_details['state']
        }

    print(len(selected), "airports added for", s)
    input("Enter to continue.")





