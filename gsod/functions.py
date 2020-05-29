# this testing script will extract and load stations to the Models
from .oper import ghcnd_extract as ge
from .oper import add_weather_stations as aws
import json
from itertools import islice
from .models import Station, GHCND
import time as t
from operator import itemgetter as ig


# this test run grabs all FIPS:CA stations -- mostly canadian
def test_run():
    # get list of stations
    results = ge.get_stations(['CA'], 'FIPS', 0)
    results = json.loads(results)
    # stations = results['results']
    count = results['metadata']['resultset']['count'] // 1000 + 1

    # setup objects for importing the Stations
    for c in range(count):
        print(c)
        results = ge.get_stations(['CA'], 'FIPS', c * 1000)
        results = json.loads(results)
        stations = results['results']
        for i in stations:
            y = Station(**i)
            y.save()
        t.sleep(0.5)

    return True


# this test run grabs specified Edmonton station data
def test_yeg(station_objs, start_date, end_date):

    # pull the names of stations from stations QuerySet
    stations = []
    for s in station_objs:
        stations.append(s.id)

    # get data from specific stations
    results = ge.get_request('GHCND', 'station', stations, '', [''], start_date, end_date, 0)
    results = json.loads(results)
    # data = results['results']
    count = results['metadata']['resultset']['count'] // 1000 + 1

    # setup objects for importing the Stations
    for c in range(count):
        # figure out timing
        st = t.time()

        results = ge.get_request('GHCND', 'station', stations, '', [''], start_date, end_date, c * 1000)
        results = json.loads(results)
        data = results['results']
        for i in data:
            # save only the date; ignore the time
            i['date'] = i['date'][0:10]

            # get the corresponding station
            this_station = Station.objects.get(id=i['station'])
            i['station'] = this_station

            # create object and save to database
            y = GHCND(**i)
            # print(y)
            y.save()

        et = t.time()
        print(c, str(et - st))
        t.sleep(0.1)  # process above takes a bit of time since it's saving one by one

    return True


# this function adds a Station Model to database
def add_station(station_details):

    s = Station(**station_details)
    s.save()

    return True


# this function runs the add_weather_stations functions
def run_add_stations():

    lst = aws.retrieve_airport_and_weather_stations('GHCND')
    usr_input = input('run airports? (Y/N)')
    if usr_input == 'Y':
        add_airports(lst['us_states'], lst['airport_lst'])
    usr_input = input('run weather stations? (Y/N)')
    if usr_input == 'Y':
        add_weather_stations(lst['us_states'], lst['weather_lst'])
    print("Completed run_add_stations function call.")

    return True


#  ----------  ADD Airports Models  ----------  #
def add_airports(states, airport_lst):
    total = 0

    # loop thru each state and check which airports to add
    for s in states:

        # list the airports for US state, then user inputs which ones to add to Models
        lst_this_state = []
        for a in airport_lst:
            if a['us_state'] == s:
                lst_this_state.append(a)

        # run thru the list and ask for user input
        lst_count = 1
        for a in lst_this_state:
            print((str(lst_count) + '.'), a['name'])
            lst_count += 1

        usr_input = input("Type number(s) to write to model, separate by space for more than one.\n")
        if usr_input == 'exit':
            return False
        selected = [int(n)-1 for n in usr_input.split(' ') if n != '']
        if len(selected) > 0:
            print("SELECTED: ", selected, ig(*selected)(lst_this_state))
            input("Hit Enter to add.")

            # adding the specified airport to Models
            for l in selected:
                apt_details = lst_this_state[l]
                new_dict = {
                    'id': apt_details['id'],
                    'name': apt_details['name'],
                    'latitude': apt_details['latitude'],
                    'longitude': apt_details['longitude'],
                    'elevation': apt_details['elevation'],
                    'elevation_unit': apt_details['elevation_unit'],
                    'us_state': apt_details['us_state']
                }
                add_station(new_dict)

            total += len(selected)
            print(len(selected), "airports added for", s)
        else:
            print("No airports added for", s)
        input("Enter to continue.")

    print(total, "airports have been added.")
    return True


#  ----------  ADD Airports Models  ----------  #
def add_weather_stations(states, weather_lst):
    total = 0

    # loop thru each state and check which weather stations to add
    for s in states:

        # list the weather stations for US state, then user inputs which ones to add to Models
        lst_this_state = []
        for a in weather_lst:
            if a['us_state'] == s:
                lst_this_state.append(a)

        # run thru the list and ask for user input
        lst_count = 1
        for a in lst_this_state:
            if a['us_state'] == s:
                print((str(lst_count) + '.'), a['name'])
                lst_count += 1
        usr_input = input("Type number(s) to write to model, separate by space for more than one.\n")
        if usr_input == 'exit':
            return False
        selected = [int(n)-1 for n in usr_input.split(' ') if n != '']
        if len(selected) > 0:
            print("SELECTED: ", ig(*selected)(lst_this_state))
            input("Hit Enter to add.")

            # adding the specified weather to Models
            for l in selected:
                wst_details = lst_this_state[l]
                new_dict = {
                    'id': wst_details['id'],
                    'name': wst_details['name'],
                    'latitude': wst_details['latitude'],
                    'longitude': wst_details['longitude'],
                    'elevation': wst_details['elevation'],
                    'elevation_unit': wst_details['elevation_unit'],
                    'us_state': wst_details['us_state']
                }
                add_station(new_dict)

            total += len(selected)
            print(len(selected), "weather stations added for", s)
        else:
            print("No airports added for", s)
        input("Enter to continue.")

    print(total, "weather stations have been added.")
    return True
