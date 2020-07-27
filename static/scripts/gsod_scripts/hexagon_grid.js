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
        ipt = [intersect[pt][0].toFixed(5), intersect[pt][1].toFixed(5)]
        poly_match = false;
        //ipt = intersect[pt];
        for (var poly in poly1) {
            poly_pt = [poly1[poly][0].toFixed(5), poly1[poly][1].toFixed(5)]
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
                poly_pt = [poly2[poly][0].toFixed(5), poly2[poly][1].toFixed(5)]
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
    //console.log(other_pts);

    return [other_pts, remove_pts];
}


// function that re_draws the hexagon based on intersection points
function redraw_hexagon(pts, remove_pts, poly1) {

    // find remove_pts (should only be 1 match)
    poly = poly1
    for (var pt in remove_pts) {
        rpt = [remove_pts[pt][0].toFixed(5), remove_pts[pt][1].toFixed(5)];

        // in case first value needs to be replaced, set prev_pt to the second last value
        poly2ndlast = poly.length - 2
        prev_pt = [poly[poly2ndlast][0].toFixed(5), poly[poly2ndlast][1].toFixed(5)]
        //console.log("PREV", prev_pt);
        for (var p in poly) {
            poly_pt = [poly[p][0].toFixed(5), poly[p][1].toFixed(5)];
            if (poly_pt[0] == rpt[0]) {
                if (poly_pt[1] == rpt[1]) {

                    // found match, now order the points to be added
                    add_pts = order_points.apply(this, [prev_pt, poly_pt].concat(pts))

                    // put splice here
                    //console.log([parseInt(p), 1].concat(pts), poly[p])
                    poly.splice.apply(poly, [parseInt(p), 1].concat(add_pts));

                    // if splice index is 0, need to adjust the last pt to equal first pt
                    if (parseInt(p) == 0) {
                        poly.splice.apply(poly, [poly.length-1, 1].concat([add_pts[0]]));
                    }
                    console.log('AFTER', poly, remove_pts, add_pts);
                    return poly;
                }
            }
            prev_pt = poly_pt;  // for reference to order the added pts
        }
    }
}


// determine how to order the points based on prev and current point (that you are replacing)
function order_points(prev_pt, remove_pt, new_pt1, new_pt2) {

    // downward
    if (prev_pt[1] > remove_pt[1]) {
        if (new_pt1[1] > new_pt2[1]) {
            pts = [new_pt1, new_pt2];
        } else {
            pts = [new_pt2, new_pt1];
        }
    }
    // upward
    else if (prev_pt[1] < remove_pt[1]) {
        if (new_pt1[1] < new_pt2[1]) {
            pts = [new_pt1, new_pt2];
        } else {
            pts = [new_pt2, new_pt1];
        }
    }
    // leftward
    else if (prev_pt[0] > remove_pt[0]) {
            if (new_pt1[0] > new_pt2[0]) {
                pts = [new_pt2, new_pt1];
            } else {
                pts = [new_pt1, new_pt2];
            }
    }
    // rightward
    else if (prev_pt[0] < remove_pt[0]) {
        if (new_pt1[0] < new_pt2[0]) {
            pts = [new_pt2, new_pt1];
        } else {
            pts = [new_pt1, new_pt2];
        }
    }

    return pts;
}

