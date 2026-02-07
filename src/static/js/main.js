document.addEventListener("DOMContentLoaded", async () => {
    const alerts = document.querySelectorAll(".alert");
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.style.transition = "opacity 0.5s ease";
                alert.style.opacity = "0";

                setTimeout(() => alert.remove(), 500);
            });
        }, 4000);
    }

    const currentPath = window.location.pathname;

    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active", "text-decoration-underline");
        }
    });
});