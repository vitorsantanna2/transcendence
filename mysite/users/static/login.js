async function handleLogin(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:8443/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            alert('Login realizado com sucesso!');
            window.location.href = data.redirect_url || '/home/';
        } else {
            const errorData = await response.json();
            alert(errorData.detail || 'Erro ao fazer login.');
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Erro ao fazer login.');
    }
}
