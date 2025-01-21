from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import bcrypt

class UserManager(BaseUserManager):
    def create_user(self, username, email, name, password=None, auth_method='site', **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            auth_method=auth_method,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, email, name, password, **extra_fields)

class UserPong(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    phoneNumber = models.CharField(max_length=14, blank=True, null=True)
    auth_method = models.CharField(
        max_length=10,
        choices=[
            ('site', 'Site Registration'),
            ('oauth', '42 API'),
        ],
        default='site',
    )
    oauth_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "email"]

    objects = UserManager()

    def __str__(self):
        return f"{self.name} - {self.username} - {self.email}"

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())

