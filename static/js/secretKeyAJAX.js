const myForm = document.getElementById("log_form");

myForm.addEventListener('submit', function (e) {
	e.preventDefault();
            
    var butn = document.getElementById("KeySub");
	butn.disabled = disabled = true;
	butn.innerHTML = "Processing...";
            
	const formData = new FormData(this);

	fetch('/secret-key-check', {
		method: 'POST',
		body: formData
	}).then(function (response) {

		if (response.status !== 200) {
			response.json().then(function (data) {
				document.getElementById('alertspace').innerHTML = ''; 
				for (const [ key, value ] of Object.entries(data)) {
					document.getElementById('alertspace').innerHTML += "<div class='alert alert-danger alert-dismissible fade show' role='alert'>" +
					"<strong>"+ key +".</strong> Перевірте будь-ласка введені дані. Схоже ваш ключ не підходить." +
					"<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
					"<span aria-hidden='true'>&times;</span></button> </div>";
				}
                var butn = document.getElementById("KeySub");
				butn.disabled = disabled = false;
				butn.innerHTML = "Підтвердити";
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