var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
    });

    points
    for (index = 0; index<points.length; index++){
        point = points[index]
        marker = new google.maps.Marker({
            title: point.name,
            position: point,
            map: map,
            url: point.slug
        });
        google.maps.event.addListener(marker, 'click', function() {
            window.location.href = 'section/view/'+this.url;
        });
    }
}