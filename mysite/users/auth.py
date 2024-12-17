def CheckUserExists(username, email):
	userUsername = User.objects.filter(username=username)
	userEmail = User.objects.filter(email=email).first()

	if userUsername.exists() or userEmail:
		return True
	return False

def ValidadeUserInput(username, password):
	if username is None or password is None:
		return False
	return True
