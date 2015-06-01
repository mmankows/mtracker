var markerCount = 0;	// global marker count
var LatLngCoords = [];
var map;		// google map
 
var totalDistance = 0;
// initialize document
window.onload = function () {
	// prepare login / logout
	if( getCookie('token') == undefined || getCookie('uid') == undefined ) {
		var login_el = document.getElementById('log');
		alert("musisz się zalogować!");
		window.location    = "../cgi/auth.cgi";
	}

	// prepare datetime fields
	var today = new Date();
	var month = today.getMonth() + 1; month = month > 9 ? month : "0" + month;
	var day   = today.getDate();      day   = day   > 9 ? day   : "0" + day;

	var today_date =  today.getFullYear() + "-" + month + "-" + day;
	document.getElementById('begin').value = today_date + " 00:00:00";
	document.getElementById('end').value   = today_date + " 23:59:59";


};
//Initializes the map…
function initialize() {
    LatLngCoords = [];
    markerCount = 0;
    totalDistance = 0;

    var myLatlng = new google.maps.LatLng(50, 20);
    var map_canvas = document.getElementById('map-canvas');
    var map_options = {
	center: myLatlng,
	zoom: 5,
    }
    map = new google.maps.Map(map_canvas, map_options);
}   
 
//When the window is loaded, run the initialize function to
//setup the map
google.maps.event.addDomListener(window, 'load', initialize);   
 
//This function will add a marker to the map each time it
//is called.  It takes latitude, longitude, and html markup
//for the content you want to appear in the info window
//for the marker.
function addMarkerToMap(lat, longi, htmlMarkupForInfoWindow){
    var infowindow = new google.maps.InfoWindow();
    var myLatLng = new google.maps.LatLng(lat, longi);
    var marker = new google.maps.Marker({
	position: myLatLng,
	map: map,
    });
     
    //Gives each marker an Id for the on click
    markerCount++;
 
    //Creates the event listener for clicking the marker
    //and places the marker on the map
    google.maps.event.addListener(marker, 'click', (function(marker, markerCount) {
	return function() {
	    infowindow.setContent(htmlMarkupForInfoWindow);
	    infowindow.open(map, marker);
	}
    })(marker, markerCount)); 
     
    //Pans map to the new location of the marker
    map.panTo(myLatLng)       
}

var start = 0;
function addMarkers() {
var xmlhttp;
if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
	xmlhttp=new XMLHttpRequest();
} else {// code for IE6, IE5
	xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}


xmlhttp.onreadystatechange=function() {

	if (xmlhttp.readyState==4 && xmlhttp.status==200) {
	    var Coords = JSON.parse(xmlhttp.responseText) || [];
	    
	    // do nothing if no markers to add
	    if( Coords.length == 0 ) {
		alert("No positions to display in given time range. Specify another time range");
	    	return false;
	    }
	    
	    // reload map
	    initialize();
            for ( var i=0; i<Coords.length; i++ ) {
		LatLngCoords[i] = new google.maps.LatLng(Coords[i].latitude, Coords[i].longitude);
		if( i > 0 ) {
			totalDistance += google.maps.geometry.spherical.computeDistanceBetween(LatLngCoords[i], LatLngCoords[i-1]);
		}
            }

	    // display markers with details //
      	    if(  disp_type == "MARKER" ) {
	        for(var i=0; i<Coords.length; i++) {
		   addMarkerToMap( Coords[i].latitude, Coords[i].longitude,
		   "<b>#" + i + "</b>" +
		   "<br/><b>time:</b>\t" + Coords[i].logdate + 
		   "<br/><b>lat:</b>\t"  + Coords[i].latitude + 
		   "<br/><b>lon:</b>\t"  + Coords[i].longitude );
	        }
            } else if ( disp_type == "ROUTE" ) {
	   	var tracked_route = new google.maps.Polyline({
			path: LatLngCoords,
			geodesic: true,
			strokeColor: '#FF0000',
			strokeOpacity: 1.0,
			strokeWeight: 2
		});
	    	tracked_route.setMap(map); 
	    }
	
	 
	    // Zoom in for all markers
	    var latlngbounds = new google.maps.LatLngBounds();
	 
	    LatLngCoords.forEach(function(n){
	    	latlngbounds.extend(n);
	    });
	    map.setZoom(17);
	    map.setCenter(latlngbounds.getCenter());
	    map.fitBounds(latlngbounds); 
	
	    // generate statistics
	    document.getElementById('modal_button').disabled = false;
	    var stats_el = document.getElementById('stats');
	    stats_el.innerHTML = "<b>długość trasy: </b>" + Math.round( totalDistance )+ " (m)<br>" +
	    			 "<b>liczba punktów: </b>" + Coords.length + "<br>" +  
	    		         "<b>początek trasy: </b>" + Coords[Coords.length-1].logdate + "<br>" +
				 "<b>koniec trasy:   </b>" + Coords[0].logdate + "<br>";
	}	
}

	var valid = true;
	var disp_type = document.getElementById('disp_type').value; 
	var uid       = getCookie('uid');
	var token     = getCookie('token');
	var cnt       = document.getElementById('cnt').value;

	var begin     = document.getElementById('begin').value;
	var end       = document.getElementById('end').value;

	// validate date
	if(  begin && !begin.match(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/ )) {
		alert("Invalid date format. Use 'YYYY-MM-DD HH:mm:ss'"); 
		valid = false;
	}
	
	if(  end && !end.match(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/)) {
		alert("Invalid date format. Use 'YYYY-MM-DD HH:mm:ss'"); 
		valid = false;
	}
	
	if( cnt && cnt < 0 ) {
		alert("Invalid number for positions number. Use positive only!");
		valid = false;
	}

	if( ! cnt  ) {
		alert("Provide number of positions to display!");
		valid = false;
	}


            
	if( valid == true && disp_type ) {
		xmlhttp.open("GET","../cgi/display.cgi?" 
				+  "uid="   + uid 
				+ "&t="     + token
				+ "&cnt="   + cnt 
				+ "&f="     +"json" 
				+ "&begin=" + begin 
				+ "&end="   + end,
		true);
		xmlhttp.send();
		start = 1;
	}

}
$(function(){
	$('#begin, #end').datetimepicker({
		format: 'YYYY-MM-DD HH:mm:ss'
	});
});
