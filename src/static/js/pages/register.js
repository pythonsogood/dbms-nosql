/**
 * @param {HTMLFormElement} form
 * @returns void
 */
async function onRegisterSubmit(form) {
	const body = {
		username: form.elements.username.value,
		email: form.elements.email.value,
		first_name: form.elements.first_name.value,
		password: form.elements.password.value,
	};

	if (form.elements.last_name.value) {
		body.last_name = form.elements.last_name.value;
	}

	if (form.elements.phone_number.value) {
		body.phone_number = form.elements.phone_number.value;
	}

	const response = await fetch(form.action, {
		method: form.method,
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(body)
	});

	const data = await response.json();

	if (!response.ok) {
		alert(JSON.stringify(data.detail));
		return;
	}

	window.location.href = "/";
}