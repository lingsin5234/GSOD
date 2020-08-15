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
def hexgrid_constructor(bbox, cellSide, stations, levels, mid_lat):

    # set variables, declare hexGrid
    bbox = ','.join([str(b) for b in bbox]).replace(',', '_')
    filename = 'blank_HexGrid' + bbox + 'r' + str(cellSide) + '.json'
    hexGrid = get_hexgrid(filename)
    centroids = []
    hexGridDict = {}
    tempDict = {}

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
        tempDict[centroid_id] = {"temperature": -1}
        centroids.append(Feature(geometry=Point(hex['centroid']['geometry']['coordinates'])))
    centroid_set = FeatureCollection(centroids)
    e1 = dte.datetime.now()

    # loop through stations and assign it to the hexGrid
    station_centroids = []
    print("Set Hexagon Tiles:", str((e1 - s1).total_seconds()), "seconds")
    s2 = dte.datetime.now()
    for station in stations:
        station_coord = Feature(geometry=Point(station['geometry']['coordinates']))
        # print(station_coord)
        closest_hex = find_closest_polygon(station_coord, centroid_set, cellSide)
        # print(closest_hex)

        # assign that hex the station
        coord = 'P' + ','.join([str(round(c, 6)) for c in closest_hex['geometry']['coordinates']])
        coord = coord.replace('P-', 'N').replace(',', '_').replace('-', 'n')
        # print(hexGridDict[coord])
        hexGridDict[coord]['station'] = station
        tempDict[coord]['temperature'] = station['properties']['TMAX']  # TMAX USED HERE #############!!!!!!
        station_centroids.append(Feature(geometry=Point(closest_hex['geometry']['coordinates'])))
    # print(hexGridDict)
    # stations_set = FeatureCollection(station_centroids)
    # print(stations_set)
    # print(len(stations_set['features']))

    e2 = dte.datetime.now()
    print("Assign Stations:", str((e2 - s2).total_seconds()), "seconds")

    # add rings
    s1 = dte.datetime.now()
    dist = math.sqrt(3) * cellSide
    for idx, hex in enumerate(hexGridDict):
        stations_set = FeatureCollection(station_centroids.copy())

        centroid_coord = hex.replace('N', '-').replace('P', '').replace('_', ',').replace('n', '-')
        centroid_coord = [float(c) for c in centroid_coord.split(',')]

        # get all the '0's and ignore the stations
        if '0' in hexGridDict[hex]['station']:
            # get closest stations in recursive function
            rings = get_closest_stations(centroid_coord, stations_set, tempDict,
                                         cellSide, 0, dist, mid_lat, 0, 1, levels)
            # print(len(stations_set['features']), idx)
            if not rings:
                # no results
                # print('No Results', rings)
                pass
            else:
                hexGridDict[hex]['rings'] = rings
                print('Rings', centroid_coord, hexGridDict[hex]['rings'])  # , stations_set)
    e1 = dte.datetime.now()
    print("Adding Rings:", str((e1 - s1).total_seconds()), "seconds")

    # find overlaps
    # hexGridDataSet = HexGridOverlaps(hexGridDataSet, levels)

    # re - calculate temps and deploy the rings, then stations
    heat_check = 0
    for idx, hex in enumerate(hexGridDict):
        if ('0' in hexGridDict[hex]['station']) and (len(hexGridDict[hex]['rings']) > 0):
            # hexGrid['features'][idx]['properties'] = hexGridDict[hex]['rings'][0]['properties'].copy()

            # accept only ring_level == 1 for now
            # if hexGridDict[hex]['rings'][0]['ring_level'] == 1:

            # take only the highest ring -- ignore overlap for now
            hexGrid['features'][idx]['properties'] = {
                'temperature': hexGridDict[hex]['rings'][0]['temperature']
            }
        elif not ('0' in hexGridDict[hex]['station']):
            # this is a weather station
            hexGrid['features'][idx]['properties'] = hexGridDict[hex]['station']['properties'].copy()
            hexGrid['features'][idx]['properties']['temperature'] = hexGrid['features'][idx]['properties']['TMAX']
        else:
            # this is not weather station and outside all rings
            if heat_check == 0:
                heat_check += 1
                print("Heat Check")
            hexGrid['features'][idx]['properties'] = {
                'temperature': -1
            }
    e2 = dte.datetime.now()
    print("Deploying Temperatures:", str((e2 - e1).total_seconds()), "seconds")

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


# adated from actual_nearest_point -- find the first polygon that it is in
def find_closest_polygon(target_point: Feature, points: FeatureCollection, min_dist) -> Feature:

    if not target_point:
        raise Exception("target_point is required")

    if not points:
        raise Exception("points is required")

    # min_dist = float("inf")
    best_feature_index = 0

    def _callback_feature_each(pt, feature_index):
        nonlocal min_dist, best_feature_index
        distance_to_point = turf.distance(target_point, pt)
        # print(distance_to_point)
        if float(distance_to_point) < min_dist:
            best_feature_index = feature_index
            min_dist = distance_to_point
            # print(min_dist)
            return False  # return False will break the loop once inside a polygon
        return True

    actual_feature_each(points, _callback_feature_each)

    nearest = points["features"][best_feature_index]
    nearest["properties"]["featureIndex"] = best_feature_index
    nearest["properties"]["distanceToPoint"] = min_dist
    return nearest


# adated from actual_nearest_point -- find the next closest ring polygon
def find_next_ring(target_point: Feature, points: FeatureCollection, min_dist, max_dist) -> Feature:

    if not target_point:
        raise Exception("target_point is required")

    if not points:
        raise Exception("points is required")

    # min_dist = float("inf")
    best_feature_index = 0

    def _callback_feature_each(pt, feature_index):
        nonlocal min_dist, best_feature_index
        distance_to_point = turf.distance(target_point, pt)
        # print(distance_to_point)
        if (float(distance_to_point) > min_dist) and (float(distance_to_point) <= max_dist):
            best_feature_index = feature_index
            min_dist = distance_to_point
            # print(min_dist)
            return False  # return False will break the loop once inside a polygon
        return True

    actual_feature_each(points, _callback_feature_each)

    nearest = points["features"][best_feature_index]
    nearest["properties"]["featureIndex"] = best_feature_index
    nearest["properties"]["distanceToPoint"] = min_dist
    return nearest


# Get Closest Weather Stations -- recursive
def get_closest_stations(coord, the_stations, tempDict, cellSide, min_dist, max_dist, mid_lat, loops, level, max_level):

    # work out the distances
    adj_max_dist = convert_distance(cellSide * math.sqrt(3) * level, coord[1], mid_lat)
    if level == 1:
        adj_min_dist = cellSide
    else:
        adj_min_dist = max_dist    # previous max is now the min

    # find next ring
    closest_station = find_next_ring(coord, the_stations, adj_min_dist, adj_max_dist)
    # closest_station = actual_nearest_point(coord, the_stations)

    # get feature index and distance
    feature_index = closest_station['properties']['featureIndex']
    distance = closest_station['properties']['distanceToPoint']
    new_stations = the_stations.copy()

    # get station coord to assign temperature
    station_coord = 'P' + ','.join([str(round(c, 6)) for c in closest_station['geometry']['coordinates']])
    station_coord = station_coord.replace('P-', 'N').replace(',', '_').replace('-', 'n')

    if (loops > 7) or (level > max_level):
        return False
    elif (float(round(distance, 6)) <= float(round(adj_max_dist, 6))) and \
            (float(round(distance, 6)) > float(round(adj_min_dist, 6))) and (len(new_stations['features']) > 1):
        # remove that from list
        new_stations['features'].pop(feature_index)

        # recursive call to get next closest station
        next_closest = get_closest_stations(coord, new_stations, tempDict, cellSide, min_dist,
                                            max_dist, mid_lat, loops+1, level, max_level)
        coord_dict = [{
            'ring_level': level,
            'temperature': (tempDict[station_coord]['temperature'] + 40 + (-1 * level)) / 80
        }]

        if not next_closest:
            pass
        else:
            coord_dict.extend(next_closest)
        return coord_dict
    elif loops <= 7:
        # else if loops less than 7 but not satisfy above -- increase the level
        next_closest = get_closest_stations(coord, new_stations, tempDict, cellSide, min_dist,
                                            max_dist, mid_lat, loops + 1, level + 1, max_level)
        # don't process coord_dict; just next_closest if not false
        if not next_closest:
            return False
        else:
            return next_closest
    else:
        return False


# convert the distance based on the latitude and reference latitude
def convert_distance(distance, lat, middle_lat):

    # find pixel distance of the distance at the middle latitude
    
    km_per_pixel = 40075 * math.cos(middle_lat * math.pi / 180) / math.pow(2, 12)
    pixel_distance = distance / km_per_pixel

    # now use pixel distance to convert it to the distance at the needed latitude
    km_per_pixel = 40075 * math.cos(lat * math.pi / 180) / math.pow(2, 12)
    return pixel_distance * km_per_pixel
