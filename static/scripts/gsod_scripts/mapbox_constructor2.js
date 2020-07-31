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
        zoom: 3,
        minZoom: 3,
        //style: 'mapbox://styles/mapbox/satellite-streets-v11',
        style: 'mapbox://styles/mapbox/streets-v11',
        //style: 'mapbox://styles/mapbox/dark-v10',
        //style: 'mapbox://styles/mapbox/light-v10',
        center: [-100, 36],     // US center -- roughly
        zoom: 3.5
    });

    vis.wrangleData();
}

// wrangleData
MapUSA.prototype.wrangleData = function () {
    var vis = this;

    // get updated variables
    //vis.yVariable = $('#data-type-select').val();
    //vis.selDate = $("#dateLabel").text();

    if (hexGrid != null) {
        console.log(hexGrid);
        vis.hexGrid = hexGrid;
        vis.updateVis();
    }
}

// updateVis
MapUSA.prototype.updateVis = function () {
    var vis = this;

    vis.map.on('load', function() {
        /*vis.map.addSource('points', {
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
        });*/
        //console.log(vis.map.getSource('points'));

        vis.map.addSource('hexagons-draw', {
            type: 'geojson',
            data: vis.hexGrid //hexagonGEO
        });

        vis.map.addLayer({
            id: 'hexagons-draw',
            type: 'fill',
            source: 'hexagons-draw',
            paint: {
                'fill-color':
                    [
                        'case',
                        [">", ["get", "temperature"], 0],
                        [
                            "interpolate", ["linear"], ["get", "temperature"],
                                0, 'rgb(148,0,211)',
                                0.45, 'rgb(114,212,188)',
                                0.55, 'rgb(100, 255, 50)',
                                0.7, 'rgb(255, 255, 0)',
                                0.9, 'rgb(255, 0, 0)',
                                1, 'rgb(153, 0, 0)'
                        ],
                        'rgb(0, 0, 0)'
                    ],
                //'fill-opacity': 0.8
                'fill-opacity':
                    [
                        'case',
                        [">", ["get", "temperature"], 0], 0.3,
                        0,
                    ]
            }
        });

        /*document.getElementById('data-type-select')
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
