document.addEventListener("DOMContentLoaded", async () => {
    const priceRange = document.getElementById("priceRange");

    if (priceRange) {
        const rangeLabel = document.createElement("span");
        rangeLabel.className = "badge bg-dark ms-2";
        rangeLabel.textContent = `$${priceRange.value}`;

        priceRange.parentNode.insertBefore(rangeLabel, priceRange.nextSibling);
    }
});