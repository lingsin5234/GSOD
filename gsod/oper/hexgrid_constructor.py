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
import json, math


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
            'station': {'0': 0},
            'rings': [],
        }
        centroids.append(Feature(geometry=Point(hex['centroid']['geometry']['coordinates'])))
    centroid_set = FeatureCollection(centroids)

    # loop through stations and assign it to the hexGrid
    station_centroids = []
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
        station_centroids.append(Feature(geometry=Point(closest_hex['geometry']['coordinates'])))
    # print(hexGridDict)
    # stations_set = FeatureCollection(station_centroids)
    # print(stations_set)
    # print(len(stations_set['features']))

    e2 = dte.datetime.now()
    print("Set Hexagon Tiles:", str((s2 - s1).total_seconds()), "seconds")
    print("Assign Stations:", str((e2 - s2).total_seconds()), "seconds")

    # add rings
    s1 = dte.datetime.now()
    max_dist = levels * math.sqrt(3) * cellSide
    print(max_dist)
    for idx, hex in enumerate(hexGridDict):
        stations_set = FeatureCollection(station_centroids.copy())

        centroid_coord = hex.replace('N', '-').replace('P', '').replace('_', ',').replace('n', '-')
        centroid_coord = [float(c) for c in centroid_coord.split(',')]

        # get all the '0's and ignore the stations
        if '0' in hexGridDict[hex]['station']:
            # get closest stations in recursive function
            rings = get_closest_stations(centroid_coord, stations_set, max_dist)
            # print(len(stations_set['features']), idx)
            if not rings:
                # no results
                # print('No Results', rings)
                pass
            else:
                hexGridDict[hex]['rings'] = rings
                print('Rings', centroid_coord, hexGridDict[hex]['rings'])  # , stations_set)
    e1 = dte.datetime.now()

    # find overlaps
    # hexGridDataSet = HexGridOverlaps(hexGridDataSet, levels)

    # re - calculate temps and deploy the rings, then stations
    for idx, hex in enumerate(hexGridDict):
        if ('0' in hexGridDict[hex]['station']) and (len(hexGridDict[hex]['rings']) > 0):
            # hexGrid['features'][idx]['properties'] = hexGridDict[hex]['rings'][0]['properties'].copy()
            hexGrid['features'][idx]['properties'] = {
                'temperature': -1
            }
        elif not ('0' in hexGridDict[hex]['station']):
            hexGrid['features'][idx]['properties'] = hexGridDict[hex]['station']['properties'].copy()
        else:
            hexGrid['features'][idx]['properties'] = {
                'temperature': -1
            }

    return hexGrid


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


# Get Closest Weather Stations -- recursive
def get_closest_stations(coord, the_stations, max_dist):

    closest_station = actual_nearest_point(coord, the_stations)
    feature_index = closest_station['properties']['featureIndex']
    distance = closest_station['properties']['distanceToPoint']
    new_stations = the_stations.copy()
    # print(feature_index, distance, max_dist)

    if (float(round(distance, 6)) < float(round(max_dist, 6))) and (len(new_stations['features']) > 1):
        # remove that from list
        new_stations['features'].pop(feature_index)

        # recursive call to get next closest station
        next_closest = get_closest_stations(coord, new_stations, max_dist)
        coord_dict = [{
            'ring_level': 1
        }]

        if not next_closest:
            pass
        else:
            coord_dict.extend(next_closest)
        return coord_dict
    else:
        return False
