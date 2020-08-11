/* Creating a Gradient for the Legend on the Temperature Map */
/*
0, 'rgb(148,0,211)',
0.45, 'rgb(114,212,188)',
0.55, 'rgb(100,255,50)',
0.7, 'rgb(255,255,0)',
0.9, 'rgb(255,0,0)',
1, 'rgb(153,0,0)'
*/

function createGradient(start, end, height, parentID) {

    // default to "100 x height" pixel box of this
    cols = 100;
    const [r1, g1, b1] = getRGB(start)
    const [r2, g2, b2] = getRGB(end)
    //console.log(r1, g1, b1);
    //console.log(r2, g2, b2);
    //console.log(Interpolate(r1, r2, cols, 1));

    parent = document.getElementById(parentID);
    legend = document.createElement("span");
    legend.style.backgroundColor = start;
    legend.style.width = cols;
    legend.style.height = height;
    legend.offsetTop = "200px";
    parent.appendChild(legend);

    return true;
}


// function breaks down the string rgb(r, g, b)
function getRGB(str) {

    rgb = str.replace('rgb(', '').replace(')', '')
    const [r, g, b] = rgb.split(",")
    //console.log(str, r, g, b);
    return [r, g, b]
}


// Interpolate the r / g / b values
// steps is the height of the array; count is which height currently at
function Interpolate(start, end, steps, count) {
    var s = parseInt(start);
    var e = parseInt(end);
    final = s + (((e - s) / steps) * count);
    //console.log(s, e, final);
    return Math.floor(final);
}
