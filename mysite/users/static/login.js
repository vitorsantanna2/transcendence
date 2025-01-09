document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const usernameInput = document.querySelector("#user");
    const passwordInput = document.querySelector("#pass");

    form.addEventListener("submit", (event) => {
        event.preventDefault(); // Impede o envio tradicional do formulário

        const username = usernameInput.value;
        const password = passwordInput.value;

        fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
        })
        .then((response) => {
            if (response.ok) {
                return response.json(); // Extrai o JSON da resposta
            } else {
                return response.json().then((data) => {
                    throw new Error(data.error || "An unknown error occurred.");
                });
            }
        })
        .then((data) => {
            window.location.href = "/auth/twofa"; // Redireciona para 2FA
        })
        .catch((error) => {
            alert(`Login failed: ${error.message}`); // Mostra mensagens de erro
        });
    });
});
