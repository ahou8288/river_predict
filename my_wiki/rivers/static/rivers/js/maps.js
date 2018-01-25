var map;
var startMarker;
var endMarker;

function placeEnd(markerLocation = map.getCenter()) {
    // if any previous marker exists, let's first remove it from the map
    if (endMarker) {
        endMarker.setMap(null);
    }
    // create the marker
    endMarker = new google.maps.Marker({
        position: markerLocation,
        label: 'Take out',
        map: map,
        draggable: true,
    });

    fillMarkerForm(endMarker,'id_form-0-');
    google.maps.event.addListener(endMarker, 'dragend', function() {
        fillMarkerForm(endMarker,'id_form-0-');
    });
}

function placeStart(markerLocation = map.getCenter()){
    // if any previous marker exists, let's first remove it from the map
    if (startMarker) {
        startMarker.setMap(null);
    }
    // create the marker
    startMarker = new google.maps.Marker({
        position: markerLocation,
        label: 'Put in',
        map: map,
        draggable: true,
    });

    fillMarkerForm(startMarker,'id_form-1-');
    google.maps.event.addListener(startMarker, 'dragend', function() {
        fillMarkerForm(startMarker,'id_form-1-');
    });
}

function initialize() {
    var originLocation = new google.maps.LatLng(-33.865143, 151.209900); // Sydney
    var mapOptions = {
        zoom: 8,
        center: originLocation
    }
    map = new google.maps.Map(document.getElementById("map"), mapOptions);

    // Add controls to the map
    var buttonPutIn = document.createElement('div');
    var controlArgs = {
        'Take out': 'placeEnd',
        'Put in': 'placeStart',
    }

    var centerControl = new CenterControl(buttonPutIn, controlArgs);
    buttonPutIn.index = 1;
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(buttonPutIn);

    // Put points on the map
    var endFormData = getMarkerForm('id_form-0-');
    document.getElementById("id_form-0-point_type").selectedIndex = 0;
    if (endFormData.lat && endFormData.lng) {
        placeEnd(endFormData)
    }

    var startFormData = getMarkerForm('id_form-1-');
    document.getElementById("id_form-1-point_type").selectedIndex = 1;
    if (startFormData.lat && startFormData.lng) {
        placeStart(startFormData)
    }

    if (startFormData.lat && startFormData.lng && endFormData.lat && endFormData.lng){
        var bounds = new google.maps.LatLngBounds();
        bounds.extend(endMarker.getPosition());
        bounds.extend(startMarker.getPosition());
        map.fitBounds(bounds);
    }
}

google.maps.event.addDomListener(window, 'load', initialize);


function submitForm(){
    
    document.getElementById("formgrid").submit();
}

function fillMarkerForm(marker,id){
    if (marker){
        pos = marker.getPosition()
        document.getElementById(id+"latitude").value = pos.lat().toFixed(6)
        document.getElementById(id+"longditude").value = pos.lng().toFixed(6)
    }
}

function getMarkerForm(id){
    var latitude = parseFloat(document.getElementById(id+"latitude").value);
    var longditude = parseFloat(document.getElementById(id+"longditude").value);
    return {
        lat: latitude,
        lng:longditude
    };
}