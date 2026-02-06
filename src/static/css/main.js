document.addEventListener('DOMContentLoaded', () => {
    
    // ==========================================
    // 1. GLOBAL LOGIC (base.html)
    // ==========================================
    
    // Auto-hide Flash Messages after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.style.transition = "opacity 0.5s ease";
                alert.style.opacity = "0";
                setTimeout(() => alert.remove(), 500);
            });
        }, 4000);
    }

    // Highlight active Navbar link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active', 'text-danger');
        }
    });

    // ==========================================
    // 2. SHOP PAGE LOGIC (shop.html)
    // ==========================================
    const priceRange = document.getElementById('priceRange');
    if (priceRange) {
        // Create a label to show the current price value dynamically
        const rangeLabel = document.createElement('span');
        rangeLabel.className = 'badge bg-dark ms-2';
        rangeLabel.textContent = `$${priceRange.value}`;
        priceRange.parentNode.insertBefore(rangeLabel, priceRange.nextSibling);

        priceRange.addEventListener('input', (e) => {
            rangeLabel.textContent = `$${e.target.value}`;
        });

        // Trigger filter on change (optional: send to backend)
        priceRange.addEventListener('change', (e) => {
            console.log(`Filter by max price: ${e.target.value}`);
            // Logic to reload page with query param:
            // window.location.href = `/shop?max_price=${e.target.value}`;
        });
    }

    // ==========================================
    // 3. PRODUCT DETAIL LOGIC (product.html)
    // ==========================================
    const addToCartForm = document.querySelector('form[action^="/add_to_cart"]');
    if (addToCartForm) {
        addToCartForm.addEventListener('submit', (e) => {
            const sizeInputs = document.querySelectorAll('input[name="size"]');
            let sizeSelected = false;
            sizeInputs.forEach(input => {
                if (input.checked) sizeSelected = true;
            });

            if (!sizeSelected) {
                e.preventDefault(); // Stop submission
                alert('Please select a size before adding to cart.');
                // Highlight size options
                document.querySelector('.d-flex.gap-2').classList.add('border', 'border-danger', 'p-2');
            }
        });
    }

    // ==========================================
    // 4. CART PAGE LOGIC (cart.html)
    // ==========================================
    const cartTable = document.querySelector('table');
    if (cartTable) {
        const qtyInputs = document.querySelectorAll('input[type="number"]');
        
        qtyInputs.forEach(input => {
            input.addEventListener('change', async (e) => {
                const newQty = e.target.value;
                if (newQty < 1) {
                    e.target.value = 1; 
                    return;
                }
                
                // UX: Disable input while updating
                e.target.disabled = true;

                // Here you would typically call your backend API
                // Example: await updateCartQuantity(productId, newQty);
                
                console.log(`Updated quantity to ${newQty}. recalculating total...`);
                
                // Simulate reload to update totals (Simplest approach for Flask)
                // location.reload(); 
                
                // Re-enable input
                e.target.disabled = false;
            });
        });
    }

    // ==========================================
    // 5. ADMIN DASHBOARD LOGIC (admin.html)
    // ==========================================
    const deleteButtons = document.querySelectorAll('.btn-outline-danger');
    if (deleteButtons.length > 0) {
        deleteButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                if (!confirm('Are you sure you want to delete this product? This action cannot be undone.')) {
                    e.preventDefault();
                } else {
                    // Logic to find the product ID usually stored in a data-attribute
                    // const productId = btn.getAttribute('data-id');
                    // fetch(`/api/delete/${productId}`, { method: 'DELETE' })...
                    console.log("Item deleted");
                }
            });
        });
    }
});