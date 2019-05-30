/**
 * place a marker representing a food truck in the @map at the
 * location specified in the @truck attributes.
 * @param  {google.maps.Map} map a Google Maps API Map object
 * @param  {dict} truck a dict object for a food truck, containing key-value pairs for each JSON field
 * @return {google.maps.Marker} a Google Maps API Marker object for the food truck
 */
function placeFoodTruckMarker(map, truck) {
    var pos = new google.maps.LatLng(truck.latitude, truck.longitude);  

    var contentString = '<div id="content">'+
        '<div id="siteNotice">'+
        '</div>'+
        `<h1 id="firstHeading" class="firstHeading">${truck.name}</h1>`+
        '<div id="bodyContent">'+
        '<ul>'+
        `<li>latitude: ${truck.latitude}</li>`+
        `<li>longitude: ${truck.longitude}</li>`+
        `<li>menu: ${truck.food_items}</li>`+
        `<li>hours: ${truck.days_hours}</li>`+
        '</ul>'+
        '</div>'+
        '</div>';

    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });
    
    var truckMarker = new google.maps.Marker({
        position: pos,
        map: map,
        animation: google.maps.Animation.DROP,
        title: truck.name,
        icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
    });

    truckMarker.addListener('mouseover', function() {
        infowindow.open(map, truckMarker);
    });

    truckMarker.addListener('mouseout', function() {
        infowindow.close();
    });
    
    return truckMarker;
}

/**
 * requests the food trucks nearby a location and places markers in the @map
 * for every returned truck.
 * @param  {google.maps.Map} map a Google Maps API Map object
 * @param  {array} truckMarkers an array of markers currently placed in @map
 * @param  {google.maps.LatLng} location a Google Maps API LatLng object representing a coordinate
 * @param  {number} radius the search radius in m
 * @param  {string} nameNeedle the name substring to filter results by
 * @param  {string} itemsNeedle the items substring to filter results by
 * @return {array} the array of newly placed markers in @map
 */
function placeNearbyTrucks(map, truckMarkers, location, radius, nameNeedle, itemsNeedle) {
    // remove current markers
    for (var i = 0; i < truckMarkers.length; i++) {
        truckMarkers[i].setMap(null);
    };
    truckMarkers = [];

    // get latitude and longitude
    var lat = location.lat();
    var lng = location.lng();

    // prepare REST API request to get nearby food trucks
    var pathArray = window.location.href.split( '/' );
    var protocol = pathArray[0];
    var host = pathArray[2];
    var rootUrl = protocol + '//' + host;
    var url = `${rootUrl}/foodtrucks/location?latitude=${lat}&longitude=${lng}&radius=${radius}`;
    if (nameNeedle != null) {
        url += `&name=${nameNeedle}`;
    }
    if (itemsNeedle != null) {
        url += `&item=${itemsNeedle}`;
    }
    
    // request food trucks and place a marker for each
    $.getJSON(url, function(result){
        $.each(result.foodtrucks, function(i, truck){  
            truckMarkers.push(placeFoodTruckMarker(map, truck))
        });
    });
    return truckMarkers;
}

/**
 * places or updates a marker for the current location in @map
 * @param  {google.maps.Map} map a Google Maps API Map object
 * @param  {google.maps.Marker} marker Google Maps API Marker for the current location
 * @param  {google.maps.LatLng} location a Google Maps API LatLng object representing a coordinate
 * @return {google.maps.Marker} the updated marker
 */
function placeMarker(map, marker, location){
    // if current location marker does not exist it is created
    if (marker == null){
        marker = new google.maps.Marker({
            position: location,
            map: map,
            animation: google.maps.Animation.DROP,
            title: 'Current location'
        });
    // else it is updated
    } else {
        marker.setPosition(location);
    }

    // center the map in the new location
    map.panTo(location);

    return marker;
}

/**
 * initializes the Google Maps Javascript API map
 */
function initMap() {
    // initialize variables
    var location = new google.maps.LatLng(37.7557, -122.4421);
    var truckMarkers = [];
    var radius = 500;
    var marker;
    var nameNeedle;
    var itemsNeedle;

    // configure map options
    var mapOptions = {
        zoom: 13,
        center: location,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        streetViewControl: false,
        mapTypeControl: false,
    };

    // configure search radius slider callbacks
    var slider = document.getElementById("radiusRange");
    var radiusTextbox = document.getElementById("radius-input");
    slider.oninput = function() {
      radius = this.value;
      radiusTextbox.value = radius;
    };
    slider.onchange = function() {
        truckMarkers = placeNearbyTrucks(map, truckMarkers, location, radius, nameNeedle, itemsNeedle);
    }

    // configure search radius input text box callbacks
    radiusTextbox.oninput = function() {
        radius = this.value;
        slider.value = radius;
    };
    radiusTextbox.onchange = function() {
        truckMarkers = placeNearbyTrucks(map, truckMarkers, location, radius, nameNeedle, itemsNeedle);
    }

    // configure name filter input text box callbacks
    var nameTextbox = document.getElementById("name-input");
    nameTextbox.onchange = function() {
        nameNeedle = this.value;
        truckMarkers = placeNearbyTrucks(map, truckMarkers, location, radius, nameNeedle, itemsNeedle);
    }

    // configure items filter input text box callbacks
    var itemsTextbox = document.getElementById("items-input");
    itemsTextbox.onchange = function() {
        itemsNeedle = this.value;
        truckMarkers = placeNearbyTrucks(map, truckMarkers, location, radius, nameNeedle, itemsNeedle);
    }

    // initialize the map
    var map = new google.maps.Map(document.getElementById("map"),
        mapOptions);
    
    // move the map and markers when a new location is clicked
    google.maps.event.addListener(map, 'click', function(event) {   
        location = event.latLng; 
        marker = placeMarker(map, marker, location);
        truckMarkers = placeNearbyTrucks(map, truckMarkers, location, radius, nameNeedle, itemsNeedle);
    });
}