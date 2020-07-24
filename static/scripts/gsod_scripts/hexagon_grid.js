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
// ASSUME latitude 40
function calculate_radius(measured_radius) {

    // use the latitude to calculate radius -- as this WILL remain a constant with respect to the measured (N-W) radius
    const ns_2piR = 39940.653 // in km, circumference of earth around the poles
    radius_meters = measured_radius * 2 / Math.sqrt(3) * 1000;

    // now check with MapBox scaling
    // Equator, 0: 9783.936 meters/pixel
    // +/-20 latitude: 9193.892 meters/pixel
    // +/-40 latitude: 7494.929 meters/pixel
    // +/-60 latitude: 4891.968 meters/pixel
    // +/-80 latitude: 1698.963 meters/pixel
    radius = radius_meters / 7494.929;

    return radius;
}
