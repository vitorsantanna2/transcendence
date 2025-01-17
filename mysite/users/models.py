from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import bcrypt
# Create your models here.

class UserPong(AbstractBaseUser):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=200)
	username = models.CharField(max_length=150, unique=True)
	email = models.EmailField(max_length=200, unique=True)
	password = models.CharField(max_length=200)
	phoneNumber = models.CharField(max_length=14, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	

	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["name", "email"]

	def __str__(self):
		return f"{self.name} - {self.username} - {self.email}"

	def save(self, *args, **kwargs):
		self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
		super(UserPong, self).save(*args, **kwargs)
