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
        //style: 'mapbox://styles/mapbox/streets-v11',
        style: 'mapbox://styles/mapbox/dark-v10',
        //style: 'mapbox://styles/lingsin5234/ckattfmaf09bn1io5puf30hxs',  // Albers USA -- used for elections
        // style: 'mapbox://styles/mapbox/light-v10',
        center: [-96, 37.8],
        zoom: 3.5
    });

    vis.wrangleData();
}

// wrangleData
MapUSA.prototype.wrangleData = function () {
    var vis = this;

    // get updated variables
    vis.yVariable = $('#data-type-select').val();
    vis.selDate = $("#dateLabel").text();

    vis.newData = stations.filter(function(d) {
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
    });

    vis.updateVis();
}

// updateVis
MapUSA.prototype.updateVis = function () {
    var vis = this;

    vis.map.on('load', function() {
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
                'text-color': 'red'
            }
        });
        //console.log(vis.map.getSource('points'));

        document.getElementById('data-type-select')
            .addEventListener('change', function() {
                vis.map.getSource('points').setData(updateData(vis.newData));
            })
        document.getElementById('date-slider')
            .addEventListener('mouseup', function() {
                //console.log('call change from date slider.');
                vis.map.getSource('points').setData(updateData(vis.newData));
            })
    });
}
