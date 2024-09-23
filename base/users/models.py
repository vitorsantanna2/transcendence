from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class User(AbstractBaseUser):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=200)
	username = models.CharField(max_length=150, unique=True)
	email = models.EmailField(max_length=200, unique=True)
	password = models.CharField(max_length=200)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["name", "email"]

	def __str__(self):
		return f"{self.name} - {self.username} - {self.email}"