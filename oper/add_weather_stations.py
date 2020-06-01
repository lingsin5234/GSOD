# this script runs thru each state obtain at least 1 airport station
import requests
import json
import datetime as dte


# get the airports and weather stations -- ONLY GHCND for now
def retrieve_airport_and_weather_stations(dataset):
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
            if ("AIRPORT" in x['name']) and (max_date >= max_date_value) and (dataset in x['id']):
                airports.append(x['name'])
                airport_lst.append({
                    'name': x['name'],
                    'id': x['id'],
                    'latitude': x['latitude'],
                    'longitude': x['longitude'],
                    'elevation': x['elevation'],
                    'elevation_unit': x['elevationUnit'],
                    'us_state': s
                })
            elif ("WEATHER" in x['name']) and (max_date >= max_date_value) and (dataset in x['id']):
                weather.append(x['name'])
                weather_lst.append({
                    'name': x['name'],
                    'id': x['id'],
                    'latitude': x['latitude'],
                    'longitude': x['longitude'],
                    'elevation': x['elevation'],
                    'elevation_unit': x['elevationUnit'],
                    'us_state': s
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

    output = {
        'us_states': states,
        'airports': airports,
        'airport_lst': airport_lst,
        'weather': weather,
        'weather_lst': weather_lst
    }
    return output

