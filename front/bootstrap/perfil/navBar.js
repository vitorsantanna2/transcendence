document.addEventListener("DOMContentLoaded", () => {
    const navItems = document.querySelectorAll(".nav-item");
    const pages = document.querySelectorAll(".pages");

    for (let i = 0; i < navItems.length; i++) {
        navItems[i].addEventListener("click", () => {
            console.log("navClicado: " + i);
            pages.forEach(page => {
                page.style.display = "none";
            });
            navItems.forEach(item => {
                item.classList.remove("active");
            });

            pages[i].style.display = "flex";
            navItems[i].classList.add("active");

        });
    }
});
