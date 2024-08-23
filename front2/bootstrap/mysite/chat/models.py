# Create your models here.

# chat/models.py

from django.db import models
from users.models import User  # Importa o modelo User do app users

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona a mensagem com o usuário
    content = models.TextField()  # Campo para armazenar o conteúdo da mensagem
    timestamp = models.DateTimeField(auto_now_add=True)  # Data e hora em que a mensagem foi criada

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'
