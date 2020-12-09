/*
	This constant values are for key DOM elements in form including itself 
*/
const form = document.getElementById("transaction-form");

const senderCard = document.getElementById('senderCard');
const receiverCard = document.getElementById('receiverCard');
const summa = document.getElementById("summa");


/*
	Set of regular expressions to validate inputs
*/
receiverCardRegex = /^\d{4} \d{4} \d{4} \d{4}$/
summaRegex = /^\d{1,7}(\.\d{1,2})?$/


/*
	Some literals used in programm to feedback errors
*/
// Default
const emptyFieldError = "Це поле треба заповнити";
const fieldMustBeEmpty = "Це поле має бути пустим";
const notChosenOption = "Необхідно обрати один з варіантів";
// Custom
const incorrectReceiverCard = "Номер карти отримувача має складатись із 16 цифр";
const notAvailableReceiverCard = "Вказаний номер карти неможливий";
const senderAndReceiverCardsEqual = "Не можна вказувати картку, з якої проводиться транзакція";
const incorrectSumma = "Сума переказу вказана некоректно";
const summaGreaterThan1E6 = "Сума переказу не може перевищувати 1 000 000 грн.";
const summaIsZero = "Сума переказу не може бути нульовою";
const notEnoughtBalance = "Вказана сума перевищує баланс на картці";


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


function getCheckInputListener(input, errMessage=emptyFieldError){
	return (event) => {return checkInput(input, errMessage)};
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
Getting listener for validation of sender card
*/
checkSenderCard = getCheckInputListener(senderCard, notChosenOption);


/*
Listener for validation of recipient card
*/
function checkReceiverCard(event){
	var value = receiverCard.value;

	if (!checkInput(receiverCard)) return false;
	if (!receiverCardRegex.test(value)){
		setInvalid(receiverCard, incorrectReceiverCard);
		return false;
	}
	if (value === senderCard.value){
		setInvalid(receiverCard, senderAndReceiverCardsEqual)
	}
	if (!valid_credit_card(value)){
		setInvalid(receiverCard, notAvailableReceiverCard);
		return false;
	}
}


/*
Listener for validation of transaction summa
*/
function checkSumma(event){
	var value = summa.value;

	if (!checkInput(summa)) return false;
	if (!summaRegex.test(value)){
		setInvalid(summa, incorrectSumma);
		return false;
	}
	if (+value > 1e6){
		setInvalid(summa, summaGreaterThan1E6);
		return false;
	}
	if (+value === 0){
		setInvalid(summa, summaIsZero);
		return false;
	}
}


// Takes a credit card string value and returns true on valid number
function valid_credit_card(value) {
  // Accept only digits, dashes or spaces
	if (/[^0-9-\s]+/.test(value)) return false;

	// The Luhn Algorithm. It's so pretty.
	let nCheck = 0, bEven = false;
	value = value.replace(/\D/g, "");

	for (var n = value.length - 1; n >= 0; n--) {
		var cDigit = value.charAt(n),
			  nDigit = parseInt(cDigit, 10);

		if (bEven && (nDigit *= 2) > 9) nDigit -= 9;

		nCheck += nDigit;
		bEven = !bEven;
	}

	return (nCheck % 10) == 0;
}



senderCard.addEventListener("blur", checkSenderCard, true);
receiverCard.addEventListener("blur", checkReceiverCard, true);
summa.addEventListener("blur", checkSumma, true);
