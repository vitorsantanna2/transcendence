from .models import UserPong

def CheckUserExists(username, email):
	userUsername = UserPong.objects.filter(username=username)
	userEmail = UserPong.objects.filter(email=email).first()

	if userUsername.exists() or userEmail:
		return True
	return False

def ValidateUserInput(username, password):
	if username is None or password is None:
		return False
	return True
