/*
*
*   HexGrid Constructor
*   This constructor script calculates and generates the hexgrid
*   temperature layer on top of the map.
*   Due to performance and function duration, the original function
*   is divided into smaller parts. Easier to monitor and add logs.
*
*/

// create the HexGrid, compute the polygons and centroids
function HexGridConstructor(bbox, cellSide, options, data, levels) {

    // set variables, declare hexGrid
    var hexGrid = turf.hexGrid(bbox, cellSide, options);
    var tempChange = 0;
    var polygons_set = [];
    var centroid_set = [];
    var dataSet = data;

    // loop through hexGrid to obtain polygons and centroids
    startTime = new Date();
    hexGrid.features.forEach(f => {

        polygon = turf.polygon([f.geometry.coordinates[0]]);
        polygons_set.push(polygon);
        centroid = turf.centroid(polygon);
        centroid_set.push(centroid);

        // filter data first; TMAX, TMIN and Coordinates must exist!
        dataSet = dataSet.filter(d => (d.properties.TMAX && d.properties.TMIN && d.geometry.coordinates[0]));

        // find the centroid that houses the weather station
        dataSet.forEach((d, i) => {
            station = d.geometry.coordinates;
            if (turf.booleanPointInPolygon(station, polygon)) {
                d.properties.centroid = centroid;
            }
        });

        f.properties = {
            temperature: -1,
            centroid: centroid
        };
        //tempChange += 0.000001;
    });

    // filter out those without a centroid
    dataSet = dataSet.filter(d => (d.properties.TMAX && d.properties.centroid));

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Set Hexagon Tiles:", seconds, "seconds");
    console.log("Updated Data Length:", dataSet.length);

    // copy over hexGridDataSet for variable use
    hexGridDataSet = hexGrid.features;

    // add rings
    hexGridDataSet = HexGridAddRings(centroid_set, cellSide, levels, hexGridDataSet);

    // find overlaps
    //rings = HexGridOverlaps(rings);
    dataSet = HexGridOverlaps(dataSet, levels);

    // re-calculate temps; deploy rings then stations
    hexGrid = HexGridDeploy(hexGrid, levels, dataSet);

    return hexGrid;
}


// this function adds rings around each weather station
function HexGridAddRings(centroid_set, cellSide, levels, hexGridDataSet) {

    // loop thru the polygons again to get the "ring" around it, for the amount of specified levels
    startTime = new Date();
    hexGridDataSet.forEach((d, i) => {
        station = d.properties.centroid;
        station_temp = d.properties['TMAX'];
        d.properties.rings = [];

        for (var cent in centroid_set) {
            coord = centroid_set[cent];

            // run the station_rings "level" # of times
            for (var x=0; x < levels; x++) {

                if (station_rings(cellSide, x+1, station, coord, bot_lat, top_lat)[0]) {
                    /*ring = {"geometry": {"coordinates": coord.geometry.coordinates},
                            "properties": {"temperature": station_temp - (x * 1)}}
                    rings[x].push(ring);*/

                    // add ring properties to the station (dataSet) information
                    ring_prop = {
                        "ring_level": x+1,
                        "station": station,
                        "coordinates": coord.geometry.coordinates,
                        "temperature": station_temp - (x * 1)
                    }
                    d.properties.rings.push(ring_prop);
                }
            }
        }
        //console.log("GHCND Index #", i, "completed.")
    });

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Adding Rings:", seconds, "seconds");

    return dataSet;
}


// find overlaps on same ring level and one below
function HexGridOverlaps(dataSet, levels) { // rings) {

    // loop thru each level and run it thru the ring overlap
    levelsArray = [...Array(levels).keys()];
    //console.log(levelsArray);

    startTime = new Date();
    levelsArray.forEach(l => {
        dataSet = ring_overlap(dataSet, l+1);
        console.log("Same Level Ring", l+1, "checked");
    });

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Check Same Level Overlap:", seconds, "seconds");

    // loop thru rings to work on below 1 overlap
    startTime = new Date();
    weights = [0.7];

    levelsArray.forEach(l => {
       dataSet = ring_overlap_below(dataSet, l+1, weights)
       console.log("One Level Below Ring", l+1, "checked");
    });

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Check 1 Level Overlap:", seconds, "seconds");

    console.log("dataSet", dataSet);

    return dataSet;

    /*
    for (var r=0; r < rings.length - 1; r++) {
        [ring_bool1, ring_bool2] = ring_overlap_below(rings[r], ring[r+1], weights)
        if (ring_bool1) {
            rings[r] = ring_bool1;
        }
        if (ring_bool2) {
            rings[r+1] = ring_bool2;
        }
        console.log("ONE Level Ring", r, "checked")
    }

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Check 1 Level Overlap:", seconds, "seconds");

    return rings;
    */
}


// re-calculate temps for each ring, and ovewrite with stations at the end
function HexGridDeploy(hexGrid, levels, dataSet) {

    // re-calculate the temperatures based on ring; overwrite any ring-hexes that are stations
    startTime = new Date();
    hexGrid.features.forEach(f => {

        polygon = turf.polygon([f.geometry.coordinates[0]]);
        centroid = turf.centroid(polygon);

        // copy all the rings in
        dataSet.forEach(d => {
            coord = d.geometry.coordinates
            if (turf.booleanPointInPolygon(coord, polygon)) {

                // find the highest level ring
                if ("rings" in d.properties) {
                    found = false
                    l = levels
                    while (!found) {
                        d.properties.rings.forEach(r => {
                            if (r.ring_level == l+1) {
                                get_temp = r.temperature;
                                found = true
                            }
                        });
                        l--;
                    }

                    f.properties = {
                        temperature: (get_temp + 40)/80,
                        centroid: centroid
                    };
                    console.log(get_temp);

                } else {
                    f.properties = {
                        temperature: (d.properties.temperature + 40)/80,
                        centroid: centroid
                    };
                }
            }
        })

        // insert the temperatures from the weather stations (overwriting some of previous)
        dataSet.forEach(d => {
            coord = d.geometry.coordinates
            if (turf.booleanPointInPolygon(coord, polygon)) {
                //console.log(coord);
                f.properties = {
                    temperature: (d.properties['TMAX'] + 40)/80,
                    centroid: centroid
                };
            }
        });
    });

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Re-calculating the temperatures:", seconds, "seconds");

    console.log("HexGrid", hexGrid);

    return hexGrid;
}
