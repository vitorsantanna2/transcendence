
# Função para checar se o email já existe na base de dados

def CheckUserExists(username, email):
	userUsername = UserPong.objects.filter(username=username)
	userEmail = UserPong.objects.filter(email=email).first()

	if userUsername.exists() or userEmail:
		return True
	return False