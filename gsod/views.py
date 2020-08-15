from django.shortcuts import render
from djangoapps.utils import get_this_template
import os
import json
import re
from .models import Station, GHCND
# from django.core.serializers.json import DjangoJSONEncoder
# from .functions import test_run, test_yeg, run_add_stations, date_range
# from .mapping import basic_map, basic_data_map
# from .forms import StationDatesForm -- defunct
# from django.db.models import Max, Min
# from django.http import HttpResponse
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from .oper import hexgrid_constructor as hc
from gsod.serializers import GHCND_Serializer
import datetime as dte

'''
API Section
'''
from rest_framework import views, permissions
from rest_framework.response import Response
from .serializers import WeatherStations


# API View for ALL Weather Stations
class WeatherStationsAPI(views.APIView):

    # get request
    def get(self, request):

        print("GET REQUEST RECEIVED", request.GET)

        # get ALL Weather Stations
        stations = Station.objects.all()
        data_types = ['TMAX', 'TMIN']  # ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN']

        # json lists
        data_json = []

        # get ghcnd info for specific day: 2020-05-16 and datatype=TMAX
        get_date = request.GET['dataDate']
        # get_date = '2020-01-01'

        st_json = []
        idx = 0
        for s in stations:
            if s.us_state == 'Alaska' or s.us_state == 'Hawaii':
                continue
            # if s.us_state != 'Alaska':  # only get alaska
            #     continue

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
                    continue
                    # new_dict['properties'][d] = None
                else:
                    new_dict['properties'][d] = ghcnd.value / 10

                    # add dict to list
                    st_json.append(new_dict)
                    # print(st_json)

            if len(st_json) > 0:
                data_json.append({
                    'key': get_date,
                    'data': st_json
                })
            # idx += 1
            # if idx > 300:
            #     break
        # print(request.GET['dataDate'], len(data_json))
        log_file = 'gsod/seleniumLog/' + str(dte.datetime.now().date()) + '.log'
        with open(log_file, 'w') as outfile:
            try:
                outfile.write('GET REQUEST: dataDate - ' + str(request.GET['dataDate']) + '\n')
            except Exception as e:
                outfile.write('dataDate ERROR:' + str(e) + '\n')

        return Response(data_json)


# API View for ALL Weather Stations
class HexGridAPI(views.APIView):

    # get request
    def get(self, request):

        # print(request.GET)

        # get the JSON file
        data = []
        filename = 'hexGrid_' + request.GET['dataDate'] + '.json'
        # print(filename)
        try:
            with open('gsod/posts/' + filename) as file:
                data = json.load(file)
                # print(data)
        except Exception as e:
            print('GET json file: Failed', e)
        else:
            print('GET json file: Success!')

        return Response(data)

    # post request
    def post(self, request):
        print(request)
        print(request.data)
        log_file = 'gsod/seleniumLog/' + str(dte.datetime.now().date()) + '.log'
        with open(log_file, 'a') as outfile:
            try:
                outfile.write('request Headers:' + str(request.headers) + '\n')
            except Exception as e:
                outfile.write('request ERROR:' + str(e) + '\n')
            try:
                outfile.write('request.POST' + '\n' + str(request.POST) + '\n')
            except Exception as e:
                outfile.write('request.POST ERROR:' + str(e) + '\n')
            '''
            try:
                outfile.write('dataDate' + '\n' + str(request.data['dataDate']) + '\n')
            except Exception as e:
                outfile.write('dataDate ERROR:' + str(e) + '\n')
            try:
                outfile.write('request.data' + '\n' + str(request.data) + '\n')
            except Exception as e:
                outfile.write('request.data ERROR:' + str(e) + '\n')
            '''
        # write the JSON to file:
        filename = 'hexGrid_' + request.data['dataDate'] + '.json'
        try:
            with open('gsod/posts/' + filename, 'w') as outfile:
                json.dump(json.loads(request.POST['data']), outfile, indent=4)
                # json.dump(request.data['data'], outfile, indent=4)
        except Exception as e:
            print('POST write to file: Failed', e)
            with open(log_file, 'a') as outfile:
                outfile.write('POST write to file: Failed' + str(e) + '\n')
            status = False
        else:
            print('POST write to file: Success!')
            with open(log_file, 'a') as outfile:
                outfile.write('POST write to file: Success!' + '\n')
            status = True

        return Response(status)


# saving the blank hexgrid generated
class BlankHexGridAPI(views.APIView):

    # post request
    def post(self, request):

        # print(str(request.POST)[:150])
        # write the JSON to file:
        bbox = request.POST['bbox']  # this is not a list anymore, just a string
        bbox = bbox.replace('[', '').replace(']', '').replace(',', '_')
        cellSide = request.POST['cellSide']
        filename = 'blank_HexGrid' + bbox + 'r' + str(cellSide) + '.json'
        # print(filename)
        try:
            with open('gsod/posts/blanks/' + filename, 'w') as outfile:
                json.dump(json.loads(request.POST['hexGrid']), outfile, indent=4)
                # json.dump(request.data['data'], outfile, indent=4)
        except Exception as e:
            print('POST write to file: Failed', e)
            status = False
        else:
            print('POST write to file: Success!')
            status = True

        return Response(status)




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
    # run_add_stations()

    stations = Station.objects.all()

    context = {
        'stations': stations
    }

    return render(request, 'pages/stations.html', context)


# quick table view of specific station data
def station_data_table(request, station_id):

    data = GHCND.objects.filter(station=station_id).values()
    header = ['station_id', 'date', 'datatype', 'attribute', 'value']
    data_list = GHCND_Serializer(data, many=True).data
    json_list = json.loads(json.dumps(data_list))
    body = [list(jl.values()) for jl in json_list]
    print(body)
    print(header)

    context = {
        'header': header,
        'body': body
    }

    return render(request, 'pages/quickTable.html', context)


def new_map(request):

    # grab start and end date based on the gsod/posts folder
    files = [f for f in os.listdir('gsod/posts') if bool(re.search('json', f))]
    start_date = files[0].replace('hexGrid_', '').replace('.json', '')
    end_date = files[len(files)-1].replace('hexGrid_', '').replace('.json', '')
    # print(start_date, end_date)

    context = {
        'mapbox_access_token': os.environ.get('mapbox_access_token'),
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'pages/new_map.html', context)


# this view is for performing the GET, calculate and POST for the HexGrid data, based on the date passed
def calculate_hexGrid(request, date_of_data):

    context = {
        'date_of_data': date_of_data
    }

    return render(request, 'pages/calculate_hexGrid.html', context)


# testing out the gradient legend
def gradientLegend(request):

    return render(request, 'pages/gradientLegend.html')


# make a blank hexgrid
def make_blank_hexgrid(request):

    bbox = [-126, 24, -66.5, 50]  # USA
    cellSide = 15

    context = {
        'bbox': bbox,
        'cellSide': cellSide
    }

    return render(request, 'pages/blank_hexgrid.html', context)


# test new hexgrid constructor function
def calculate_hexGrid2(request):

    bbox = [-126, 24, -66.5, 50]  # USA
    cellSide = 15

    stations = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-96.726937845145, 33.733555]
            },
            "properties": {
                "TMAX": 21,
                "TMIN": 11
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-123.726937845145, 43.733940496411925]
            },
            "properties": {
                "TMAX": -20,
                "TMIN": -31
            }
        },
    ]

    hexGrid = hc.hexgrid_constructor(bbox, cellSide, stations, 8, (24 + 50)/2)

    context = {
        'mapbox_access_token': os.environ.get('mapbox_access_token'),
        'hexGrid': hexGrid
    }

    return render(request, 'pages/run_hexGrid2.html', context)
