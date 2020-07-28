/*
*   This file is to generate the hexagon grid
*   for vector tile mapping
*/

// generate a single hexagon
function single_hexagon(radius, long, lat) {

    // 60 degrees all around, so all are equilateral triangles
    // L\ triangle (see notes)
    // w (bottom) = r * cos 60 = r * 1/2
    // h (left) = r * sin 60 = r * sqrt(3)/2
    width_factor = 1/2 * radius;
    height_factor = Math.sqrt(3) / 2 * radius;

    // use the CENTER as reference point; ASSUME NORTHERN HEMISPHERE FOR NOW
    // x,y is [long,lat] format
    left = [long - radius, lat];
    right = [long + radius, lat];
    top_left = [long - width_factor, lat - height_factor];
    top_right = [long + width_factor, lat - height_factor];
    bot_left = [long - width_factor, lat + height_factor];
    bot_right = [long + width_factor, lat + height_factor];

    return [left, right, top_left, top_right, bot_left, bot_right];
}


// draw hexagon
function draw_hexagon(container, left, right, top_left, top_right, bot_left, bot_right, colour) {

    var canvas = document.getElementById(container);
    if (canvas.getContext) {

        var ctx = canvas.getContext("2d");

        /*var size = 512;
        canvas.style.width = size + "px";
        canvas.style.height = size + "px";
        var scale = window.devicePixelRatio; // Change to 1 on retina screens to see blurry canvas.
        canvas.width = Math.floor(size * scale);
        canvas.height = Math.floor(size * scale);
        // Normalize coordinate system to use css pixels.
        ctx.scale(scale, scale);*/

        ctx.beginPath();
        ctx.moveTo(left[0], left[1]);
        ctx.lineTo(top_left[0], top_left[1]);
        ctx.lineTo(top_right[0], top_right[1]);
        ctx.lineTo(right[0], right[1]);
        ctx.lineTo(bot_right[0], bot_right[1]);
        ctx.lineTo(bot_left[0], bot_left[1]);
        ctx.lineTo(left[0], left[1]);
        ctx.strokeStyle = "#000000";
        ctx.stroke();
        ctx.fillStyle = colour;
        ctx.fill();
    }
    return true;
}


// generate start points based on the radius; offsets are actually the top-left-most [long, lat] coordinates
function create_start_points(radius, rows, columns, left_offset, top_offset) {

    points = [];
    // start with rows
    for (var r=0; r < rows; r++) {

        // then columns
        for (var c=0; c < columns / 2; c++) {

            // even rows
            if (r % 2 == 0) {
                x = 3 * c * radius + left_offset;
            }
            // odd rows
            else {
                x = 3 * c * radius + 1.5 * radius + left_offset;
            }
            y = Math.sqrt(3) * r * radius / 2 + top_offset;
            points.push([radius, x, y]);
        }
    }

    return points;
}


// the MEASURED radius is the hexagon in NORTH SOUTH direction, NOT the true radius of hexagon.
// ASSUME lat 40
/*
function calculate_radius(measured_radius, lat) {

    // use the latitude to calculate radius -- as this WILL remain a constant with respect to the measured (N-W) radius
    const ns_2piR = 39940.653 // in km, circumference of earth around the poles
    radius_meters = measured_radius * 2 / Math.sqrt(3) * 1000;

    // now check with MapBox scaling
    // Equator, 0: 9783.936 meters/pixel
    // +/-20 latitude: 9193.892 meters/pixel
    // +/-40 latitude: 7494.929 meters/pixel
    // +/-60 latitude: 4891.968 meters/pixel
    // +/-80 latitude: 1698.963 meters/pixel
    radius = radius_meters / 5000; // lat 52

    return radius;
}
*/

// function that determines which latitude hexagon rows the coordinates are between
function find_hexagon_rows(radius, lat, bot_left_long, bot_left_lat, pixel_radius, rows, columns) {

    // [-170.335167, 72]
    // canvas is mirrored? why is first row starting in second column on map but not in canvas?

    // north south radius (for rows) has not changed - pixel_radius
    prev_lat = bot_left_lat;
    for (var r=0; r < rows; r++) {

        // get the new km_per_pixel value; the pixel value didn't change for the hexes.
        km_per_pixel = calculate_radius(radius, prev_lat)[1];
        new_radius = pixel_radius * km_per_pixel
        //console.log("New Radius", new_radius);

        // each row is only Math.sqrt(3)/2 of the actual radius in km; sizing is off, divide by 2 again?
        lat_change = calculate_latitude(new_radius * Math.sqrt(3) / 2, km_per_pixel);
        row_lat = prev_lat + lat_change;

        // loop thru to find the two rows that the coordinate is in between
        if (lat > row_lat) {
            console.log("data-looping", r, prev_lat, new_radius * Math.sqrt(3) / 2, lat_change, km_per_pixel);
            prev_lat = row_lat;
        } else {
            console.log(r, lat, prev_lat, row_lat, radius, pixel_radius);
            break;
        }
    }

    return true;
}


// calculate the EAST-WEST radius -- this appears to be applied to the map projection as well
function calculate_radius(measured_radius, lat) {
    /*
    *   at latitude 50:
    *   the latitude circle radius = 6356.7524 * cos 50 = 4086.0417 km
    *   circle 2piR = 4086.0417 * 2 * pi = 25673.3569
    *   1 degree longitude at latitude 50 = 25673.3569 / 360 = 71.3149 km
    *   calculate lat 50 radius using the 50 km reference for lat 40: 50 / 84.9898 * 71.3149 = 41.9550 km
    *   account for the meters/pixel as well; lat 40 is 7494.929 meters/pixel
    *   m/p = one_deg_longitude / 84.9898 (KM) * 7494.929 (METERS)
    */
    // rad = degree * Math.PI / 180
    /*lat_circle_radius = 6356.7524 * Math.cos(lat * Math.PI / 180); // in km
    one_deg_longitude = lat_circle_radius * 2 * Math.PI / 360;  // in km
    km_per_pixel = one_deg_longitude / 84.9898 * 7.494929
    ew_radius = measured_radius / km_per_pixel;*/
    //console.log(measured_radius, ": ", lat, ew_radius);


    km_per_pixel = 40075 * Math.cos(lat * Math.PI / 180) / Math.pow(2, 12);
    calc_radius = measured_radius / km_per_pixel;
    //console.log('calc_radius, km/pixel', calc_radius, km_per_pixel);

    return [calc_radius, km_per_pixel];
}


// calculate latitude change
function calculate_latitude(distance, km_per_pixel) {

    // arc length = degrees / 360 * (2 * Math.PI * 6356.7524)
    //degrees = 180 * distance * km_per_pixel / (Math.PI * 6356.7524)
    degrees = 180 * distance / (Math.PI * 6356.7524)

    //console.log('degrees, distance', degrees, distance);
    return degrees;
}

/*(C ∙ cos(latitude) / 2^(zoomlevel + 8)
cos(latitude) = 2^(zoomlevel + 8) / C*/


// normalize coordinates based on the grid
function normalize_coordinates(long, lat, top_left_long, top_left_lat, bot_right_long, bot_right_lat) {

    // normalize
    n_long = long / (bot_right_long - top_left_long);
    n_lat = lat / (top_left_lat - bot_right_lat);

    return [Math.abs(n_long), Math.abs(n_lat)];
}


// hexagon lat-long
function hexagon_lat_long(radius, long, lat) {

    km_per_pixel = calculate_radius(radius, lat)[1];
    width_factor = 1/2 * radius;
    height_factor = Math.sqrt(3) / 2 * radius;
    degrees = calculate_latitude(radius, km_per_pixel);
    width_deg = calculate_latitude(width_factor, km_per_pixel);
    height_deg = calculate_latitude(height_factor, km_per_pixel);

    left = [long - degrees, lat];
    right = [long + degrees, lat];
    top_left = [long - width_deg, lat + height_deg];
    top_right = [long + width_deg, lat + height_deg];
    bot_left = [long - width_deg, lat - height_deg];
    bot_right = [long + width_deg, lat - height_deg];

    return [left, top_left, top_right, right, bot_right, bot_left, left];
}


// find overlap for the hexagons
function find_intersect_points(intersect, poly1, poly2) {

    // find the points that are the same as the corners of the polygons
    pts = [];
    for (var pt in intersect) {
        // keep 5 decimals
        ipt = [intersect[pt][0].toFixed(6), intersect[pt][1].toFixed(6)]
        poly_match = false;
        //ipt = intersect[pt];
        for (var poly in poly1) {
            poly_pt = [poly1[poly][0].toFixed(6), poly1[poly][1].toFixed(6)]
            if (poly_pt[0] == ipt[0]) {
                if (poly_pt[1] == ipt[1]) {
                    pts.push(pt);
                    poly_match = true;
                    break;
                }
            }
        }
        if (!poly_match) {
            for (var poly in poly2) {
                poly_pt = [poly2[poly][0].toFixed(6), poly2[poly][1].toFixed(6)]
                if (poly_pt[0] == ipt[0]) {
                    if (poly_pt[1] == ipt[1]) {
                        pts.push(pt);
                        break;
                    }
                }
            }
        }
    }

    // indices of pts that are corners of polygon
    other_pts = [];
    remove_pts = [];
    for (var ins in intersect) {
        if (!pts.includes(ins) && ins != intersect.length-1) {
            other_pts.push(intersect[ins]);
        }
        else if (pts.includes(ins)) {
            remove_pts.push(intersect[ins]);
        }
    }
    console.log('Intersect Points:', other_pts);
    console.log('Remove Points:', remove_pts);

    return [other_pts, remove_pts];
}


// function that re_draws the hexagon based on intersection points
function redraw_hexagon(pts, remove_pts, poly1) {

    // find remove_pts (should only be 1 match)
    poly = poly1
    spliced = false;
    for (var pt in remove_pts) {
        rpt = [remove_pts[pt][0].toFixed(6), remove_pts[pt][1].toFixed(6)];

        // in case first value needs to be replaced, set prev_pt to the second last value
        poly2ndlast = poly.length - 2
        prev_pt = [poly[poly2ndlast][0].toFixed(6), poly[poly2ndlast][1].toFixed(6)]
        //console.log("PREV", prev_pt);
        for (var p in poly) {
            poly_pt = [poly[p][0].toFixed(6), poly[p][1].toFixed(6)];
            if (poly_pt[0] == rpt[0]) {
                if (poly_pt[1] == rpt[1]) {

                    if (!spliced) {
                        // found match, now order the points to be added
                        add_pts = order_points.apply(this, [prev_pt, poly_pt].concat(pts))

                        // put splice here
                        //console.log([parseInt(p), 1].concat(pts), poly[p])
                        poly.splice.apply(poly, [parseInt(p), 1].concat(add_pts));

                        // if splice index is 0, need to adjust the last pt to equal first pt
                        if (parseInt(p) == 0) {
                            poly.splice.apply(poly, [poly.length-1, 1].concat([add_pts[0]]));
                        }
                        spliced = true;
                        break;
                    }
                    else {
                        // if already spliced, just remove points that need to be removed
                        poly.splice(parseInt(p), 1);
                        if (parseInt(p) == 0) {
                            poly.splice.apply(poly, [poly.length-1, 1].concat([poly[0]]))
                            break;
                        }
                    }
                }
            }
            prev_pt = poly_pt;  // for reference to order the added pts
        }
    }
    return poly;
}


// determine how to order the points based on prev and current point (that you are replacing)
// base it on distance, since the closer point should be the replacement... find exceptions later
function order_points(prev_pt, remove_pt, new_pt1, new_pt2) {

    pts = [new_pt1, new_pt2]
    // find pt with furthest distance
    min_dist = 1000000;
    min_index = 1;
    for (var ins in pts) {
        dist = turf.distance(prev_pt, pts[ins])
        if (dist < min_dist) {
            min_dist = dist;
            min_index = ins;
            console.log(min_dist, min_index);
        }
    }

    if (min_index == 1) {
        pts = [new_pt2, new_pt1]
    }

    return pts;
}


// get the second point if only 1 point found on intersect
// this is likely due to multi-polygon overlap
function get_second_pt(pt, intersect) {

    // get the pt that did match
    console.log("All Intersects", intersect);
    for (var ins in intersect) {
        ipt = [intersect[ins][0].toFixed(6), intersect[ins][1].toFixed(6)];
        if (ipt[0] == pt[0].toFixed(6) && ipt[1] == pt[1].toFixed(6)) {
            index = ins;
            break;
        }
    }

    // find pt with furthest distance
    max_dist = 0;
    max_index = index;
    for (var ins in intersect) {
        dist = turf.distance(intersect[index], intersect[ins])
        if (dist > max_dist) {
            max_dist = dist;
            max_index = ins;
            //console.log(max_dist, max_index);
        }
    }
    //console.log("Get Second Pt", pt, intersect[max_index]);

    return [pt, intersect[max_index]]
}


// this function looks for "ring" around weather station based on distance and level.
// the bounding box matters, because the center lat, is used as the reference for the most equilateral hexagon.
function station_rings(distance, level, station, coord, bot_lat, top_lat) {

    dist = turf.distance(station, coord);

    // factor in the latitude of the station [long, lat]
    lat = station.geometry.coordinates[1];
    longest_distance = distance * level * Math.sqrt(3);

    // the other measurement to take into account is the shortest distance in that level
    // for EVEN levels, it's exactly (level + 1) * r
    if (level == 1) {
        shortest_dist = convert_distance(distance * level * Math.sqrt(3), lat, bot_lat, top_lat);
        /*if (station.geometry.coordinates[0] == -150 && station.geometry.coordinates[1] == 61.22116571887389) {
            result = (dist <= converted_distance * (1 + 0.05) && dist >= shortest_dist * (1 - 0.05));
            if (!result) { console.log(result, level, shortest_dist, dist, converted_distance) }
        }*/
    } else {
        shortest_dist = distance * level * 1.5;
        shortest_dist = convert_distance(shortest_dist, lat, bot_lat, top_lat);
    }

    // [-150, 61.22116571887389] [-152.9299247223268, 65.11533712450444
    if (station.geometry.coordinates[0] == -152.9299247223268 && station.geometry.coordinates[1] == 65.11533712450444) {
        result = (dist <= longest_distance * (1 + 0.05) && dist >= shortest_dist * (1 - 0.05));
        if (result) { console.log(result, level, shortest_dist, dist, longest_distance) }
    }
    if (dist == 0) {
        //console.log("Station", station);
    }

    // 5% margin of error for below 68th latitude
    return ((dist <= longest_distance * (1 + 0.05) && dist >= shortest_dist * (1 - 0.05)) ? [true, dist]: [false, dist]);
}


// convert the distance based on the latitude and reference latitude
function convert_distance(distance, lat, bot_lat, top_lat) {

    // find pixel distance of the distance at the middle latitude
    middle_lat = (top_lat + bot_lat) / 2;
    km_per_pixel = 40075 * Math.cos(middle_lat * Math.PI / 180) / Math.pow(2, 12);
    pixel_distance = distance / km_per_pixel;

    // now use pixel distance to convert it to the distance at the needed latitude
    km_per_pixel = 40075 * Math.cos(lat * Math.PI / 180) / Math.pow(2, 12);
    return pixel_distance * km_per_pixel;
}


// check rings on the same level that overlap
function ring_overlap(ring) {

    collector = [];  // collects all unique coordinates (centroids)
    overlap = [];  // collects only the overlapping coordinates
    for (var r in ring) {
        coord = ring[r].geometry.coordinates
        check = false
        for (var c in collector) {
            if (collector[c][0] == coord[0] && collector[c][1] == coord[1]) {
                overlap.push(coord);
                check = true;
                break;
            }
        }
        if (!check) {
            collector.push(coord);
        }
    }
    console.log(collector);

    // if the sizes don't match, that means there's overlaps
    if (collector.length == ring.length) {
        return false;
    }
    else {
        for (var o in overlap) {
            temp = [];  // temperatures to take the mean of
            indices = [];  // save the indices for easier reference
            for (var r in ring) {
                coord = ring[r].geometry.coordinates
                if (overlap[o][0] == coord[0] && overlap[o][1] == coord[1]) {
                    // add temperature and index
                    temp.push(ring[r].properties.temperature);
                    indices.push(r);
                }
            }

            // take the mean of temperatures and add it back into each indexed ring coordinate
            //console.log(temp.reduce((a,b) => a + b, 0) / temp.length);
            for (var i in indices) {
                index = indices[i];
                ring[index].properties.temperature = temp.reduce((a,b) => a + b, 0) / temp.length;
            }
        }
        return ring;
    }
}


// check rings one level below for overlap
function ring_overlap_below(ring1, ring2, weights) {

    collector1 = [];  // collects all unique coordinates (centroids)
    for (var r in ring1) {
        coord = ring1[r].geometry.coordinates;
        check = false;
        for (var c in collector1) {
            if (collector1[c][0] == coord[0] && collector1[c][1] == coord[1]) {
                check = true;
                break;
            }
        }
        if (!check) {
            collector1.push(coord);
        }
    }
    console.log(collector1);

    collector2 = [];  // collects all unique coordinates (centroids)
    for (var r in ring2) {
        coord = ring2[r].geometry.coordinates
        check = false
        for (var c in collector2) {
            if (collector2[c][0] == coord[0] && collector2[c][1] == coord[1]) {
                check = true;
                break;
            }
        }
        if (!check) {
            collector2.push(coord);
        }
    }
    console.log(collector2);

    // go thru collector1 to find overlaps in collector2
    overlap = [];  // collects only the overlapping coordinates
    for (var col in collector1) {
        coord = collector1[col];
        for (var c in collector2) {
            if (collector2[c][0] == coord[0] && collector2[c][1] == coord[1]) {
                overlap.push(coord);
                break;
            }
        }
    }

    if (overlap.length == 0) {
        return [false, false];
    }

    // if the sizes don't match, that means there's overlaps
    for (var o in overlap) {

        // ring 1
        temp1 = [];  // temperatures to take the mean of
        indices1 = [];  // save the indices for easier reference
        for (var r in ring1) {
            coord = ring1[r].geometry.coordinates
            if (overlap[o][0] == coord[0] && overlap[o][1] == coord[1]) {
                // add temperature and index
                temp1.push(ring1[r].properties.temperature);
                indices1.push(r);
            }
        }

        // ring 2
        temp2 = [];  // temperatures to take the mean of
        //indices2 = [];  // save the indices for easier reference
        for (var r in ring2) {
            coord = ring2[r].geometry.coordinates
            if (overlap[o][0] == coord[0] && overlap[o][1] == coord[1]) {
                // add temperature and index
                temp2.push(ring2[r].properties.temperature);
                //indices2.push(r);
            }
        }

        // weighted averages (example ring1 to ring2, 60/40: weights[0] = 0.6; ring2 to ring1, 50/50: weight[1] = 0.5)
        ring1_temp = temp1.reduce((a,b) => a + b, 0) * weights[0] + temp2.reduce((a,b) => a + b, 0) * (1 - weights[0])
        //ring2_temp = temp1.reduce((a,b) => a + b, 0) * weights[1] + temp2.reduce((a,b) => a + b, 0) * (1 - weights[1])

        // take the mean of temperatures and add it back into each indexed ring coordinate
        //console.log(temp.reduce((a,b) => a + b, 0) / temp.length);
        for (var i in indices1) {
            index = indices1[i];
            ring1[index].properties.temperature = ring1_temp;
        }
        // second one gets overwritten on the map anyway
        /*(for (var i in indices2) {
            index = indices2[i];
            ring2[index].properties.temperature = ring2_temp;
        }*/
    }
    return [ring1, ring2];
}

