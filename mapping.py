# mapping functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from django.db.models import Max, Min
import urllib, base64, io


# set up a basic map plotting all the stations in Edmonton
# this one uses MATPLOTLIB -- so far it'll be a static image
def basic_map(stations):

    # find lat long min max
    long_min = stations.aggregate(Min('longitude'))['longitude__min']
    long_max = stations.aggregate(Max('longitude'))['longitude__max']
    lat_min = stations.aggregate(Min('latitude'))['latitude__min']
    lat_max = stations.aggregate(Max('latitude'))['latitude__max']

    # create the bounding box
    bbox = (long_min, long_max, lat_min, lat_max)
    print(bbox)

    # find out which coordinates are too big
    # for s in stations:
    #     print(s.name, s.longitude, s.latitude)
    edm_map = plt.imread('static/img/edmonton-map.png')

    # set up the axis for the bounding box and image
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_title('Plotting Stations in Edmonton')
    ax.set_xlim(bbox[0], bbox[1])
    ax.set_ylim(bbox[2], bbox[3])
    ax.imshow(edm_map, zorder=0, extent=bbox, aspect='equal')

    # loop thru and plot the stations
    for s in stations:
        # alpha changes the opacity; c is the colour; s is size. unclear if its pixels
        ax.scatter(s.longitude, s.latitude, zorder=1, alpha=0.8, c='b', s=5)

    # convert graph into string buffer 64-bit code
    buf = io.BytesIO()
    print(fig)
    print(ax)
    fig.savefig(buf, format='png')
    buf.seek(0)  # move cursor to start
    buf_string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(buf_string)

    return uri
