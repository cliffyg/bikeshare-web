var pointFeature;
var vectorLayer;
var features = [];
function init() {
  map = new OpenLayers.Map("mapdiv");
  var newLayer = new OpenLayers.Layer.OSM("Local Tiles", "http://tile.openstreetmap.org/${z}/${x}/${y}.png", {numZoomLevels: 19});
  //var newLayer = new OpenLayers.Layer.OSM("Local Tiles", "http://bikeshare.cs.pdx.edu/osm/${z}/${x}/${y}.png", {numZoomLevels: 19, crossOriginKeyword: null});
  map.addLayer(newLayer); 
  // allow testing of specific renderers via "?renderer=Canvas", etc
  var renderer = OpenLayers.Util.getParameters(window.location.href).renderer;
  renderer = (renderer) ? [renderer] : OpenLayers.Layer.Vector.prototype.renderers;
  var layer_style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
  layer_style.fillOpacity = 0.2;
  layer_style.graphicOpacity = 1;
  var lonlat = new OpenLayers.LonLat(-122.680591,45.510016).transform(
      new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
      new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator
    );
      vectorLayer = new OpenLayers.Layer.Vector("Simple Geometry", {
          styleMap: new OpenLayers.StyleMap({'default':{
              strokeColor: "${pointColor}",
              strokeOpacity: 1,
              strokeWidth: 3,
              fillColor: "${pointColor}",
              fillOpacity: 0.8,
              pointRadius: 5,
              pointerEvents: "visiblePainted",
              label : "${name}",
              fontColor: "${favColor}",
              fontSize: "12px",
              fontFamily: "Courier New, monospace",
              fontWeight: "bold",
              labelAlign: "${align}",
              labelXOffset: "${xOffset}",
              labelYOffset: "${yOffset}"
          }}),
          renderers: renderer
      });
  var zoom = 14;
      var point = new OpenLayers.Geometry.Point(-122.680591,45.510016);
      point.transform(
      	   //this has to be done, not sure of the reason
            	new OpenLayers.Projection("EPSG:4326"), 
            	new OpenLayers.Projection("EPSG:900913") 
      
      );
      var pointFeature = new OpenLayers.Feature.Vector(point);
      pointFeature.attributes = {
      name: "BikeShare - PSU Computer Science",
      favColor: 'red',
      align: "cm",
      	xOffset: 10,
      	yOffset: 10,
      	pointColor: 'blue'
          };
      features.push(pointFeature);
      var providenceParkPoint = new OpenLayers.Geometry.Point(-122.691692,45.521718);
      providenceParkPoint.transform(
      		new OpenLayers.Projection("EPSG:4326"), 
  		new OpenLayers.Projection("EPSG:900913") 
  		);
      providenceParkPointFeature = new OpenLayers.Feature.Vector(providenceParkPoint);
      providenceParkPointFeature.attributes = {
  	name : "BikeShare - Providence Park",
  	favColor : 'red',
  	align : 'cm',
  	xOffset : 10,
  	yOffset : 10,
  	pointColor : 'blue'
      };
      features.push(providenceParkPointFeature);
      esplanadePoint = new OpenLayers.Geometry.Point(-122.667549,45.516573);
      esplanadePoint.transform(
  	new OpenLayers.Projection("EPSG:4326"), 
  	new OpenLayers.Projection("EPSG:900913")
      );
      esplanadePointFeature = new OpenLayers.Feature.Vector(esplanadePoint);
      esplanadePointFeature.attributes = {
  	name : "BikeShare - East Bank Esplanade",
          favColor : 'red',
          align : 'cm',
          xOffset : 10,
          yOffset : 10,
          pointColor : 'blue'
      };
      features.push(esplanadePointFeature);
      waterfrontPoint = new OpenLayers.Geometry.Point(-122.673013,45.509234);
      waterfrontPoint.transform(
  	new OpenLayers.Projection("EPSG:4326"),
  	new OpenLayers.Projection("EPSG:900913")
      );
      waterfrontPointFeature = new OpenLayers.Feature.Vector(waterfrontPoint);
      waterfrontPointFeature.attributes = {
  	name : "BikeShare - Waterfront",
          favColor : 'red',
          align : 'cm',
          xOffset : 10,
          yOffset : 10,
          pointColor : 'blue'
      };
      features.push(waterfrontPointFeature);
      modaCenterPoint = new OpenLayers.Geometry.Point(-122.666639,45.530688);
      modaCenterPoint.transform(
  	new OpenLayers.Projection("EPSG:4326"),
  	new OpenLayers.Projection("EPSG:900913")
      );
      modaCenterPointFeature = new OpenLayers.Feature.Vector(modaCenterPoint);
      modaCenterPointFeature.attributes = {
          name : "BikeShare - Moda Center",
          favColor : 'red',
          align : 'cm',
          xOffset : 10,
          yOffset : 10,
          pointColor : 'blue'
      };
      features.push(modaCenterPointFeature);
      tramPoint = new OpenLayers.Geometry.Point(-122.671613,45.499209);
      tramPoint.transform(
  	new OpenLayers.Projection("EPSG:4326"),
  	new OpenLayers.Projection("EPSG:900913")
      );
      tramPointFeature = new OpenLayers.Feature.Vector(tramPoint);
      tramPointFeature.attributes = {
          name : "BikeShare - Tram",
          favColor : 'red',
          align : 'cm',
          xOffset : 10,
          yOffset : 10,
          pointColor : 'blue'
      };
      features.push(tramPointFeature); 
      map.addLayer(vectorLayer);
      vectorLayer.addFeatures(features);
      map.setCenter(lonlat, zoom);
}
function getRandomInt (min, max) {
  	return Math.floor(Math.random() * (max - min + 1)) + min;
}

function setRandomPointStuff() {
 	colors = ['red','yellow','blue'];
  var numFeatures = features.length;
  for (var i = 0; i< numFeatures; i ++) {
  	colorNum = getRandomInt(0,2);
  	features[i].attributes.pointColor = colors[colorNum];
  }
 vectorLayer.redraw();
}
 setInterval(function(){setRandomPointStuff()},15000);
