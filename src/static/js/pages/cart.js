/**
 * @param {HTMLInputElement} input
 * @param {string} product_id
 * @param {string} size
 * @returns void
 */
async function cartItemQuantityChange(input, product_id, size) {
	input.disabled = true;

	const response = await fetch(`/api/shop/cart/${product_id}?size=${size}&quantity=${input.value}`, {
		method: "PATCH",
		headers: {
			"Content-Type": "application/json"
		},
	});

	const data = await response.json();

	if (!response.ok) {
		alert(JSON.stringify(data.detail));
		return;
	}

	input.disabled = false;

	window.location.reload();
}

/**
 * @param {string} product_id
 * @param {string} size
 * @returns void
 */
async function removeFromCart(product_id, size) {
	const response = await fetch(`/api/shop/cart/${product_id}?size=${size}`, {
		method: "DELETE",
		headers: {
			"Content-Type": "application/json"
		},
	});

	const data = await response.json();

	if (!response.ok) {
		alert(data.detail);
		return;
	}

	window.location.reload();
}