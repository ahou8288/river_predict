
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;
var startMarker;
var endMarker;

function initialize() {
  directionsDisplay = new google.maps.DirectionsRenderer();
  var origin_location = new google.maps.LatLng(-33.865143, 151.209900); // Sydney
  var mapOptions = {
    zoom: 8,
    center: origin_location
  }
  map = new google.maps.Map(document.getElementById("map"), mapOptions);
  directionsDisplay.setMap(map);
}

function place_end() {
  // if any previous marker exists, let's first remove it from the map
  if (endMarker) {
    endMarker.setMap(null);
  }
  // create the marker
  endMarker = new google.maps.Marker({
    position: map.getCenter(),
    label: 'Take out',
    map: map,
    draggable: true,
  });

  copyMarkerpositionToInput();
  // add an event "onDrag"
  google.maps.event.addListener(endMarker, 'dragend', function() {
    copyMarkerpositionToInput(endMarker);
  });
}

function place_start(){
  // if any previous marker exists, let's first remove it from the map
  if (startMarker) {
    startMarker.setMap(null);
  }
  // create the marker
  startMarker = new google.maps.Marker({
    position: map.getCenter(),
    label: 'Put in',
    map: map,
    draggable: true,
  });

  copyMarkerpositionToInput();
  // add an event "onDrag"
  google.maps.event.addListener(startMarker, 'dragend', function() {
    copyMarkerpositionToInput(startMarker);
  });
}


function copyMarkerpositionToInput(marker) {
  // get the position of the marker, and set it as the value of input
  // document.getElementById("end").value = marker.getPosition().lat() +','+  marker.getPosition().lng();
}

google.maps.event.addDomListener(window, 'load', initialize);