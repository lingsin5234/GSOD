// constructor function
MapUSA = function(_parentElement, _svgHeight, _svgWidth, _yVariable, _selDate) {
    this.parentElement = _parentElement;
    this.svgHeight = _svgHeight;
    this.svgWidth = _svgWidth;
    this.yVariable = _yVariable;
    this.selDate = _selDate;

    this.initVis();
}

// initVis!
MapUSA.prototype.initVis = function() {
    var vis = this;

    mapboxgl.accessToken = mapbox_token;
    vis.map = new mapboxgl.Map({
        container: 'map',
        //style: 'mapbox://styles/mapbox/satellite-streets-v11',
        style: 'mapbox://styles/mapbox/streets-v11',
        //style: 'mapbox://styles/mapbox/dark-v10',
        //style: 'mapbox://styles/mapbox/light-v10',
        //center: [-96, 37.8],
        center: [95.899147, 18.088694],
        zoom: 5,
        minZoom: 4
    });

    vis.wrangleData();
}

// wrangleData
MapUSA.prototype.wrangleData = function () {
    var vis = this;

    // get updated variables
    //vis.yVariable = $('#data-type-select').val();
    //vis.selDate = $("#dateLabel").text();

    /*vis.newData = stations.filter(function(d) {
        //console.log(vis.selDate, typeof(vis.selDate));
        return d.key == vis.selDate;
    })[0]['data'].map(function (x) {
        //console.log(x)
        return {
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: x.geometry.coordinates
            },
            properties: {
                title: x.properties[vis.yVariable]
            }
        }
    });*/
    //console.log(vis.newData);
    vis.updateVis();
}

// updateVis
MapUSA.prototype.updateVis = function () {
    var vis = this;

    vis.map.on('load', function() {

        // using gradient fill from github
        vis.map.addSource('canvas-source', {
            type: 'canvas',
            canvas: 'canvasMap',
            coordinates: [
                [91.4461, 21.5006],
                [100.3541, 21.5006],
                [100.3541, 13.9706],
                [91.4461, 13.9706]
            ],

            // The canvas is static, animate should be set to false to improve performance.
            animate: false
        });

        vis.map.addLayer({
            id: 'canvas-layer',
            type: 'raster',
            source: 'canvas-source'
        });

        vis.map.addSource('canvas-test', {
            type: 'canvas',
            canvas: 'canvasID',
            coordinates: [
                [91.4461, 21.5006],
                [100.3541, 21.5006],
                [100.3541, 13.9706],
                [91.4461, 13.9706]
            ],

            // The canvas is static, animate should be set to false to improve performance.
            animate: true
        });

        vis.map.addLayer({
            id: 'canvas-testLayer',
            type: 'raster',
            source: 'canvas-test'
        });


        /*
        vis.map.addSource('points', {
            type: 'geojson',
            data: {
                type: 'FeatureCollection',
                features: vis.newData
            }
        });
        vis.map.addLayer({
            id: 'points',
            type: 'symbol',
            source: 'points',
            layout: {
                // get the icon name from the source's "icon" property
                // concatenate the name to get an icon from the style's sprite sheet
                'icon-image': ['concat', ['get', 'icon'], '-15'],
                // get the title name from the source's "title" property
                'text-field': ['get', 'title'],
                'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
                'text-offset': [0, 0],
                'text-anchor': 'top'
            },
            paint: {
                'text-color': 'blue'
            }
        });
        //console.log(vis.map.getSource('points'));

        // attempt to add weather gradient fill

        // try fill
        /*vis.map.addLayer({
            'id': 'weather-fill',
            'type': 'fill',
            'source': 'points',
            'minzoom': 3,
            'maxzoom': 10,
            'paint': {
                'fill-color': {
                property: 'title',
                type: 'interval', // cannot use interpolate for fill-color
                stops: [
                    [-60, 'rgba(69,117,180,0.5)'],
                    [-20, 'rgb(145,191,219)'],
                    //[0.4, 'rgb(224,243,248)'],
                    //[0.6, 'rgb(254,224,144)'],
                    [20, 'rgb(253,141,89)'],
                    [60, 'rgb(215,48,39)']
                ]
                },
                'fill-opacity': 0.8
            }
        }, 'waterway-label');*/



        /*
        document.getElementById('data-type-select')
            .addEventListener('change', function() {
                vis.map.getSource('points').setData(updateData(vis.newData));
            })
        document.getElementById('date-slider')
            .addEventListener('mouseup', function() {
                //console.log('call change from date slider.');
                vis.map.getSource('points').setData(updateData(vis.newData));
            })*/
    });
}
