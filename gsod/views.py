from django.shortcuts import render
from djangoapps.utils import get_this_template
import os
import json
from .models import Station, GHCND
from django.core.serializers.json import DjangoJSONEncoder
from .functions import test_run, test_yeg, run_add_stations
from .mapping import basic_map, basic_data_map
# from .forms import StationDatesForm -- defunct
# from django.db.models import Max, Min
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


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

    # get all stations
    stations = Station.objects.all()

    # stations json
    st_json = []
    for s in stations:
        new_dict = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    s.longitude,
                    s.latitude
                ]
            },
            'properties': {
                'title': '',  # s.name
                # 'icon': 'communications-tower'
                'icon': 'airport'
            }
        }
        st_json.append(new_dict)
    # print(st_json)

    context = {
        'mapbox_access_token': os.environ.get('mapbox_access_token'),
        'stations': json.dumps(st_json, cls=DjangoJSONEncoder)
    }

    return render(request, 'pages/map.html', context)


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
