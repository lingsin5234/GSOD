var bi=function(resX,resY,data,container) {

    var arr=[];
    var map_size = [-89.99, 89.99, -179.99, 180]

    function make(x,y,v){
        return {x:x,y:y,v:v,dist:0,weight:0}
    }

    var cnv = container;
    var ctx=cnv.getContext("2d");

    var imageData = ctx.getImageData(0,0,resX,resY);
    var rawData = imageData.data;

    function metric(x1,y1,x2,y2){

        var f=resX/resY;

        var x=(x2-x1);
        var y=(y2-y1);


       x=x*x*f;

        y=y*y/f;

        return (1/(x+y));
    }


    function drawGradient(ready_state){

        var p={x:0,y:0};

        function sortBy(a,b){
            return a.dist>b.dist;
        }


        function calculateDist(p){

            var sumDist=0;
            var maxDist=0;

            for(var i=0;i<arr.length;i++){
                var d=metric(p.x, p.y,arr[i].x,arr[i].y);
                d+=0.001;
                arr[i].dist=d;
            }

            for(i=0;i<arr.length;i++){

                sumDist+=arr[i].dist;
            }

            for(i=0;i<arr.length;i++){
                arr[i].weight=arr[i].dist/sumDist;
            }

        }

        dt1 = Date.now();
        for (y = 0; y < resY; y++) {
            for (x = 0; x < resX; x++) {

                p.x=x/resX;
                p.y=y/resY;

                //dt1 = Date.now();
                calculateDist(p);
                //dt2 = Date.now();

                var r=0;
                var g=0;
                var b=0;

                for(var i=0;i<arr.length;i++){
                    r+=arr[i].v[0]*arr[i].weight;
                    g+=arr[i].v[1]*arr[i].weight;
                    b+=arr[i].v[2]*arr[i].weight;
                }
                //dt3 = Date.now();

                r=Math.floor(Math.min(255,r));
                g=Math.floor(Math.min(255,g));
                b=Math.floor(Math.min(255,b));

                var index=(x+y*resX)*4;
                rawData[index]=r;
                rawData[index+1]=g;
                rawData[index+2]=b;

                /*console.log("Coord processing: calculateDist(): ", dt2-dt1, "ms, arr loop: ", dt3-dt2, "ms, rest: ",
                Date.now()-dt3);*/
            }
        }
        console.log("Full process:", Date.now() - dt1);

        if (ready_state) {
            // add transparency (r, g, b, alpha)
            //console.log("imageData.length", rawData.length)
            for (var i=3; i < rawData.length; i+=4) {
                rawData[i] = 200;
            }
        }

        ctx.putImageData(imageData,0,0);
    }


    function getCanvas(){
        return cnv;

    }

    function addPoint(x,y,r,g,b){

        var point=make(x,y,[r,g,b]);
        arr.push(point);
        //drawGradient(false);
        return point;

    }

    /*
    *   Loop thru the points
    *   Calculate normalized coordinates
    *   Assign the RGB based on the value
    */
    POI = [];
    for (var dat in data) {
        add_pt = normalize_coord.apply(this, map_size.concat(data[dat]['geometry']['coordinates']))
        POI.push(add_pt.concat(temp2rgb(data[dat].properties.title)));
    }

    for (var pt in POI) {
        //console.log(POI[pt]);
        addPoint.apply(this, POI[pt]);
    }

    // perform the transparency just once
    drawGradient(true);
};
