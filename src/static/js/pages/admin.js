/**
 * @param {HTMLFormElement} form
 * @returns void
 */
async function deleteProduct(form) {
	const response = await fetch(form.action, {
		method: "DELETE",
		headers: {
			"Content-Type": "application/json"
		},
	});

	const data = await response.json();

	if (!response.ok) {
		alert(JSON.stringify(data.detail));
		return;
	}

	window.location.reload();
}