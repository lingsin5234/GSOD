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
function HexGridConstructor(bbox, cellSide, options, data, levels, bot_lat, top_lat) {

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
    //console.log(hexGridDataSet.length, centroid_set.length); // SAME LENGTH

    // add rings
    hexGridDataSet = HexGridAddRings(centroid_set, cellSide, levels, hexGridDataSet, dataSet, bot_lat, top_lat);

    // find overlaps
    //rings = HexGridOverlaps(rings);
    //hexGridDataSet = HexGridOverlaps(hexGridDataSet, levels);

    // re-calculate temps; deploy rings then stations
    //hexGrid = HexGridDeploy(hexGrid, levels, hexGridDataSet, dataSet);

    return hexGrid;
}


// this function adds rings around each weather station
function HexGridAddRings(centroid_set, cellSide, levels, hexGridDataSet, dataSet, bot_lat, top_lat) {

    // loop thru the each station again to create the "ring" around it, for the amount of specified levels
    startTime = new Date();
    dataSet.forEach((d, i) => {
        station = d.properties.centroid;
        station_temp = d.properties['TMAX'];

        for (var cent in centroid_set) {
            coord = centroid_set[cent];
            hexGridDataSet[cent].properties.rings = [];

            // run the station_rings "level" # of times
            for (var x=0; x < levels; x++) {

                if (station_rings(cellSide, x+1, station, coord, bot_lat, top_lat)[0]) {
                    // add ring properties to the station (dataSet) information
                    ring_prop = {
                        "ring_level": x+1,
                        "station": station,
                        "coordinates": coord.geometry.coordinates,
                        "temperature": station_temp - (x * 1)
                    }
                    hexGridDataSet[cent].properties.rings.push(ring_prop);
                }
            }
            //console.log(hexGridDataSet[cent]);
        }
        //console.log("GHCND Index #", i, "completed.")
    });

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Adding Rings:", seconds, "seconds");

    console.log("HexGridDataSet:", hexGridDataSet);

    return hexGridDataSet;
}


// find overlaps on same ring level and one below
function HexGridOverlaps(hexGridDataSet, levels) { // rings) {

    // loop thru each level and run it thru the ring overlap
    levelsArray = [...Array(levels).keys()];
    //console.log(levelsArray);

    startTime = new Date();
    levelsArray.forEach(l => {
        hexGridDataSet = ring_overlap(hexGridDataSet, l+1);
        console.log("Same Level Ring", l+1, "checked");
    });

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Check Same Level Overlap:", seconds, "seconds");

    // loop thru rings to work on below 1 overlap
    startTime = new Date();
    weights = [0.7];

    levelsArray.forEach(l => {
       hexGridDataSet = ring_overlap_below(hexGridDataSet, l+1, weights)
       console.log("One Level Below Ring", l+1, "checked");
    });

    endTime = new Date();
    seconds = (endTime.getTime() - startTime.getTime()) / 1000;
    console.log("Check 1 Level Overlap:", seconds, "seconds");

    console.log("hexGridDataSet", hexGridDataSet);

    return hexGridDataSet;
}


// re-calculate temps for each ring, and ovewrite with stations at the end
function HexGridDeploy(hexGrid, levels, hexGridDataSet, dataSet) {

    // re-calculate the temperatures based on ring; overwrite any ring-hexes that are stations
    startTime = new Date();
    hexGrid.features.forEach((f, i) => {

        polygon = turf.polygon([f.geometry.coordinates[0]]);
        centroid = turf.centroid(polygon);

        // copy all the rings in
        coord = hexGridDataSet[i].properties.centroid.geometry.coordinates
        if (turf.booleanPointInPolygon(coord, polygon)) {

            // find the highest level ring
            //console.log(("rings" in hexGridDataSet[i].properties));
            if ("rings" in hexGridDataSet[i].properties) {
                found = false
                l = levels
                while (!found) {
                    hexGridDataSet[i].properties.rings.forEach(r => {
                        if (r.ring_level == l+1) {
                            get_temp = r.temperature;
                            found = true
                            //console.log(get_temp, l+1);
                        }
                    });
                    l--;
                    if (l <= 0) {
                        found = true
                        get_temp = -120  // to get -1 for temperature
                    }
                }

                f.properties = {
                    temperature: (get_temp + 40)/80,
                    centroid: centroid
                };
                //console.log(get_temp);

            } else {
                /*
                //don't change the temperature
                f.properties = {
                    temperature: (hexGridDataSet[i].properties.temperature + 40)/80,
                    centroid: centroid
                };
                */
            }
        }

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
