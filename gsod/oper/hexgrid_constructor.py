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

'''
# get the default hexgrid, compute the polygons and centroids
def hexgrid_constructor(bbox, cellSide, options, data, levels, bot_lat, top_lat)

    # set variables, declare hexGrid
    hexGrid = get_hexgrid()
    tempChange = 0
    polygons_set = []
    centroid_set = []
    dataSet = data

    # loop through hexGrid to obtain polygons and centroids
    startTime = dte.datetime.now()

    for hex in hexGrid:
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

    endTime = dte.datetime.now()
    seconds = (endTime.getTime() - startTime.getTime()) / 1000
    print("Set Hexagon Tiles:", seconds, "seconds")
    print("Updated Data Length:", dataSet.length)

    # copy over hexGridDataSet for variable use
    # hexGridDataSet = hexGrid.features

    # add rings
    # hexGridDataSet = HexGridAddRings(centroid_set, cellSide, levels, hexGridDataSet, dataSet, bot_lat, top_lat)

    # find overlaps
    # hexGridDataSet = HexGridOverlaps(hexGridDataSet, levels)

    # re - calculate temps and deploy the rings, then stations
    # hexGrid = HexGridDeploy(hexGrid, levels, hexGridDataSet, dataSet)

    return hexGrid
'''
