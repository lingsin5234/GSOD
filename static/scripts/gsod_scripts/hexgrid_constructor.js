/*
*
*   HexGrid Constructor
*   This constructor script calculates and generates the hexgrid
*   temperature layer on top of the map.
*
*/

function HexGridConstructor(bbox, cellSide, options, data, levels) {

    // set variables, declare hexGrid
    var hexGrid = turf.hexGrid(bbox, cellSide, options);
    var tempChange = 0;
    var polygons_set = [];
    var centroid_set = [];

    // loop through hexGrid to obtain polygons and centroids
    hexGrid.features.forEach(f => {

        polygon = turf.polygon([f.geometry.coordinates[0]]);
        polygons_set.push(polygon);
        centroid = turf.centroid(polygon);
        centroid_set.push(centroid);

        // filter data first
        data = data.filter(d => (d.properties.TMAX && d.properties.TMIN));

        // find the centroid that houses the weather station
        data.forEach((d, i) => {
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

    // loop thru the polygons again to get the "ring" around it, for the amount of specified levels
    rings = [];
    for (var x=0; x < levels; x++) {
        rings[x] = [];
    }
    data.forEach((d, i) => {
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
    });

    // loop thru rings to check overlap along same ring
    rings.forEach(r => {
        ring_bool = ring_overlap(r);
        if (ring_bool) {
            r = ring_bool;
        }
    });

    // loop thru rings to work on below 1 overlap
    weights = [0.7];
    for (var r=0; r < rings.length - 1; r++) {
        [ring_bool1, ring_bool2] = ring_overlap_below(rings[r], ring[r+1], weights)
        if (ring_bool1) {
            rings[r] = ring_bool1;
        }
        if (ring_bool2) {
            rings[r+1] = ring_bool2;
        }
    }

    hexGrid.features.forEach(f => {

        polygon = turf.polygon([f.geometry.coordinates[0]]);
        centroid = turf.centroid(polygon);

        // insert colours from each ring, starting with outermost first
        for (var ring=levels-1; ring >= 0; ring--) {
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
        }

        // insert the colours from the weather stations
        data.forEach(d => {
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

    return hexGrid;
}
