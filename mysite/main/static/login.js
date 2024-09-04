document.addEventListener("DOMContentLoaded", () => {
    const botaoCriarConta = document.querySelector(".botao-criar-conta");
    const linkLogin = document.querySelector(".link-login");
    const loginPage = document.querySelector(".login-page");
    const botaoFazerLogin = document.querySelector(".botao-fazer-login");
    const telaPerfil = document.querySelector(".cover-container");
    const navBar = document.querySelector(".tab-lateral");
    const introPage = document.querySelector(".intro-page");

    botaoCriarConta.addEventListener("click", (event) => {
        event.preventDefault();
        introPage.style.display = "none";
        telaPerfil.style.display = "flex";
        navBar.style.display = "flex";

    });

    linkLogin.addEventListener("click", () => {
        introPage.style.display = "none";
        loginPage.style.display = "flex";
    })

    botaoFazerLogin.addEventListener("click", (event) => {
        event.preventDefault();
        loginPage.style.display = "none";
        telaPerfil.style.display = "flex";
        navBar.style.display = "flex";
    })
});