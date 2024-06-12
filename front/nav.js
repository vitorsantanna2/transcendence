const nav_links = document.querySelectorAll('.nav-link');

document.addEventListener("DOMContentLoaded", () => {
    nav_links.forEach(link => {
        link.addEventListener('click', () => {
            nav_links.forEach(nav_link => {
                nav_link.classList.remove('active', 'text-bg-secondary', 'text-bg-light');
            });
            link.classList.add('active', 'text-bg-light');
        });

    });
});