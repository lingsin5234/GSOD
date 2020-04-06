from django.shortcuts import render
from djangoapps.utils import get_this_template
from .models import Station, GHCND
from .functions import test_run, test_yeg
from .mapping import basic_map, basic_data_map
from .forms import StationDatesForm
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

    x = test_run()

    stations = Station.objects.all()
    print(x)

    context = {
        'stations': stations
    }

    return render(request, 'pages/stations.html', context)


# this is test map using Edmonton
def map_test(request):

    # get stations from Edmonton
    station_objs = Station.objects.filter(name__contains='Edmonton')
    station_objs = station_objs.exclude(name__contains='Stony Plain')
    x = test_yeg(station_objs, '2020-03-31', '2020-04-05')
    # the_map = basic_map(stations)

    # now get station data that was just saved
    # stacking filters filter(A,B) == A && B; filter(A).filter(B) == A || B
    # note that when referencing the foreign key model -- IT MUST BE lowercase!
    station_data = GHCND.objects.filter(date__gte='2020-03-31', date__lte='2020-04-05')\
        .values('station__longitude', 'station__latitude', 'date', 'datatype', 'attributes', 'value')
    the_map = basic_data_map(station_data)

    context = {
        'map': the_map
    }

    return render(request, 'pages/map.html', context)
