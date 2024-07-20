document.addEventListener("DOMContentLoaded", () => {
    const botaoLogin = document.querySelector(".botao-criar-conta");
    const telaPerfil = document.querySelector(".cover-container");
    const navBar = document.querySelector(".tab-lateral");
    const introPage = document.querySelector(".intro-page");

    botaoLogin.addEventListener("click", (event) => {
        event.preventDefault();
        introPage.style.display = "none";
        telaPerfil.style.display = "flex";
        navBar.style.display = "flex";

    });
});