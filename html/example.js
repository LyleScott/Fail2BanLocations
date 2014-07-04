function showInfoWindow(cluster) {
    if (cluster instanceof Cluster) {
        var markers = cluster.getMarkers();
        var center = cluster.getCenter();
    } else {
        var markers = [this];
        var center = this.getPosition();
    }

    var tbl = '<table cellspacing=0 cellpadding=0>';
    tbl += '<tr><th>&nbsp;</th><th>IP</th><th>Date</th></tr>';

    for (var i=0; i < markers.length; i++) {
        var data = markers[i].data;
        tbl += '<tr>';
        tbl += '<td>' + (i+1) + '</td>';
        tbl += '<td>' + data['ip'] + '</td>';
        tbl += '<td>' + data['date'] + '</td>';
        tbl += '</tr>';
    }

    tbl += '</table>';

    if (typeof infowindow != 'undefined') {
        infowindow.close();
    }

    infowindow = new google.maps.InfoWindow({
        content: tbl,
        position: center
    });

    infowindow.open(this.map);
}


function initmap() {
    var center = new google.maps.LatLng(0, 0);

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: center,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDoubleClickZoom: true,
        streetViewControl: false
    });

    google.maps.event.addListener(map, 'click', function() {
        if (typeof infowindow != 'undefined') {
            infowindow.close();
        }
    });
    google.maps.event.addListener(map, 'zoom_changed', function() {
        if (typeof infowindow != 'undefined') {
            infowindow.close();
        }
    });

    var markers = [];

    for (var i in locations) {
        var data = locations[i];

        var latLng = new google.maps.LatLng(
            data.latitude,
            data.longitude
        );

        var marker = new google.maps.Marker({
            position: latLng,
            data: data
        });

        google.maps.event.addListener(marker, 'click', showInfoWindow);

        markers.push(marker);
    }

    var markerCluster = new MarkerClusterer(map, markers, {
        zoomOnClick: false
    });

    google.maps.event.addListener(markerCluster, "click", showInfoWindow);
}

google.maps.event.addDomListener(window, 'load', initmap);