import requests

# Substitua pelos valores do seu aplicativo
CLIENT_ID = "u-s4t2ud-4c3014502f1eea041c31ac5305fc8718df34d94f58b564ab5b7019fcbf0beacf"
CLIENT_SECRET = "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"

# URL para obter o token
TOKEN_URL = "https://api.intra.42.fr/oauth/token"

TOKEN_ACESS = "856682493726ce54dcdbc442d09a228e1ef496cba73de09927f9981e2bed55ce"

# Parâmetros da requisição
payload = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
}

# Fazendo a requisição para obter o token
response = requests.post(TOKEN_URL, data=payload)

if response.status_code == 200:
    access_token = response.json().get('access_token')
    print(f"Access Token: {access_token}")
else:
    print(f"Erro ao obter o token: {response.status_code}")
    print(response.json())


# Exemplo: obter informações do usuário logado
USER_URL = "https://api.intra.42.fr/v2/cursus/42/users/"
headers = {
    'Authorization': f'Bearer {access_token}',
}

try:
	user_response = requests.get(USER_URL, headers=headers)
	print(user_response.json())
except e:
    print(e)

if user_response.status_code == 200:
    user_data = user_response.json()
    print("Dados do Usuário:", user_data)
else:
    print("Erro ao obter os dados do usuário:", user_response.status_code)
# 