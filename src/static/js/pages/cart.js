/**
 * @param {string} product_id
 * @param {string} size
 * @param {number} quantity
 * @returns void
 */
async function cartItemQuantityChange(product_id, size, quantity) {
	const response = await fetch(`/api/shop/cart/${product_id}?size=${size}&quantity=${quantity}`, {
		method: "PATCH",
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