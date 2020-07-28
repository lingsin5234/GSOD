from django.shortcuts import render
from djangoapps.utils import get_this_template
import os
import json
from .models import Station, GHCND
from django.core.serializers.json import DjangoJSONEncoder
from .functions import test_run, test_yeg, run_add_stations, date_range
from .mapping import basic_map, basic_data_map
# from .forms import StationDatesForm -- defunct
# from django.db.models import Max, Min
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import datetime as dte


# homepage
def homepage(request):

    return render(request, 'pages/gsod_home.html')


# project page
def project_markdown(request):

    page_height = 1050
    f = open('gsod/README.md', 'r')
    if f.mode == 'r':
        readme = f.read()
        page_height = len(readme)/2 + 200

    content = {
        'readme': readme,
        'page_height': page_height
    }

    template_page = get_this_template('gsod', 'project.html')

    return render(request, template_page, content)


# stations list
def list_stations(request):

    # x = test_run()
    run_add_stations()

    stations = Station.objects.all()

    context = {
        'stations': stations
    }

    return render(request, 'pages/stations.html', context)


# this is test map using USA
def map_test(request):

    # get all stations and ghcnds
    stations = Station.objects.all()
    data_types = ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN']

    # json lists
    dates_json = []

    # go thru dates and populate the json structure
    start_date = dte.date(2020, 5, 9)
    end_date = dte.date(2020, 5, 16)  # date + 1 to end on 16th

    for this_date in date_range(start_date, (end_date + dte.timedelta(1))):
        # get ghcnd info for specific day: 2020-05-16 and datatype=TMAX
        get_date = this_date

        st_json = []
        for s in stations:
            # create dictionary to load info to template view
            new_dict = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        s.longitude,
                        s.latitude
                    ]
                },
                'properties': {}
            }

            # generate dict based on all listed data types
            for d in data_types:
                try:
                    ghcnd = GHCND.objects.get(station__id=s.id, date=get_date, datatype=d)
                except Exception as e:
                    # print(s.id, 'no data found for', d)
                    new_dict['properties'][d] = None
                else:
                    new_dict['properties'][d] = ghcnd.value / 10

            # add dict to list
            st_json.append(new_dict)
            # print(st_json)

        dates_json.append({
            'key': get_date,
            'data': st_json
        })

    context = {
        'mapbox_access_token': os.environ.get('mapbox_access_token'),
        'stations': json.dumps(dates_json, cls=DjangoJSONEncoder),
        'start_date': dte.date.strftime(start_date, '%Y-%m-%d'),
        'end_date': dte.date.strftime(end_date, '%Y-%m-%d')
    }

    return render(request, 'pages/map.html', context)


# testing out what a contour layout looks like
def contour_test(request):

    # get all stations and ghcnds
    stations = Station.objects.all()
    data_types = ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN']

    # json lists
    dates_json = []

    # go thru dates and populate the json structure
    start_date = dte.date(2020, 5, 9)
    end_date = dte.date(2020, 5, 16)  # date + 1 to end on 16th

    for this_date in date_range(start_date, (end_date + dte.timedelta(1))):
        # get ghcnd info for specific day: 2020-05-16 and datatype=TMAX
        get_date = this_date

        st_json = []
        for s in stations:
            # create dictionary to load info to template view
            new_dict = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        s.longitude,
                        s.latitude
                    ]
                },
                'properties': {}
            }

            # generate dict based on all listed data types
            for d in data_types:
                try:
                    ghcnd = GHCND.objects.get(station__id=s.id, date=get_date, datatype=d)
                except Exception as e:
                    # print(s.id, 'no data found for', d)
                    new_dict['properties'][d] = None
                else:
                    new_dict['properties'][d] = ghcnd.value / 10

            # add dict to list
            st_json.append(new_dict)
            # print(st_json)

        dates_json.append({
            'key': get_date,
            'data': st_json
        })

    context = {
        'mapbox_access_token': os.environ.get('mapbox_access_token'),
        'stations': json.dumps(dates_json, cls=DjangoJSONEncoder),
        'start_date': dte.date.strftime(start_date, '%Y-%m-%d'),
        'end_date': dte.date.strftime(end_date, '%Y-%m-%d')
    }

    return render(request, 'pages/contour.html', context)


# this is mapbox test zooming in on Edmonton
def map_box_test(request):

    context = {
        'mapbox_access_token': os.environ.get('mapbox_access_token')
    }

    return render(request, 'pages/mapbox.html', context)


# quick table view of specific station data
def station_data_table(request, station_id):

    data = GHCND.objects.filter(station=station_id)
    header = ['station', 'date', 'datatype', 'attribute', 'value']
    print(data)

    context = {
        'header': header,
        'body': data
    }

    return render(request, 'pages/quickTable.html', context)


# 2D Gradient test -- forked from GitHub: dismedia/gradient2d
def test_2dGradient(request):

    context = {
        'mapbox_access_token': os.environ.get('mapbox_access_token')
    }

    return render(request, 'pages/test.html', context)


def hexagon_test(request):

    # get all stations and ghcnds
    stations = Station.objects.all()
    data_types = ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN']

    # json lists
    dates_json = []

    # go thru dates and populate the json structure
    start_date = dte.date(2020, 5, 9)
    end_date = dte.date(2020, 5, 9)  # date + 1 to end on 16th

    for this_date in date_range(start_date, (end_date + dte.timedelta(1))):
        # get ghcnd info for specific day: 2020-05-16 and datatype=TMAX
        get_date = this_date

        st_json = []
        for s in stations:
            if s.us_state != 'Alaska':
                continue

            # create dictionary to load info to template view
            new_dict = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        s.longitude,
                        s.latitude
                    ]
                },
                'properties': {}
            }

            # generate dict based on all listed data types
            for d in data_types:
                try:
                    ghcnd = GHCND.objects.get(station__id=s.id, date=get_date, datatype=d)
                except Exception as e:
                    # print(s.id, 'no data found for', d)
                    new_dict['properties'][d] = None
                else:
                    new_dict['properties'][d] = ghcnd.value / 10

            # add dict to list
            st_json.append(new_dict)
            # print(st_json)

        dates_json.append({
            'key': get_date,
            'data': st_json
        })

    context = {
        'mapbox_access_token': os.environ.get('mapbox_access_token'),
        'stations': json.dumps(dates_json, cls=DjangoJSONEncoder),
        'start_date': dte.date.strftime(start_date, '%Y-%m-%d'),
        'end_date': dte.date.strftime(end_date, '%Y-%m-%d')
    }

    return render(request, 'pages/hexagon.html', context)
