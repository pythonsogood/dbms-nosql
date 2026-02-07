/**
 * @param {HTMLFormElement} form
 * @returns void
 */
async function onReviewSubmit(form) {
	const response = await fetch(form.action, {
		method: form.method,
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({
			rating: parseInt(reviewRating.value),
			comment: reviewComment.value,
		})
	});

	const data = await response.json();

	if (!response.ok) {
		alert(data.detail);
		return;
	}

	window.location.reload();
}

/**
 * @param {HTMLFormElement} form
 * @returns void
 */
async function onAddToCartSubmit(form) {
	const response = await fetch(form.action + `/?size=${form.elements.size.value}&quantity=${form.elements.quantity.value}`, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json"
		},
	});

	const data = await response.json();

	if (!response.ok) {
		alert(data.detail);
		return;
	}

	alert(data.message);

	window.location.reload();
}