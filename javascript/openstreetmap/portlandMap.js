var pointFeature;
var map;
var map1;
var stationLayer;
var bikeLayer;
var decisionLayer;
var featuresToStationIds = []
var features = []
var routePoint = 0;
var bikeFeature;
var riderFeatures = {};
var stationFeatures = {};
var osmUrl = "http://bikeshare.cs.pdx.edu/osm";
var iconUrl = "http://localhost/static/ic_launcher32.png";
var apiUrl = "http://api.bikeshare.cs.pdx.edu";
var decisionLatLong = [
    [-122.677116394043,45.514647367543],
    [-122.645616531372,45.5166922220549],
    [-122.68123626709,45.5266748564834],
    [-122.661924362183,45.519639087554]
];
function init() {
    map = new OpenLayers.Map("mapdiv");
    //switch between local and remote tiles
    var tileLayer = new OpenLayers.Layer.OSM("Local Tiles", osmUrl + "/${z}/${x}/${y}.png", {numZoomLevels: 19, crossOriginKeyword: null});
    map.addLayer(tileLayer); 
    var renderer = OpenLayers.Util.getParameters(window.location.href).renderer;
    renderer = (renderer) ? [renderer] : OpenLayers.Layer.Vector.prototype.renderers;
    var layer_style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
    layer_style.fillOpacity = 0.2;
    layer_style.graphicOpacity = 1;
    var lonlat = new OpenLayers.LonLat(-122.653534,45.522912).transform(
        new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
        new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator
      );
    stationLayer = new OpenLayers.Layer.Vector("Simple Geometry", {
        styleMap: new OpenLayers.StyleMap({'default':{
            strokeColor: "${pointColor}",
            strokeOpacity: 1,
            strokeWidth: 3,
            fillColor: "${pointColor}",
            fillOpacity: 0.8,
            pointRadius: 5,
            pointerEvents: "visiblePainted",
            label : "${name}",
            fontColor: "black",
            fontSize: "14px",
            fontFamily: "Courier New, monospace",
            fontWeight: "bold",
            labelAlign: "${align}",
            labelXOffset: "${xOffset}",
            labelYOffset: "${yOffset}"
        }}),
        renderers: renderer
    });
    stationLayer.events.register("featuresadded", stationLayer, function() {
        stationLayer.redraw();
    });
    map.addLayer(stationLayer);

    decisionLayer = new OpenLayers.Layer.Vector("decisionPoints", {
        styleMap: new OpenLayers.StyleMap({'default':{
            strokeColor: "black",
            strokeOpacity: 1,
            strokeWidth: 3,
            fillColor: "black",
            fillOpacity: 1,
            pointRadius: 3,
            pointerEvents: "visiblePainted",
            fontColor: "black",
            fontSize: "14px",
        }}),
        renderers: renderer
    });
   for (var i = 0; i < decisionLatLong.length; i ++) {
        var decisionPoint = new OpenLayers.Geometry.Point(decisionLatLong[i][0],decisionLatLong[i][1]);
        decisionPoint.transform(
             new OpenLayers.Projection("EPSG:4326"),
             new OpenLayers.Projection("EPSG:900913")
        );
        decisionPointFeature = new OpenLayers.Feature.Vector(decisionPoint);
        decisionPointFeature.attributes = {
            favColor : 'black',
            align : 'cm',
            xOffset : 10,
            yOffset : 10,
            pointColor : 'black'
        };
        decisionLayer.addFeatures([decisionPointFeature]);
    }
    map.addLayer(decisionLayer);
    var zoom = 13;
      map.setCenter(lonlat, zoom); 
      bikeLayer = new OpenLayers.Layer.Vector("bikeLayer", {
          style : {
              externalGraphic : iconUrl,
              graphicWidth: 21,
              graphicHeight: 25
          }
    });
    map.addLayer(bikeLayer);
     var highlightCtrl = new OpenLayers.Control.SelectFeature(stationLayer, {
                hover: true,
                eventListeners: {
                    featurehighlighted: featureHighlighted,
                    featureunhighlighted: featureUnhighlighted 
        }
     });
    
    map.addControl(highlightCtrl);
    highlightCtrl.activate();
    map.setCenter(lonlat, zoom);
    createBikeshareStationFeatures();
    createRiderFeatures();
}

/*
var stationLayer1;
var bikeLayer1;
var decisionLayer1;
var featuresToStationIds1 = []
var features1 = []
var routePoint1 = 0;
var bikeFeature1;
var riderFeatures1 = {};
var stationFeatures1 = {};

function initone() {
    map1 = new OpenLayers.Map("mapdiv1");
    //switch between local and remote tiles
    var tileLayer = new OpenLayers.Layer.OSM("Local Tiles", osmUrl + "/${z}/${x}/${y}.png", {numZoomLevels: 19, crossOriginKeyword: null});
    map1.addLayer(tileLayer); 
    var renderer = OpenLayers.Util.getParameters(window.location.href).renderer;
    renderer = (renderer) ? [renderer] : OpenLayers.Layer.Vector.prototype.renderers;
    var layer_style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
    layer_style.fillOpacity = 0.2;
    layer_style.graphicOpacity = 1;
    var lonlat = new OpenLayers.LonLat(-122.653534,45.522912).transform(
        new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
        new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator
      );
    stationLayer1 = new OpenLayers.Layer.Vector("Simple Geometry", {
        styleMap: new OpenLayers.StyleMap({'default':{
            strokeColor: "${pointColor}",
            strokeOpacity: 1,
            strokeWidth: 3,
            fillColor: "${pointColor}",
            fillOpacity: 0.8,
            pointRadius: 5,
            pointerEvents: "visiblePainted",
            label : "${name}",
            fontColor: "black",
            fontSize: "14px",
            fontFamily: "Courier New, monospace",
            fontWeight: "bold",
            labelAlign: "${align}",
            labelXOffset: "${xOffset}",
            labelYOffset: "${yOffset}"
        }}),
        renderers: renderer
    });
    stationLayer1.events.register("featuresadded", stationLayer1, function() {
        stationLayer1.redraw();
    });
    map1.addLayer(stationLayer1);

    decisionLayer1 = new OpenLayers.Layer.Vector("decisionPoints", {
        styleMap: new OpenLayers.StyleMap({'default':{
            strokeColor: "black",
            strokeOpacity: 1,
            strokeWidth: 3,
            fillColor: "black",
            fillOpacity: 1,
            pointRadius: 3,
            pointerEvents: "visiblePainted",
            fontColor: "black",
            fontSize: "14px",
        }}),
        renderers: renderer
    });
   for (var i = 0; i < decisionLatLong.length; i ++) {
        var decisionPoint = new OpenLayers.Geometry.Point(decisionLatLong[i][0],decisionLatLong[i][1]);
        decisionPoint.transform(
             new OpenLayers.Projection("EPSG:4326"),
             new OpenLayers.Projection("EPSG:900913")
        );
        decisionPointFeature = new OpenLayers.Feature.Vector(decisionPoint);
        decisionPointFeature.attributes = {
            favColor : 'black',
            align : 'cm',
            xOffset : 10,
            yOffset : 10,
            pointColor : 'black'
        };
        decisionLayer1.addFeatures([decisionPointFeature]);
    }
    map1.addLayer(decisionLayer1);
    var zoom = 13;
      map1.setCenter(lonlat, zoom); 
      bikeLayer1 = new OpenLayers.Layer.Vector("bikeLayer1", {
          style : {
              externalGraphic : iconUrl,
              graphicWidth: 21,
              graphicHeight: 25
          }
    });
    map1.addLayer(bikeLayer1);
     var highlightCtrl1 = new OpenLayers.Control.SelectFeature(stationLayer1, {
                hover: true,
                eventListeners: {
                    featurehighlighted1: featureHighlighted1,
                    featureunhighlighted1: featureUnhighlighted1
        }
     });
    
    map1.addControl(highlightCtrl1);
    highlightCtrl1.activate();
    map1.setCenter(lonlat, zoom);
    createBikeshareStationFeatures1();
    createRiderFeatures1();
}
*/

function createBikeFeatures() {
    var bikePoint = new OpenLayers.Geometry.Point(route[0][0],route[0][1]);
    //var bikePoint1 = new OpenLayers.Geometry.Point(route[0][0],route[0][1]);
    bikePoint.transform(
        new OpenLayers.Projection("EPSG:4326"),
        new OpenLayers.Projection("EPSG:900913")
    );
    /*bikePoint1.transform(
        new OpenLayers.Projection("EPSG:4326"),
        new OpenLayers.Projection("EPSG:900913")
    );*/
    bikeFeature = new OpenLayers.Feature.Vector(bikePoint);
    //bikeFeature1 = new OpenLayers.Feature.Vector(bikePoint1);
    bikeLayer.addFeatures([bikeFeature]);
    //bikeLayer1.addFeatures([bikeFeature1]);
}

function createRiderFeatures() {
    $.ajax({url :  apiUrl + "/REST/1.0/bikes/active",
        success : function(result) {
            createRiderPoints(result['bikes']);
        }
    });
}

/*
function createRiderFeatures1() {
    $.ajax({url :  apiUrl + "/REST/1.0/bikes/active",
        success : function(result) {
            createRiderPoints(result['bikes']);
        }
    });
}
*/

function createRiderPoints(rider_locations) {
    for (var i = 0; i < rider_locations.length; i ++ ) {
        var bikePoint = new OpenLayers.Geometry.Point(rider_locations[i]['LONGITUDE'],rider_locations[i]['LATITUDE']);
        //var bikePoint1 = new OpenLayers.Geometry.Point(rider_locations[i]['LONGITUDE'],rider_locations[i]['LATITUDE']);
        bikePoint.transform(
            new OpenLayers.Projection("EPSG:4326"),
            new OpenLayers.Projection("EPSG:900913")
        );
        /*bikePoint1.transform(
            new OpenLayers.Projection("EPSG:4326"),
            new OpenLayers.Projection("EPSG:900913")
        );*/
        riderFeatures[rider_locations[i]['USER_ID']] = new OpenLayers.Feature.Vector(bikePoint);
        //riderFeatures1[rider_locations[i]['USER_ID']] = new OpenLayers.Feature.Vector(bikePoint1);
        bikeLayer.addFeatures([riderFeatures[rider_locations[i]['USER_ID']]]);
        //bikeLayer1.addFeatures([riderFeatures1[rider_locations[i]['USER_ID']]]);
    }
    bikeLayer.redraw();
    //bikeLayer1.redraw();
}
function getBikestationData() {
    for (var i = 0; i < featuresToStationIds.length; i ++) {
       $.ajax({ url : apiUrl + "/REST/1.0/stations/info/" + featuresToStationIds[i],
            crossDomain : true,
            success : function(result) {
                stationData = JSON.parse(result);
                setStationColor(this.stationFeatureId,stationData);  
                return;          
            },
            stationFeatureId : i
       });
    }
    /*for (var i = 0; i < featuresToStationIds1.length; i ++) {
       $.ajax({ url : apiUrl + "/REST/1.0/stations/info/" + featuresToStationIds1[i],
            crossDomain : true,
            success : function(result) {
                stationData = JSON.parse(result);
                setStationColor(this.stationFeatureId,stationData);  
                return;          
            },
            stationFeatureId : i
       });
    }*/
    stationLayer.redraw();
    //stationLayer1.redraw();
}

function setStationColor(stationNum,stationData) {
    bikePercent = (stationData.num_bikes / stationData.num_docks) * 100;
    if (bikePercent >= 50) {
        features[stationNum].attributes.pointColor = 'blue';
        //features1[stationNum].attributes.pointColor = 'blue';
    } else if (50 > bikePercent >= 25) {
        features[stationNum].attributes.pointColor = 'yellow';
        //features1[stationNum].attributes.pointColor = 'yellow';
    } else {
        features[stationNum].attributes.pointColor = 'red';
        //features1[stationNum].attributes.pointColor = 'red';
    }
}
function getRandomInt (min, max) {
  	return Math.floor(Math.random() * (max - min + 1)) + min;
}


function getRiderData() {
    $.ajax({url :  apiUrl +  "/REST/1.0/bikes/active",
        crossDomain : true,
        success : function(result) {
            updateRiderPoints(result['bikes']);
        }
    });
}

function updateRiderPoints(rider_locations) {
    bikeLayer.removeFeatures(bikeLayer.features);
    //bikeLayer1.removeFeatures(bikeLayer1.features);
    for (var i = 0; i < rider_locations.length; i ++ ) {
        var bikePoint = new OpenLayers.Geometry.Point(rider_locations[i]['LONGITUDE'],rider_locations[i]['LATITUDE']);
        //var bikePoint1 = new OpenLayers.Geometry.Point(rider_locations[i]['LONGITUDE'],rider_locations[i]['LATITUDE']);
        bikePoint.transform(
            new OpenLayers.Projection("EPSG:4326"),
            new OpenLayers.Projection("EPSG:900913")
        );
        /*bikePoint1.transform(
            new OpenLayers.Projection("EPSG:4326"),
            new OpenLayers.Projection("EPSG:900913")
        );*/
        if (rider_locations[i]['USER_ID'] in riderFeatures) {
            riderFeatures[rider_locations[i]['USER_ID']].geometry = bikePoint;
        } else {
            riderFeatures[rider_locations[i]['USER_ID']] = new OpenLayers.Feature.Vector(bikePoint);
        }
        /*if (rider_locations[i]['USER_ID'] in riderFeatures1) {
            riderFeatures1[rider_locations[i]['USER_ID']].geometry = bikePoint1;
        } else {
            riderFeatures1[rider_locations[i]['USER_ID']] = new OpenLayers.Feature.Vector(bikePoint1);
        }*/
        bikeLayer.addFeatures([riderFeatures[rider_locations[i]['USER_ID']]]);
        //bikeLayer1.addFeatures([riderFeatures1[rider_locations[i]['USER_ID']]]);
    }
    bikeLayer.redraw();
    //bikeLayer1.redraw();
}


function featureHighlighted(feature) {
    var popupIndex = getPopupIndex(feature.feature.attributes.popup);
    map.popups[popupIndex].show();
}

/*
function featureHighlighted1(feature) {
    var popupIndex1 = getPopupIndex(feature.feature.attributes.popup);
    map1.popups[popupIndex1].show();
}
*/

function featureUnhighlighted(feature) {
    var popupIndex = getPopupIndex(feature.feature.attributes.popup);
    map.popups[popupIndex].hide(); 
}

/*
function featureUnhighlighted1(feature) {
    var popupIndex1 = getPopupIndex(feature.feature.attributes.popup);
    map1.popups[popupIndex1].hide(); 
}
*/

function createBikeshareStationFeatures() {
    $.ajax({url : apiUrl + "/REST/1.0/stations/all",
    crossDomain : true,
    success: function(result) {
        bikeStationList = result['stations'];
        for (var i = 0; i < bikeStationList.length; i ++) {
            $.ajax({url : apiUrl + "/REST/1.0/stations/info/" + bikeStationList[i].STATION_ID,
            crossDomain: true,
            success: function(result) {
                        stationData = result;
                        createStationFeature(this.lon,this.lat,this.stationName,stationData.CURRENT_BIKES,stationData.CURRENT_DOCKS,this.stationIndex,this.stationId);
                    },
                    stationName : bikeStationList[i].STATION_NAME, 
                    lat : bikeStationList[i].LATITUDE, 
                    lon: bikeStationList[i].LONGITUDE,
                    stationIndex : i,
                    stationId : bikeStationList[i].STATION_ID
            });
        }
     }
   });
}

/*
function createBikeshareStationFeatures1() {
    $.ajax({url : apiUrl + "/REST/1.0/stations/all",
    crossDomain : true,
    success: function(result) {
        bikeStationList = result['stations'];
        for (var i = 0; i < bikeStationList.length; i ++) {
            $.ajax({url : apiUrl + "/REST/1.0/stations/info/" + bikeStationList[i].STATION_ID,
            crossDomain: true,
            success: function(result) {
                        stationData = result;
                        createStationFeature1(this.lon,this.lat,this.stationName,stationData.CURRENT_BIKES,stationData.CURRENT_DOCKS,this.stationIndex,this.stationId);
                    },
                    stationName : bikeStationList[i].STATION_NAME, 
                    lat : bikeStationList[i].LATITUDE, 
                    lon: bikeStationList[i].LONGITUDE,
                    stationIndex : i,
                    stationId : bikeStationList[i].STATION_ID
            });
        }
     }
   });
}
*/

function createStationFeature(lon,lat,stationName,bikes,docks,index,stationId) {
   var bikePercent = (bikes/docks) * 100;
   var pointColor;
   if (bikePercent > 50) {
        pointColor = 'blue';
   } else if (50 > bikePercent >= 25) {
        pointColor = 'yellow';
   } else {
        pointColor = 'red';
   }
   var stationPoint = new OpenLayers.Geometry.Point(lon,lat);
   stationPoint.transform(
        new OpenLayers.Projection("EPSG:4326"),
        new OpenLayers.Projection("EPSG:900913")
   );
   pointFeature = new OpenLayers.Feature.Vector(stationPoint);
   pointFeature.attributes = {
       name : stationName,
       favColor : 'black',
       align : 'cm',
       xOffset : 10,
       yOffset : 10,
       pointColor : pointColor,
       stationId : stationId,
       index: index,
       lat : lat,
       lon : lon
   };
   pointFeature.attributes.popup = new OpenLayers.Popup.FramedCloud("Popup" + stationName,
        stationPoint.getBounds().getCenterLonLat(), null,
        stationName + '</br>Bikes ' + bikes + '</br>Docks ' + docks,
        null,
        false
   );
   pointFeature.attributes.popup.panMapIfOutOfView = false;
   stationFeatures[stationId] = pointFeature;
   //stationFeatures1[stationId] = pointFeature;
   stationLayer.addFeatures(stationFeatures[stationId]);
   //stationLayer1.addFeatures(stationFeatures1[stationId]);
   map.addPopup(pointFeature.attributes.popup);
   for (var j = 0; j < map.popups.length; j ++) {
        map.popups[j].hide();
   }
   /*map1.addPopup(pointFeature.attributes.popup);
   for (var j = 0; j < map1.popups.length; j ++) {
        map1.popups[j].hide();
   }*/
}

/*
function createStationFeature1(lon,lat,stationName,bikes,docks,index,stationId) {
   var bikePercent = (bikes/docks) * 100;
   var pointColor;
   if (bikePercent > 50) {
        pointColor = 'blue';
   } else if (50 > bikePercent >= 25) {
        pointColor = 'yellow';
   } else {
        pointColor = 'red';
   }
   var stationPoint = new OpenLayers.Geometry.Point(lon,lat);
   stationPoint.transform(
        new OpenLayers.Projection("EPSG:4326"),
        new OpenLayers.Projection("EPSG:900913")
   );
   pointFeature = new OpenLayers.Feature.Vector(stationPoint);
   pointFeature.attributes = {
       name : stationName,
       favColor : 'black',
       align : 'cm',
       xOffset : 10,
       yOffset : 10,
       pointColor : pointColor,
       stationId : stationId,
       index: index,
       lat : lat,
       lon : lon
   };
   pointFeature.attributes.popup = new OpenLayers.Popup.FramedCloud("Popup" + stationName,
        stationPoint.getBounds().getCenterLonLat(), null,
        stationName + '</br>Bikes ' + bikes + '</br>Docks ' + docks,
        null,
        false
   );
   pointFeature.attributes.popup.panMapIfOutOfView = false;
   //stationFeatures[stationId] = pointFeature;
   stationFeatures1[stationId] = pointFeature;
   //stationLayer.addFeatures(stationFeatures[stationId]);
   stationLayer1.addFeatures(stationFeatures1[stationId]);
   /*map.addPopup(pointFeature.attributes.popup);
   for (var j = 0; j < map.popups.length; j ++) {
        map.popups[j].hide();
   }
   map1.addPopup(pointFeature.attributes.popup);
   for (var j = 0; j < map1.popups.length; j ++) {
        map1.popups[j].hide();
   }
}
*/


function updateBikestationData() {
    for (var featureId in stationFeatures) {
        $.ajax({url : apiUrl + "/REST/1.0/stations/info/" + featureId,
            success : function(results) {
                 stationData = results;
                 updateStationFeature(this.featureId,stationData);
                },
                featureId : featureId
            });
    }
    /*for (var featureId in stationFeatures1) {
        $.ajax({url : apiUrl + "/REST/1.0/stations/info/" + featureId,
            success : function(results) {
                 stationData = results;
                 updateStationFeature(this.featureId,stationData);
                },
                featureId : featureId
            });
    }*/
    stationLayer.redraw();
    //stationLayer1.redraw();
}

/*
function updateBikestationData1() {
    for (var featureId in stationFeatures) {
        $.ajax({url : apiUrl + "/REST/1.0/stations/info/" + featureId,
            success : function(results) {
                 stationData = results;
                 updateStationFeature(this.featureId,stationData);
                },
                featureId : featureId
            });
    }
    for (var featureId in stationFeatures1) {
        $.ajax({url : apiUrl + "/REST/1.0/stations/info/" + featureId,
            success : function(results) {
                 stationData = results;
                 updateStationFeature(this.featureId,stationData);
                },
                featureId : featureId
            });
    }
    //stationLayer.redraw();
    stationLayer1.redraw();
}
*/

function updateStationFeature(stationId,stationData) {
    var bikePercent = (stationData.CURRENT_BIKES/stationData.CURRENT_DOCKS) * 100;
    var pointColor;
    if (bikePercent > 50) {
        pointColor = 'blue';
    } else if ( 50 > bikePercent >= 25) {
        pointColor = 'yellow';
    } else {
        pointColor = 'red';
    }
    stationFeatures[stationId].attributes.pointColor = pointColor;
    //stationFeatures1[stationId].attributes.pointColor = pointColor;
    var stationPoint = new OpenLayers.Geometry.Point(stationFeatures[stationId].attributes.lon,stationFeatures[stationId].attributes.lat);
    //var stationPoint1 = new OpenLayers.Geometry.Point(stationFeatures1[stationId].attributes.lon,stationFeatures1[stationId].attributes.lat);
    stationPoint.transform(
         new OpenLayers.Projection("EPSG:4326"),
         new OpenLayers.Projection("EPSG:900913")
    );

    popupIndex = getPopupIndex(stationFeatures[stationId].attributes.popup);
    //popupIndex = getPopupIndex(stationFeatures1[stationId].attributes.popup);
    if (stationData['CURRENT_DISCOUNT'] > 0 ) {
        map.popups[popupIndex].setContentHTML('Station ' + stationFeatures[stationId].attributes.name + '</br>Bikes ' + stationData['CURRENT_BIKES'] + '</br>Docks ' + stationData['CURRENT_DOCKS'] + '</br>Discounts ' + stationData['CURRENT_DISCOUNT']);
        //map1.popups[popupIndex].setContentHTML('Station ' + stationFeatures1[stationId].attributes.name + '</br>Bikes ' + stationData['CURRENT_BIKES'] + '</br>Docks ' + stationData['CURRENT_DOCKS'] + '</br>Discounts ' + stationData['CURRENT_DISCOUNT']);
    } else {
        map.popups[popupIndex].setContentHTML('Station ' + stationFeatures[stationId].attributes.name + '</br>Bikes ' + stationData['CURRENT_BIKES'] + '</br>Docks ' + stationData['CURRENT_DOCKS']);
        //map1.popups[popupIndex].setContentHTML('Station ' + stationFeatures1[stationId].attributes.name + '</br>Bikes ' + stationData['CURRENT_BIKES'] + '</br>Docks ' + stationData['CURRENT_DOCKS']);
    }
    pointFeature.attributes.popup.panMapIfOutOfView = false;  
    stationLayer.removeFeatures([stationFeatures[stationId]]);
    stationLayer.addFeatures([stationFeatures[stationId]]);
    //stationLayer1.removeFeatures([stationFeatures1[stationId]]);
    //stationLayer1.addFeatures([stationFeatures1[stationId]]);
}


function getPopupIndex(popup) {
    popupIdx = -1;
    for (var i = 0; i < map.popups.length; i ++) {
        if (popup.id == map.popups[i].id) {
            popupIdx = i;
        }
    }
    /*for (var i = 0; i < map1.popups.length; i ++) {
        if (popup.id == map1.popups[i].id) {
            popupIdx = i;
        }
    }*/
    return popupIdx;
}
setInterval(function(){updateBikestationData()},1000);
//setInterval(function(){updateBikestationData1()},1000);
setInterval(function(){getRiderData()},1000);
