document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Impede o envio do formulário

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest", // Indica que é uma requisição AJAX
                },
            });

            if (response.ok) {
                // Se a resposta for OK (200-299)
                const data = await response.json(); // Espera que a resposta seja em JSON
                window.location.href = "/auth/login"; // Redireciona para o login
            } else {
                // Se a resposta não for OK (ex: erro 400, 500)
                const error = await response.text();
                alert(`Registration failed: ${error}`); // Exibe a mensagem de erro
            }
        } catch (error) {
            // Caso aconteça um erro de rede ou outro tipo de erro
            alert(`An error occurred: ${error.message}`);
        }
    });
});
