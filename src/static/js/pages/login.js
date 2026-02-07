/**
 * @param {HTMLFormElement} form
 * @returns void
 */
async function onLoginSubmit(form) {
	const response = await fetch(form.action, {
		method: form.method,
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({
			username: form.elements.username.value,
			password: form.elements.password.value
		})
	});

	const data = await response.json();

	if (!response.ok) {
		alert(data.detail);
		return;
	}

	window.location.href = "/";
}