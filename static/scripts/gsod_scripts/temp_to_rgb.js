/*
*   This file converts temperature into rgb based on which interval it lands in
*   defunct method is good for a TRUE gradient
*   it is more aesthetically pleasing to use a TIERED gradient
*/

// t for temperate
function temp2rgb(t) {

    // if statements in order
    // <= -40 = rgb(0,0,80)
    if (t <= -40) {
        rgb = [0,0,80];
    }
    // -30 - -39 = rgb(0,0,119)
    else if (t <= -30) {
        rgb = [0,0,119];
    }
    // -20 - -29 = rgb(0,0,159)
    else if (t <= -20) {
        rgb = [0,0,159];
    }
    // -15 - -19 = rgb(2,2,255)
    else if (t <= -15) {
        rgb = [2,2,255];
    }
    // -10 - -14 = rgb(41,41,255)
    else if (t <= -10) {
        rgb = [41,41,255];
    }
    // -5 - -9 = rgb(100,100,255)
    else if (t <= -5) {
        rgb = [100,100,255];
    }
    // 0 - -4 = rgb(159,159,255)
    else if (t <= 0) {
        rgb = [159,159,255];
    }
    // 5 - 1 = rgb(255,227,177)
    else if (t <= 5) {
        rgb = [255,227,117];
    }
    // 10 - 6 = rgb(255,213,137)
    else if (t <= 10) {
        rgb = [255,213,137];
    }
    // 15 - 11 = rgb(255,200,98)
    else if (t <= 15) {
        rgb = [255,200,98];
    }
    // 20 - 16 = rgb(255,186,59)
    else if (t <= 20) {
        rgb = [255,186,59];
    }
    // 25 - 21 = rgb(255,172,20)
    else if (t <= 25) {
        rgb = [255,172,20];
    }
    // 30 - 26 = rgb(255,165,0)
    else if (t <= 30) {
        rgb = [255,165,0];
    }
    // 35 - 31 = rgb(255,69,0)
    else if (t <= 35) {
        rgb = [255,69,0];
    }
    // 40 - 35 = rgb(204,55,0)
    else if (t <= 40) {
        rgb = [204,55,0];
    }
    // 40+ = rgb(153,0,0)
    else {
        rgb = [153,0,0];
    }

    return rgb;
}

// previous version; this gradient is too "smooth"; showing temperature is better with tiered above
function temp2rgb_defunct(t) {

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


