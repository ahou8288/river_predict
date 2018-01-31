var map;
var markers = [];
var windows = [];
var map_ready = false;

function bindClick(marker,infowindow){
    if (map_ready) {
    console.log(marker)
    console.log(infowindow)
        infowindow.open(map, marker);
    }
}


function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
    });
    
    var infowindow = new google.maps.InfoWindow();

    var contents = []
    
    for (var index = 0; index<points.length; index++){
        point = points[index]

        contents.push('<a href="section/view/'+point.slug+'"><div id="content">'+
            '<p>'+point.river+'</p>'+
            '<p>'+point.name+'</p>'+
            '</div></a>');

        marker = new google.maps.Marker({
            title: point.name,
            position: point,
            map: map,
        });
    
        google.maps.event.addListener(marker, 'click', (function (marker, index) {
            return function () {
                infowindow.setContent(contents[index]);
                infowindow.open(map, marker);
            }
        })(marker, index)); 
    }

    map_ready=true;
}