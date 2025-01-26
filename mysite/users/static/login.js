// login.js

async function handleLogin(event) {
    event.preventDefault(); // Prevent the default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        // Step 1: Send login credentials to the LoginView API
        const loginResponse = await fetch('http://localhost:8443/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Ensure CSRF token is included if required
            },
            body: JSON.stringify({ 
                username: email, // Assuming 'username' is the email. Adjust if different.
                password: password 
            }),
            credentials: 'include' // Include cookies if needed
        });

        const loginData = await loginResponse.json();

        if (loginResponse.ok) {
            // Step 2: 2FA code sent successfully. Prompt the user for the code.
            const userId = loginData.user_id;
            const userMessage = loginData.message || '2FA code sent to your phone.';
            alert(userMessage);
            
            const twoFACode = prompt('Por favor, insira o código 2FA enviado para o seu telefone:');
            
            if (twoFACode) {
                // Step 3: Verify the 2FA code
                const verifyResponse = await fetch('http://localhost:8443/auth/two-factor-auth/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken() // Ensure CSRF token is included if required
                    },
                    body: JSON.stringify({
                        user_id: userId,
                        code: twoFACode
                    }),
                    credentials: 'include' // Include cookies if needed
                });

                const verifyData = await verifyResponse.json();

                if (verifyResponse.ok) {
                    // Step 4: 2FA verification successful. Store JWT tokens and redirect.
                    const accessToken = verifyData.access;
                    const refreshToken = verifyData.refresh;

                    // Store tokens securely. Consider using HTTP-Only cookies for enhanced security.
                    localStorage.setItem('access_token', accessToken);
                    localStorage.setItem('refresh_token', refreshToken);

                    alert('Login realizado com sucesso!');
                    window.location.href = '/home/'; // Adjust the redirect URL as needed
                } else {
                    // Handle 2FA verification errors
                    alert(verifyData.error || 'Código 2FA inválido.');
                }
            } else {
                alert('Código 2FA é obrigatório para continuar.');
            }
        } else {
            // Handle login errors
            alert(loginData.error || 'Erro ao fazer login.');
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Ocorreu um erro ao tentar fazer login. Por favor, tente novamente mais tarde.');
    }
}

// Function to retrieve CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
