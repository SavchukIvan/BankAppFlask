/*
This script must be added after scripts registrationFormValidation.js and regionsDistrictsCities.js
because it uses constant variables 
- from first one: form, passportType, passportSeries, passportID, region, district and city;
- from second one: regions and districts.
*/


/*
Last values of passport type and region, district are useful to recognize if user didn't changed
its selections when event 'blur' occured, so in this case we have not to drop values in other fields.
*/
var lastPassportTypeValue = '';

var lastRegionValue = '';
var lastDistrictValue = '';


/*
unsetValidStatus drops succes or error feedback for element.
*/
function unsetValidStatus(element){
	element.classList.remove("is-valid");
	element.classList.remove("is-invalid");
}


/*
Listener for passwortType. It enables field passportID and enables or disables field
passportSeries depending on type of passport.
*/
function onSelectPassportType(event){
	var value = passportType.value;

	if (value === lastPassportTypeValue) return;
	lastPassportTypeValue = value;

	unsetValidStatus(passportSeries);
	unsetValidStatus(passportID);
	passportID.value = '';
	passportSeries.value = '';
	
	if (value === 'book'){
		passportID.setAttribute('maxlength', '6')
		if (passportSeries.hasAttribute('disabled')) passportSeries.removeAttribute('disabled');
		if (passportID.hasAttribute('disabled')) passportID.removeAttribute('disabled');
	}
	else if (value === 'card'){
		passportID.setAttribute('maxlength', '9')
		if (!passportSeries.hasAttribute('disabled')) passportSeries.setAttribute('disabled', '');
		if (passportID.hasAttribute('disabled')) passportID.removeAttribute('disabled');
	}
}


/*
This listener for select-field region enables select-field district and clear value in it. 
It set all available options (districts) for chosen region.
Also it disables field cities and clear values for it.
*/
function onSelectRegion(event){
	var value = region.value;

	if (value === lastRegionValue) return;
	lastRegionValue = value;

	unsetValidStatus(district);
	unsetValidStatus(city);
	district.value = '';

	district.removeAttribute('disabled');
	city.setAttribute('disabled', "");
	district.value = '';
	city.value = '';

	district.innerHTML = createOptions(regions.get(value));
}


/*
This listener for select-field district enables select-field city and clear value in it. 
It set all available options (cities) for chosen district.
*/
function onSelectDistrict(event){
	var value = district.value;

	if (value === lastDistrictValue) return;
	lastDistrictValue = value;

	unsetValidStatus(city);

	city.removeAttribute('disabled');
	city.value = '';

	city.innerHTML = createOptions(districts.get(value));
}


/*
This function gets strings array of available in select options as parameter options.
It generates HTML markup with tags <option> for all strings in options. Very first option
is default and not present in options array. It is selected and disabled and has empty string value.
Text of this option is defined as optional parameter defaultOptionText. Returns string with HTML.
*/
function createOptions(options, defaultOptionText="Обрати..."){
	var selectInner = "<option selected disabled value=\"\">"+defaultOptionText+"</option>";
	var option;

	for (var i = 0; i < options.length; i++){
		option = options[i];
		selectInner = selectInner+"\n"+"<option value=\""+option+"\">"+option+"</option>";
	}
	return selectInner;
}


/*
Binding listeners to events on select elements.
*/
passportType.addEventListener('blur', onSelectPassportType);
region.addEventListener('blur', onSelectRegion);
district.addEventListener('blur', onSelectDistrict);


/*
Add available options to select regions in HTML.
*/
region.innerHTML = createOptions(Array.from(regions.keys()));