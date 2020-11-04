/*
This constant values are for key DOM elements in form including itself 
*/
const form = document.getElementById("login-form");
const email = document.getElementById("email");
const password = document.getElementById("password");


/*
Some literals used in programm to feedback errors
*/
const emptyFieldError = "Ви нічого не ввели";
const incorrectEmail = "Таких імейлів не існує в нашій базі даних";
const incorrectPassword = "Неправильний пароль";


/*
Set of regular expressions to validate inputs
*/
const emailRegex = /^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$/;
const passwordGeneralRegexp = /^\w{8,40}$/i;
const passwordNumRegex = /.{0,}\d+.{0,}/;
const passwordUpperRegex = /.{0,}[A-Z]+.{0,}/;


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
Listener for validation of password
*/
function checkPassword(event){
	var value = password.value;


	if (!checkInput(password)) return false;
	if (!passwordGeneralRegexp.test(value)){
		setInvalid(password, incorrectPassword);
		return false;
	}
	else if (!(passwordNumRegex.test(value) && passwordUpperRegex.test(value))){
		setInvalid(password, incorrectPassword);
		return false;
	}
	else{
		setValid(password);
		return true;
	}

}


/*
This function is listener for submitting registraton form.
It uses each previous validators (listeners) within AND function.
AND function is just logical AND operator-like function
*/
function checkForm(event){
	event.preventDefault();
	if (AND(checkEmail(event), checkPassword(event))) form.submit();
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
Blur event represents losing of focus on element. Binding validation listeners
to blur events allows to show feedback immediatelly after filling input field. 
*/
email.addEventListener("blur", checkEmail, true);
password.addEventListener("blur", checkPassword, true);

/*
Key listener - validation of entire form on submit event before sending form to
server.
*/
form.addEventListener("submit", checkForm, false);