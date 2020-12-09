
function senderCardOnBlur(event){
	if (receiverCard.value == senderCard.value) {
		receiverCard.value = "";
		receiverCard.classList.remove("is-valid");
		receiverCard.classList.remove("is-invalid");
	}
}


function receiverCardOnKeyDown(event){
	var K = event.key;
	var selStart = receiverCard.selectionStart;

	if ((K === "Backspace") &&
			([5, 10, 15].includes(selStart)) &&
			(selStart === receiverCard.selectionEnd)){
		var value = receiverCard.value;

		value = value.slice(0, selStart-1) + value.slice(selStart);
		
		receiverCard.value = value.slice(0, selStart-1) + value.slice(selStart-1);

		receiverCard.selectionStart = selStart-1;
		receiverCard.selectionEnd = receiverCard.selectionStart;
	}

	else if ((K === "ArrowRight") &&
			([3, 8, 13].includes(selStart)) &&
			(selStart === receiverCard.selectionEnd)){
		receiverCard.selectionStart++;
		receiverCard.selectionEnd++;
	}

	else if ((K === "ArrowLeft") &&
			([5, 10, 15].includes(selStart)) &&
			(selStart === receiverCard.selectionEnd)){
		receiverCard.selectionStart--;
		receiverCard.selectionEnd--;
	}

	if (/^\D$/.test(K)) event.preventDefault();
}


function receiverCardOnInput (event){
	var caretePos = receiverCard.selectionStart;

	receiverCard.value = formatCardNumber(receiverCard.value);
	
	receiverCard.selectionStart = caretePos + [4, 9, 14].includes(caretePos);
	receiverCard.selectionEnd = receiverCard.selectionStart;
}


function summaOnKeyDown(event){
	var K = event.key;
	var selStart = summa.selectionStart;
	var value = summa.value;
	var point = value.match(/\./);

	summa.selectionEnd = selStart;

	if (K==="."){
		if (point) event.preventDefault();
		else if ((value.length - selStart) > 2) event.preventDefault();
	}
	else if (K.match(/^\d$/)){
		var valLen = value.length;

		if (point){
			var ptPos = point.index;

			if (selStart <= ptPos){

			}
			else{
				if (valLen-ptPos > 2) event.preventDefault();
			}
		}
		else {
			if (valLen === 7) event.preventDefault();
		}
	}
	else if (K==="Backspace"){
		if (point && (selStart==point.index+1)){
			summa.value = value.slice(0, point.index+1);
		}
	}
	else if (K==="Delete"){
		if (point && (selStart==point.index)){
			summa.value = value.slice(0, point.index);
		}
	}
	else if (! ["ArrowLeft", "ArrowRight"].includes(K)){
		event.preventDefault();
	}
}


function summaOnBlur(event){
	var valLen = summa.value.length;
	var point = summa.value.match(/\./);

	if (point){
		var ptPos = point.index;
		var diff = valLen-ptPos;

		if (diff===1) summa.value += "00";
		else if (diff===2) summa.value += "0";
	}
	else summa.value += ".00";
}


function formatCardNumber(number){
	var newNumber = number.replaceAll(" ", "");
	var len = newNumber.length;
	if (len >= 4) {
		newNumber = newNumber.slice(0, 4) + " " + newNumber.slice(4,);
	}
	else return newNumber;

	if (len >= 8){
		newNumber = newNumber.slice(0, 9) + " " + newNumber.slice(9,);
	}
	else return newNumber;

	if (len >= 12){
		newNumber = newNumber.slice(0, 14) + " " + newNumber.slice(14,);
	}
	return newNumber;

}

senderCard.addEventListener("blur", senderCardOnBlur);

receiverCard.addEventListener("keydown", receiverCardOnKeyDown);
receiverCard.addEventListener("input", receiverCardOnInput);

summa.addEventListener("keydown", summaOnKeyDown);
summa.addEventListener("blur", summaOnBlur);