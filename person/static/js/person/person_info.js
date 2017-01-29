
$(document).ready(function(){
	var child_count = 0;
	var alternate_count=0;	
	
	/* Datepicker */	
	$(function() {
		$( "#datepicker" ).datepicker({changeMonth: false, changeYear: true, yearRange: '1950:2100'})	
		$( "#spouse_datepicker" ).datepicker({changeMonth: false, changeYear: true, yearRange: '1950:2100'});
	});

	/* Graduation Year Selector */
	for (i = new Date().getFullYear(); i > 1900; i--){
		$('#yearpicker').append($('<option />').val(i).html(i));
		$('#spouse_yearpicker').append($('<option />').val(i).html(i));
		$('.child_yearpicker').append($('<option />').val(i).html(i));
	}



	/* Address Picker Code */
	$(".map-wrapper1").css("display","none");
	$(".map-wrapper2").css("display","none");
	$(".map-wrapper3").css("display","none");
	$(".map-wrapper4").css("display","none");

	
	/* MAP 1*/
	$(".addresspicker_map1").focus(function(){
		$(".map-wrapper1").css("display","block");
		$(function() {
			var addresspickerMap = $( ".addresspicker_map1" ).addresspicker({
				regionBias: "fr",
				elements: {
					map:"#map1",
					lat:      "#lat",
					lng:      "#lng",
					street_number: '#street_number',
					route: '#route',
					locality: '#locality',
					administrative_area_level_2: '#administrative_area_level_2',
					administrative_area_level_1: '#administrative_area_level_1',
					country:  '#country',
					postal_code: '#postal_code',
					type:    '#type' 	
				},
				mapOptions: {
					zoom: 5,
					center: new google.maps.LatLng(10,20),
				}
			});

			$('#reverseGeocode1').change(function(){ 
				$(".addresspicker_map1").addresspicker("option", "reverseGeocode", ($(this).val() === 'true'));
			});
			var gmarker = addresspickerMap.addresspicker( "marker");
			gmarker.setVisible(true);
			addresspickerMap.addresspicker( "updatePosition");
		
			var geocoder = new google.maps.Geocoder();
			var map = addresspickerMap.addresspicker("map");
			var address = $('input[name=principal_address]').val();
			//"{{ person.contacts.principal_address|default_if_none:'Roorkee, Uttarakhand, India' }}";
			if(address == ''){
				address = 'Roorkee, Uttarakhand, India';
			}
			
			geocoder.geocode( { 'address': address}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					map.setCenter(results[0].geometry.location);
					var marker = gmarker;
					gmarker.map = map;
					gmarker.position = results[0].geometry.location;
				} else {
					alert('Geocode was not successful for the following reason: ' + status);
				}
			});
		});	
	});
	
	
	/* MAP 2*/
	$(".addresspicker_map2").focus(function(){
		$(".map-wrapper2").css("display","block");
	
		$(function() {
			var addresspickerMap = $( ".addresspicker_map2" ).addresspicker({
				regionBias: "fr",
				elements: {
					map:"#map2",
				},
				mapOptions: {
					zoom: 5,
					center: new google.maps.LatLng(10,20),
				}
			});

			$('#reverseGeocode2').change(function(){ 
				$(".addresspicker_map2").addresspicker("option", "reverseGeocode", ($(this).val() === 'true'));
			});
			var gmarker = addresspickerMap.addresspicker( "marker");
			gmarker.setVisible(true);
			addresspickerMap.addresspicker( "updatePosition");
		
			var geocoder = new google.maps.Geocoder();
			var map = addresspickerMap.addresspicker("map");
			var address = $('input[name=alternate_address1]').val();
			//"{{ person.contacts.principal_address|default_if_none:'Roorkee, Uttarakhand, India' }}";
			if(address = ''){
				address = 'Roorkee, Uttarakhand, India';
			}
			geocoder.geocode( { 'address': address}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					map.setCenter(results[0].geometry.location);
					var marker = gmarker;
					gmarker.map = map;
					gmarker.position = results[0].geometry.location;
				} else {
					alert('Geocode was not successful for the following reason: ' + status);
				}
			});
		});	
	});
	
	/* MAP 3*/
	$(".addresspicker_map3").focus(function(){
		$(".map-wrapper3").css("display","block");
			$(function() {
			var addresspickerMap = $( ".addresspicker_map3" ).addresspicker({
				regionBias: "fr",
				elements: {
					map:"#map3",
				},
				mapOptions: {
					zoom: 5,
					center: new google.maps.LatLng(10,20),
				}
			});

			$('#reverseGeocode3').change(function(){ 
				$(".addresspicker_map3").addresspicker("option", "reverseGeocode", ($(this).val() === 'true'));
			});
			var gmarker = addresspickerMap.addresspicker( "marker");
			gmarker.setVisible(true);
			addresspickerMap.addresspicker( "updatePosition");
		
			var geocoder = new google.maps.Geocoder();
			var map = addresspickerMap.addresspicker("map");
			var address = $('input[name=alternate_address2]').val();
			//"{{ person.contacts.principal_address|default_if_none:'Roorkee, Uttarakhand, India' }}";
			if(address = ''){
				address = 'Roorkee, Uttarakhand, India';
			}
			geocoder.geocode( { 'address': address}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					map.setCenter(results[0].geometry.location);
					var marker = gmarker;
					gmarker.map = map;
					gmarker.position = results[0].geometry.location;
				} else {
					alert('Geocode was not successful for the following reason: ' + status);
				}
			});
		});	
	});
		/* MAP 4*/
	$(".addresspicker_map4").focus(function(){
		$(".map-wrapper4").css("display","block");
	
		$(function() {
			var addresspickerMap = $( ".addresspicker_map4" ).addresspicker({
				regionBias: "fr",
				elements: {
					map:"#map4",
				},
				mapOptions: {
					zoom: 5,
					center: new google.maps.LatLng(10,20),
				}
			});

			$('#reverseGeocode4').change(function(){ 
				$(".addresspicker_map4").addresspicker("option", "reverseGeocode", ($(this).val() === 'true'));
			});
			var gmarker = addresspickerMap.addresspicker( "marker");
			gmarker.setVisible(true);
			addresspickerMap.addresspicker( "updatePosition");
		
			var geocoder = new google.maps.Geocoder();
			var map = addresspickerMap.addresspicker("map");
			var address = $('input[name=alternate_address3]').val();
			//"{{ person.contacts.principal_address|default_if_none:'Roorkee, Uttarakhand, India' }}";
			if(address = ''){
				address = 'Roorkee, Uttarakhand, India';
			}
			geocoder.geocode( { 'address': address}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					map.setCenter(results[0].geometry.location);
					var marker = gmarker;
					gmarker.map = map;
					gmarker.position = results[0].geometry.location;
				} else {
					alert('Geocode was not successful for the following reason: ' + status);
				}
			});
		});	
	});


	/* MARITAL STATUS */
	if($('input[name=marital_status]').val()=="yes"){	
		$("#spouse_form").css("display","block");
		$("#spouse_form :input").removeAttr("disabled");
	}
	else{
		$("#spouse_form :input").attr("disabled","true");
		$("#spouse_form").css("display","none");
	}
	$('input[name=marital_status]').change(function(){
		if($(this).val()=="yes"){	
			$("#spouse_form").css("display","block");
			$("#child_button").css("display","block");
			$("#child_remove").css("display","block");	
			$("#spouse_form :input").removeAttr("disabled");
		}
		else{
			child_count=0;
			$("#child_count").val(child_count);
			$("#spouse_form").css("display","none");
			$("#child_button").css("display","none");
			$("#child_remove").css("display","none");
			$("#spouse_form :input").attr("disabled","true");
			$("#child_form").empty();	
		}	
	});
	$('#child_count').val(child_count);			

	/*** Default Submit Button ***/
	$(function(){
		$('form').each(function () {
			var thisform = $(this);
			thisform.prepend(thisform.find('.ajax-button').clone().css({
				position: 'absolute',
				left: '-999px',
				top: '-999px',
				height: 0,
				width: 0
			}));
		});
	});
	
	
	/*** Form Validations ***/	

	$('form').submit(function(){
		var valid=true;
		$.each($('.required :input'), function(){
			valid=true;
			if($(this).val() == ''){
				if($(this).attr("disabled")){
					return;
				}
				$(this).focus();
				valid=false;
				$(this).siblings('span.help-inline').html('This field is required.');
				return false;
			}	
		});
		var phone;
		phone = $('input[name=phone_home]').val();
		if((isNaN(phone) && valid)){
			alert("Phone no. must contain only numbers (0-9)");
			$('input[name=phone_home]').focus();
			return false;
		}
		phone = $('input[name=phone_work]').val();
		if((isNaN(phone) && valid)){
			alert("Phone no. must contain only numbers (0-9)");
			$('input[name=phone_work]').focus();		
			return false;
		}
		phone = $('input[name=phone_mobile]').val();
		if((isNaN(phone) && valid)){
			alert("Phone no. must contain only numbers (0-9)");
			$('input[name=phone_mobile]').focus();	
			return false;
		}
		return valid;
	});
});

