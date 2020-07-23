/*
*   This file works with the bi.js file to calculate the normalized coordinates
*   based on the canvas sizing. Height and width are separately normalized to
*   values between 0 and 1.
*/

function normalize_coord(lat_start, lat_end, long_start, long_end, lat, long) {

    // latitude -- assume start is negative
    lat_total = Math.abs(lat_start) + Math.abs(lat_end);
    if (lat < 0) {
        norm_lat = Math.abs(lat) / lat_total;
    } else {
        norm_lat = (lat + 89.99) / lat_total;  // note that the start and end are both -0.01
    }

    // longitude
    longitude = Math.abs(lat_start) + Math.abs(lat_end);
    if (lat < 0) {
        norm_long = Math.abs(lat) / lat_total;
    } else {
        norm_long = (lat + 179.99) / lat_total; // only the start is -179.99
    }

    return [norm_lat, norm_long];
}


