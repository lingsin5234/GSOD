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
    width_factor = 1/2 * radius
    height_factor = Math.sqrt(3) / 2 * radius

    // use the CENTER as reference point; ASSUME NORTHERN HEMISPHERE FOR NOW
    // x,y is [long,lat] format
    left = [long - radius, lat]
    right = [long + radius, lat]
    top_left = [long - width_factor, lat - height_factor]
    top_right = [long + width_factor, lat - height_factor]
    bot_left = [long - width_factor, lat + height_factor]
    bot_right = [long + width_factor, lat + height_factor]

    return [left, right, top_left, top_right, bot_left, bot_right]
}


// draw hexagon
function draw_hexagon(container, left, right, top_left, top_right, bot_left, bot_right) {

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
        ctx.fill();
    }
    return true;
}

