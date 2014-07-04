var infowindow;

function showInfoWindow(cluster) {
    var markers, center;

    if (cluster instanceof Cluster) {
        markers = cluster.getMarkers(),
        center = cluster.getCenter();
    } else {
        markers = [this];
        center = this.getPosition();
    }

    var tbl = '<table cellspacing="0" cellpadding="0" width="98%">' +
              '  <tr>' +
              '    <th>&nbsp;</th>' +
              '    <th>IP</th>' +
              '    <th>City</th>' +
              '    <th>Country</th>' +
              '    <th>Service</th>' +
              '    <th>Source</th>' +
              '    <th>Dates</th>' +
              '</tr>';

    for (var i = 0; i < markers.length; i++) {
        var data = markers[i].data;

        tbl += '<tr>' +
               '  <td>' + (i + 1) + '</td>' +
               '  <td>' + data['ip'] + '</td>' +
               '  <td>' + (data['city'] || '&nbsp;') + '</td>' +
               '  <td>' + data['country_name'] + '</td>' +
               '  <td>' + data['service'] + '</td>' +
               '  <td>' + data['source'] + '</td>' +
               '  <td>' + data['dates'].join('<br>') + '</td>' +
               '</tr>';
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


function build_markers() {
    var markers = [];

    for (var i = 0; i < locations.length; i++) {
        var data = locations[i],
            marker = new google.maps.Marker({
                position: new google.maps.LatLng(data.latitude, data.longitude),
                data: data
            });

        google.maps.event.addListener(marker, 'click', showInfoWindow);
        markers.push(marker);
    }

    return markers;
}


function initmap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: new google.maps.LatLng(0, 0),
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

    var markers = build_markers(),
        markerCluster = new MarkerClusterer(map, markers, {
            zoomOnClick: false
        });

    google.maps.event.addListener(markerCluster, "click", showInfoWindow);
}

google.maps.event.addDomListener(window, 'load', initmap);