/*
This script foresees addition of script includeSelects.js
because specified script provides enabling fields for inputing
passport series, district and city.
Also current script provides few constant variables for
script includeSelects.js.
*/


/*
	This constant values are for key DOM elements in form including itself 
*/
const form = document.getElementById("registration-form");

const name = document.getElementById('name');
const surname = document.getElementById('surname');
const email = document.getElementById("email");

const passportType = document.getElementById("passport-type");
const passportSeries = document.getElementById("passport-series");
const passportID = document.getElementById("passport-ID");
const vatin = document.getElementById("VATIN");

const region = document.getElementById("region");
const district = document.getElementById("district");
const city = document.getElementById("city");
const phone = document.getElementById("phone");

const password = document.getElementById("password");
const password2 = document.getElementById("password2");

const secretQuestion = document.getElementById("secret-question");
const secretAnswer = document.getElementById("secret-answer");

const accepsRules = document.getElementById("accept-rules");


/*
	Set of regular expressions to validate inputs
*/
const emailRegex = /^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$/;
const passpSeriesRegex = /^[абвгґдеєжзиіїйклмнопрстуфхцчшщьюя]{2}$/i;
const passpBookIDRegex = /^\d{6}$/;
const passpCardIDRegex = /^\d{9}$/;
const vatinRegex = /^\d{10}$|^\d{12}?$/;
const phoneRegex = /^\+?3?8?(0[5-9][0-9]\d{7})$/;
const passwordGeneralRegexp = /^\w{8,40}$/i;
const passwordNumRegex = /.{0,}\d+.{0,}/;
const passwordUpperRegex = /.{0,}[A-Z]+.{0,}/;


/*
	Some literals used in programm to feedback errors
*/
// Default
const emptyFieldError = "Це поле треба заповнити";
const fieldMustBeEmpty = "Це поле має бути пустим";
const notChosenOption = "Необхідно обрати один з варіантів";
// Custom
const incorrectEmail = "Некоректно вказана адреса електронної пошти";
const incorrectPasspSeries = "Серія паспорту має містити 2 українські літери";
const incorrectBookID = "Номер паспорту (книжечка) має складатися з 6 цифр";
const incorrectCardID = "Номер паспорту (ID картка) має складатися з 9 цифр";
const incorrectVATIN = "ІПН має складатися з 12 або з 10 цифр";
const incorrectPhone = "Номер телефону має відповідати формату +380ххххххххх";
const incorrectPasswordGeneral = "Пароль має бути не коротшим за 8 символів і має містити літери латиниці і числа та може включати символ '_'.";
const incorrectPasswordSecondary = "Пароль має містити принаймні одну цифру та літеру верхнього регістру";
const incorrectPassword2 = "Паролі не співпадають";


/*
	Next part of code contains checkXXXX functions for validations and giving
	feedback about error to user
*/

/*
This function is default for checking input field for emptiness.
It responsive for showing error when input field is empty.
Returns true when field input is not empty and false otherwise.
*/ 
function checkInput(input, errMessage=emptyFieldError) {
	var value = input.value.trim();

	if (input.hasAttribute("disabled")) return value?true:false;

	if (value ==='') setInvalid(input, errMessage);
	else {
		setValid(input);
		return true;
	}
	return false;
}


/*
This function returns listener-function for input
and just realises checkInput validation.
*/
function getCheckInputListener(input, errMessage=emptyFieldError){
	return (event) => {return checkInput(input, errMessage)};
}


/*
checkName and checkSurname are listeners to be used as validations of
name and surname inputs.
*/
checkName = getCheckInputListener(name);
checkSurname = getCheckInputListener(surname);


/*
Listener for validation of email
*/
function checkEmail(event){
	var value = email.value;

	if (!checkInput(email)) return false;
	else if (!emailRegex.test(value)){
		setInvalid(email, incorrectEmail);
		return false;
	}
	else{
		setValid(email);
		return true;
	}
}


/*
Getting listener for validation of passport type
*/
checkPassportType = getCheckInputListener(passportType, notChosenOption);


/*
Listener for validation of passport series
*/
function checkPassportSeries(event){
	var passpType = passportType.value;
	var value = passportSeries.value;

	if (passpType === 'book'){
		if (!checkInput(passportSeries)) return false;
		if (!passpSeriesRegex.test(value)) {
			setInvalid(passportSeries, incorrectPasspSeries);
			return false;
		}
		setValid(passportSeries);
		passportSeries.value = value.toUpperCase();
		return true;
	}
	else if (passpType === 'card'){
		if (value !== ''){
			setInvalid(passportSeries, fieldMustBeEmpty);
			return false;
		}
	}
	return true
}


/*
Listener for validation of passport ID
*/
function checkPassportID(event){
	var passpType = passportType.value;
	var value = passportID.value;

	if (passpType === 'book'){
		if (!checkInput(passportID)) return false;
		if (!passpBookIDRegex.test(value)) {
			setInvalid(passportID, incorrectBookID);
			return false;
		}
		setValid(passportID);
		return true;
	}
	else if (passpType === 'card'){
		if (!checkInput(passportID)) return false;
		if (!passpCardIDRegex.test(value)) {
			setInvalid(passportID, incorrectCardID);
			return false;
		}
		setValid(passportID);
		return true;
	}
	return true
}


/*
Listener for validation of VATIN code
*/
function checkVATIN(event){
	var value = vatin.value;

	if (!checkInput(vatin)) return false;
	if (!vatinRegex.test(value)){
		setInvalid(vatin, incorrectVATIN);
		return false;
	}
	setValid(vatin);
	return true;
}


/*
Getting listeners for validation of region, district and city
*/
checkRegion = getCheckInputListener(region, notChosenOption);
checkDistrict = getCheckInputListener(district, notChosenOption);
checkCity = getCheckInputListener(city, notChosenOption);


/*
Listener for validation of phone number
*/
function checkPhone(event){
	var value = phone.value;

	if (!checkInput(phone)) return false;
	if (!phoneRegex.test(value)){
		setInvalid(phone, incorrectPhone);
		return false;
	}

	setValid(phone);
	return true;
}


/*
password validator uses last value of password to make some actions
*/
var lastPasswordValue = "";
/*
Listener for validation of password
*/
function checkPassword(event){
	var value = password.value;

	if (!checkInput(password)) return false;
	if (!passwordGeneralRegexp.test(value)){
		setInvalid(password, incorrectPasswordGeneral);
		return false;
	}
	else if (!(passwordNumRegex.test(value) && passwordUpperRegex.test(value))){
		setInvalid(password, incorrectPasswordSecondary);
		return false;
	}
	else{
		setValid(password);
		return true;
	}

}
/*
Listener to drop value from password2 when password changed
*/
function dropPassword2(event){
	var value = password.value;

	if (value !== lastPasswordValue){
		password2.classList.remove("is-invalid");
		password2.classList.remove("is-valid");
		password2.value = "";
	}
}

password.addEventListener("blur", dropPassword2, true)


/*
Listener for validation of password2
*/
function checkPassword2(event){
	var value = password2.value;
	var passwd = password.value;

	if (!checkInput(password2)) return false;
	if (value !== passwd){
		setInvalid(password2, incorrectPassword2);
		return false;
	}
	setValid(password2);
	return true;
}


/*
Getting listeners for validation of secret question and secret answer
*/
checkSecretQuestion = getCheckInputListener(secretQuestion, notChosenOption);
checkSecretAnswer = getCheckInputListener(secretAnswer);


/*
Last one - check if user accepted usage rules (not event listener)
*/
function checkAcceptRules(){
	if (accepsRules.checked){
		accepsRules.classList.remove("is-invalid");
		return true;
	}
	else{
		accepsRules.classList.add("is-invalid");
		return false;
	}
}


/*
	Functions giving feedback for some element
*/

/*
setInvalid gives error feedback with message for element 
*/
function setInvalid(element, message=emptyFieldError){
	var feedbackDiv = element.parentElement.querySelector("div.invalid-feedback");
	feedbackDiv.innerText = message;

	element.classList.remove("is-valid");
	element.classList.add("is-invalid");
}


/*
setValid gives succes feedback for element without any messages
*/
function setValid(element){
	element.classList.remove("is-invalid");
	element.classList.add("is-valid");
}


/*
This function is listener for submitting registraton form.
It uses each previous validators (listeners) within AND function.
AND function is just logical AND operator-like function
*/
function checkForm(event){
	event.preventDefault();
	if (AND(checkName(event), checkSurname(event), checkEmail(event), 
		checkPassportType(event), checkPassportSeries(event), checkPassportID(event),
		checkVATIN(event), 
		checkRegion(event), checkDistrict(event), checkCity(event),
		checkPhone(event),
		checkPassword(event), checkPassword2(event),
		checkSecretQuestion(event), checkSecretAnswer(event),
		checkAcceptRules()));
}

/*
This function returns logical AND value for each of arguments it gets.
Difference between this function and && operator is that if some argument is
expression (function call, for example) so that argument will be evaluated
first and then got as argument while && operator just will return last logically 
false operand without evaluating other operands wich may be expressions.
It is valuable because checkForm function must show all the errors if they occured
but it does no if && operator used.
*/
function AND(){
	var n = arguments.length;
	if (!n) return false;
	if (n === 1) return (!!arguments[0]);
	for (var i = 0; i < n; i++) {
		if (!arguments[i]) return false;
	}
	return true;
}

/*
	Last part of script - binding listeners to events.
*/

/*
Blur event represents losing of focus on element. Binding validation listeners
to blur events allows to show feedback immediatelly after filling input field. 
*/
name.addEventListener("blur", checkName, true);
surname.addEventListener("blur", checkSurname, true);
email.addEventListener("blur", checkEmail, true);

passportType.addEventListener("blur", checkPassportType, true);
passportSeries.addEventListener("blur", checkPassportSeries, true);
passportID.addEventListener("blur", checkPassportID, true);
vatin.addEventListener("blur", checkVATIN, true);

region.addEventListener("blur", checkRegion, true);
district.addEventListener("blur", checkDistrict, true);
city.addEventListener("blur", checkCity, true);
phone.addEventListener("blur", checkPhone, true);

password.addEventListener("blur", checkPassword, true)
password2.addEventListener("blur", checkPassword2, true)

secretQuestion.addEventListener("blur", checkSecretQuestion, true)
secretAnswer.addEventListener("blur", checkSecretAnswer, true)


/*
Key listener - validation of entire form on submit event before sending form to
server.
*/
form.addEventListener("submit", checkForm, false);