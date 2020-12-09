/*
	Remember that we uses current script after script registrationFormValidation.js
	And so we use form validation function checkForm from named script
*/
const myForm = form;

myForm.addEventListener('submit', function (e) {
	e.preventDefault();

	if (!checkForm(e)) return;

	var butn = document.getElementById("ButSub");
	butn.disabled  = true;
	butn.innerHTML = "Processing...";
	const formData = new FormData(this);

	fetch('/reg-in', {
		method: 'POST',
		body: formData
	}).then(function (response) {

		if (response.status !== 200) {
			response.json().then(function (data) {
				document.getElementById('alertspace').innerHTML = ''; 
				for (const [ key, value ] of Object.entries(data)) {
					document.getElementById('alertspace').innerHTML += "<div class='alert alert-danger alert-dismissible fade show' role='alert'>" +
					"<strong>"+ key +" вже існує в базі даних.</strong> Перевірте будь-ласка введені дані." +
					"<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
					"<span aria-hidden='true'>&times;</span></button> </div>";
				}
				var butn = document.getElementById("ButSub");
				butn.disabled = false;
				butn.innerHTML = "Відправити дані";
				console.log(data);
			});
		} else {
			response.json().then(function (data) {
                var value = data["redirect"];
                window.location.href = window.location.origin + value;
            });
		}
				
	})
});