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
from geojson import Feature, Polygon, FeatureCollection, Point
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
    hexGridDict = {}

    # loop thru hexgrid to get centroids
    s1 = dte.datetime.now()
    for hex in hexGrid['features']:
        centroid_id = 'P' + ','.join([str(round(c, 6)) for c in hex['centroid']['geometry']['coordinates']])
        centroid_id = centroid_id.replace('P-', 'N').replace(',', '_').replace('-', 'n')
        # print(centroid_id)
        hexGridDict[centroid_id] = {
            'station': {},
            'rings': {}
        }
        centroids.append(Feature(geometry=Point(hex['centroid']['geometry']['coordinates'])))
    centroid_set = FeatureCollection(centroids)

    # loop through stations and assign it to the hexGrid
    s2 = dte.datetime.now()
    for station in stations:
        station_coord = Feature(geometry=Point(station['geometry']['coordinates']))
        # print(station_coord)
        closest_hex = actual_nearest_point(station_coord, centroid_set)
        # print(closest_hex)

        # assign that hex the station
        coord = 'P' + ','.join([str(round(c, 6)) for c in closest_hex['geometry']['coordinates']])
        coord = coord.replace('P-', 'N').replace(',', '_').replace('-', 'n')
        # print(hexGridDict[coord])
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


# ACTUAL nearest point -- edited the source code from turfpy library
def actual_nearest_point(target_point: Feature, points: FeatureCollection) -> Feature:

    if not target_point:
        raise Exception("target_point is required")

    if not points:
        raise Exception("points is required")

    min_dist = float("inf")
    best_feature_index = 0

    def _callback_feature_each(pt, feature_index):
        nonlocal min_dist, best_feature_index
        distance_to_point = turf.distance(target_point, pt)
        # print(distance_to_point)
        if float(distance_to_point) < min_dist:
            best_feature_index = feature_index
            min_dist = distance_to_point
            # print(min_dist)
        return True

    actual_feature_each(points, _callback_feature_each)

    nearest = points["features"][best_feature_index]
    nearest["properties"]["featureIndex"] = best_feature_index
    nearest["properties"]["distanceToPoint"] = min_dist
    return nearest


# ACTUAL feature each loop -- edited the source code from turfpy library
def actual_feature_each(geojson, callback):
    if geojson["type"] == "Feature":
        callback(geojson, 0)
    elif geojson["type"] == "FeatureCollection":
        for i in range(0, len(geojson["features"])):
            # print(callback(geojson["features"][i], i))
            if not callback(geojson["features"][i], i):
                break
