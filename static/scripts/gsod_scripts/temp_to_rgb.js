/*
*   This file converts temperature into rgb based on which interval it lands in
*/

// t for temperate
function temp2rgb(t) {

    /*
    *   0 and below, fade from white-ish colour to dark blue
    *   dark blue = rgb(0, 0, 100)
    *   white-ish blue = rgb(237, 237, 255)
    *   red = 237 / 15 til -15
    *   green = 237 / 15 til -15
    *   blue = (255 - 100) / 25 start at -16
    *   bottoms out at -40
    */
    if (t <= 0) {
        r = (t < -15 ? 0 : (15 + t) * 237 / 15);
        g = (t < -15 ? 0 : (15 + t) * 237 / 15);
        b = (t < -15 ? (t < -40 ? 100 : (15 + t) * (255 - 100) / 25) : 255); // -15 til -40 use formula
    }

    /*
    *   1 to 25, use white-ish to orange
    *   orange = rgb(255, 172, 20)
    *   pale yellow = rgb(255, 248, 235)
    *   red = 255
    *   green formula = (248 - 172) / 25
    *   blue formula = (235 - 20) / 25
    */
    else if (t > 0 && t <= 25) {
        r = 255
        g = t * (248 - 172) / 25
        b = t * (235 - 20) / 25
    }

    /*
    *   25+, fade orange towards red
    *   orange = rgb(255, 172, 20)
    *   crimson red = rgb(194, 37, 32)
    *   r = (194 - 255) / 20 + 254 <- just to account for above statement ending at orange
    *   g = (37 - 172) / 20 + 172
    *   b = (32 - 20) / 20
    *   top out at +45
    */
    else {
        r = (t > 45 ? 194 : t * (194 - 255) / 20 + 254);
        g = (t > 45 ? 37 : t * (37 - 172) / 20 + 172);
        b = (t > 45 ? 32 : t * (32 - 20) / 20);
    }

    return [r, g, b];
}
