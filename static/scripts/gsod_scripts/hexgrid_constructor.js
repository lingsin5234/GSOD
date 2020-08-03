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

    // add rings
    rings = HexGridAddRings(hexGrid, polygon_set, centroid_set, cellSide, levels, dataSet);

    // find overlaps
    rings = HexGridOverlaps(rings);

    // re-calculate temps; deploy rings then stations
    hexGrid = HexGridDeploy(hexGrid, rings, dataSet);

    return hexGrid;
}


// this function adds rings around each weather station
function HexGridAddRings(hexGrid, polygon_set, centroid_set, cellSide, levels, dataSet) {

    // loop thru the polygons again to get the "ring" around it, for the amount of specified levels
    startTime = new Date();
    rings = [];
    for (var x=0; x < levels; x++) {
        rings[x] = [];
    }
    dataSet.forEach((d, i) => {
        station = d.properties.centroid;
        station_temp = d.properties['TMAX'];

        for (var cent in centroid_set) {
            coord = centroid_set[cent];

            // run the station_rings "level" # of times
            for (var x=0; x < levels; x++) {

                if (station_rings(cellSide, x+1, station, coord, bot_lat, top_lat)[0]) {
                    ring = {"geometry": {"coordinates": coord.geometry.coordinates},
                            "properties": {"temperature": station_temp - (x * 1)}}
                    rings[x].push(ring);
                }
            }
        }
        console.log("GHCND Index #", i, "completed.")
    });

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Adding Rings:", seconds, "seconds");

    return rings;
}


// find overlaps on same ring level and one below
function HexGridOverlaps(rings) {

    // loop thru rings to check overlap along same ring
    startTime = new Date();
    rings.forEach((r, i) => {
        ring_bool = ring_overlap(r);
        if (ring_bool) {
            r = ring_bool;
        }
        console.log("Same Level Ring", i, "checked")
    });

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Check Same Level Overlap:", seconds, "seconds");

    // loop thru rings to work on below 1 overlap
    startTime = new Date();
    weights = [0.7];
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
}


// re-calculate temps for each ring, and ovewrite with stations at the end
function HexGridDeploy(hexGrid, rings, dataSet) {

    // re-calculate the temperatures based on ring; overwrite any ring-hexes that are stations
    startTime = new Date();
    hexGrid.features.forEach(f => {

        polygon = turf.polygon([f.geometry.coordinates[0]]);
        centroid = turf.centroid(polygon);

        // insert colours from each ring, starting with outermost first
        for (var ring=levels-1; ring >= 0; ring--) {
            time1 = new Date();
            rings[ring].forEach(r => {
                coord = r.geometry.coordinates
                if (turf.booleanPointInPolygon(coord, polygon)) {
                    //console.log(coord, f);
                    f.properties = {
                        temperature: (r.properties.temperature + 40)/80,
                        centroid: centroid
                    };
                }
            });
            time2 = new Date();
            seconds = (time1.getTime() - time2.getTime()) / 1000;
            console.log("Ring", ring, "complete:", seconds, "seconds")
        }

        // insert the colours from the weather stations
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

    return hexGrid;
}
