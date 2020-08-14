#########################################################################
#                                                                       #
#   HexGrid Constructor (Python Version)                                #
#   This constructor script calculates and generates the hexgrid        #
#   temperature layer on top of the map.                                #
#   Due to performance and function duration, the original function     #
#   is divided into smaller parts. Easier to monitor and add logs.      #
#                                                                       #
#########################################################################
import turfpy as turf
import datetime as dte
import json


# get default hexgrid
def get_hexgrid(filename):

    with ('gsod/posts/blanks' + filename, 'r') as readfile:
        hexgrid = json.load(readfile)

    return hexgrid


# get the default hexgrid, compute the polygons and centroids
def hexgrid_constructor(bbox, cellSide, options, stations, levels):

    # set variables, declare hexGrid
    bbox = ','.join([str(b) for b in bbox]).replace(',', '_')
    filename = 'blank_HexGrid-' + bbox + 'r' + str(cellSide) + '.json'
    hexGrid = get_hexgrid(filename)
    polygons_set = []
    centroid_set = []
    # dataSet = data

    # loop through stations and assign it to the hexGrid
    start_time = dte.datetime.now()

    for hex in hexGrid.features:
        polygon = turf.polygon([hex.geometry.coordinates[0]])
        polygons_set.push(polygon)
        centroid = turf.centroid(polygon)
        centroid_set.push(centroid)

        # filter data first: TMAX, TMIN and Coordinates must exist!
        dataSet = dataSet.filter(d= > (d.properties.TMAX & & d.properties.TMIN & & d.geometry.coordinates[0]))

        # find the centroid that houses the weather station
        dataSet.forEach((d, i) = > {
            station = d.geometry.coordinates
            if (turf.booleanPointInPolygon(station, polygon)) {
            d.properties.centroid = centroid
            }
        })

        f.properties = {
        temperature: -1,
                     centroid: centroid
        }
    })

    # filter out those without a centroid
    dataSet = dataSet.filter(d= > (d.properties.TMAX & & d.properties.centroid))

    end_time = dte.datetime.now()
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

    return hexGrid
# '''
