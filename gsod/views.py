from django.shortcuts import render
from djangoapps.utils import get_this_template
from .models import Station


# homepage
def homepage(request):

    return render(request, 'pages/gsod_home.html')


# project page
def project_markdown(request):

    page_height = 1050
    f = open('baseball/README.md', 'r')
    if f.mode == 'r':
        readme = f.read()
        page_height = len(readme)/2 + 200

    content = {
        'readme': readme,
        'page_height': page_height
    }

    template_page = get_this_template('baseball', 'project.html')

    return render(request, template_page, content)


# stations list
def list_stations(request):

    stations = Station.objects.all()

    context = {
        'stations': stations
    }

    return render(request, 'pages/stations.html', context)
