#########################################################################
#                                                                       #
#   HexGrid Constructor (Python Version)                                #
#   This constructor script calculates and generates the hexgrid        #
#   temperature layer on top of the map.                                #
#   Due to performance and function duration, the original function     #
#   is divided into smaller parts. Easier to monitor and add logs.      #
#                                                                       #
#########################################################################
import turfpy.measurement as turf
from turfpy.transformation import union
from geojson import Feature, Polygon, FeatureCollection
import datetime as dte
import json


# get default hexgrid
def get_hexgrid(filename):

    filepath = 'gsod/posts/blanks/' + filename
    with open(filepath, 'r') as readfile:
        hexgrid = json.load(readfile)

    return hexgrid


# get the default hexgrid, compute the polygons and centroids
def hexgrid_constructor(bbox, cellSide, stations, levels):

    # set variables, declare hexGrid
    bbox = ','.join([str(b) for b in bbox]).replace(',', '_')
    filename = 'blank_HexGrid' + bbox + 'r' + str(cellSide) + '.json'
    hexGrid = get_hexgrid(filename)
    centroids = []
    hexGridDict = dict()

    # loop thru hexgrid to get centroids
    s1 = dte.datetime.now()
    for hex in hexGrid['features']:
        centroid_id = ','.join([str(c) for c in hex['centroid']['geometry']['coordinates']]),
        hexGridDict[centroid_id] = dict()
        centroids.append(hex['centroid'])
    centroid_set = union(FeatureCollection(centroids))

    # loop through stations and assign it to the hexGrid
    s2 = dte.datetime.now()
    for station in stations:

        closest_hex = turf.nearest_point(station, centroid_set)

        # assign that hex the station
        coord = ','.join([str(c) for c in closest_hex])
        hexGridDict[coord]['station'] = station
    print(hexGridDict)

    e2 = dte.datetime.now()
    # seconds = (endTime.getTime() - startTime.getTime()) / 1000
    # print("Set Hexagon Tiles:", seconds, "seconds")
    # print("Updated Data Length:", dataSet.length)

    # copy over hexGridDataSet for variable use
    # hexGridDataSet = hexGrid.features

    # add rings
    # hexGridDataSet = HexGridAddRings(centroid_set, cellSide, levels, hexGridDataSet, dataSet, bot_lat, top_lat)

    # find overlaps
    # hexGridDataSet = HexGridOverlaps(hexGridDataSet, levels)

    # re - calculate temps and deploy the rings, then stations
    # hexGrid = HexGridDeploy(hexGrid, levels, hexGridDataSet, dataSet)

    return True
# '''
