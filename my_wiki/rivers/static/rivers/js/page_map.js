var map;
var markers = [];
var windows = [];
var map_ready = false;

function pinSymbol(color) {
    return {
        path: 'M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z M -2,-30 a 2,2 0 1,1 4,0 2,2 0 1,1 -4,0',
        fillColor: color,
        fillOpacity: 1,
        strokeColor: '#000',
        strokeWeight: 2,
        scale: 1,
   };
}

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
            icon: pinSymbol('hsl(215, 100%, 50%)'),
        });
    
        google.maps.event.addListener(marker, 'click', (function (marker, index) {
            return function () {
                infowindow.setContent(contents[index]);
                infowindow.open(map, marker);
            }
        })(marker, index)); 
    }

    google.maps.event.addListener(map, "click", function(event) {
        infowindow.close();
    });

    map_ready=true;
}