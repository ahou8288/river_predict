var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
    });
    var marker1 = new google.maps.Marker({
        label: 'Put in',
        position: put_in,
        map: map
    });
    var marker2 = new google.maps.Marker({
        label: 'Take out',
        position: take_out,
        map: map
    });

    var bounds = new google.maps.LatLngBounds();
    bounds.extend(marker2.getPosition());
    bounds.extend(marker1.getPosition());
    map.fitBounds(bounds);
}