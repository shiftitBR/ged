var initialLocation;
var brasil	= new google.maps.LatLng(10, 55);
var browserSupportFlag =  new Boolean();
var geocoder;
var map;

function initialize() {
  geocoder = new google.maps.Geocoder();
  var myOptions = {
    zoom: 10,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
  
  // Try W3C Geolocation (Preferred)
  if(navigator.geolocation) {
    browserSupportFlag = true;
    navigator.geolocation.getCurrentPosition(function(position) {
      initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
      map.setCenter(initialLocation);
    }, function() {
      handleNoGeolocation(browserSupportFlag);
    });
  // Try Google Gears Geolocation
  } else if (google.gears) {
    browserSupportFlag = true;
    var geo = google.gears.factory.create('beta.geolocation');
    geo.getCurrentPosition(function(position) {
      initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
      map.setCenter(initialLocation);
    }, function() {
      handleNoGeoLocation(browserSupportFlag);
    });
  // Browser doesn't support Geolocation
  } else {
    browserSupportFlag = false;
    handleNoGeolocation(browserSupportFlag);
  }
  
  function handleNoGeolocation(errorFlag) {
    if (errorFlag == true) {
      alert("O serviço de Geolocalização falhou.");
      initialLocation = brasil;
    } else {
      alert("Seu brownser não suporta o serviço de geolocalização.");
      initialLocation = brasil;
    }
    map.setCenter(initialLocation);
  }
   
}

$(document).ready
(
	function()
	{
		$('#map_canvas').change(initialize())
		$('#map_canvas').change(codeAddress('Lauro Linhares Trindade'))
	}
);

function codeAddress(iEndereco) {
	$.post('/enderecos/', { dir: 'teste' }, function(data)
    {
		var lista=data.split("%");
		var id;
		var endereco;
		var nome;
		for (var i = 0; i < lista.length; i++) 
		{
			id= lista[i]
			i++
			endereco= lista[i]
			i++
			nome= lista[i]
			codeAddress(id, endereco, nome);
		}
		
		function codeAddress(vId, vEndereco, vNome) {
		    geocoder.geocode( { 'address': vEndereco}, function(results, status) {
		      if (status == google.maps.GeocoderStatus.OK) {
		        map.setCenter(results[0].geometry.location);
		        var marker = new google.maps.Marker({
		            map: map,
		            position: results[0].geometry.location,
		            title:vNome
		        });
		        google.maps.event.addListener(marker, 'click', function() {
		        	window.location="/publico/"+ vId; 
		        });
		      } else {
		    	  alert("O Endereço: "+ address + ", Não foi encontrado!");
		      }
		    });
		  }
    });
  }
