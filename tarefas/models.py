from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ListaTarefas(models.Model):
    nome = models.CharField(max_length=64)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_lista", null=True)
    descricao = models.TextField(max_length=300)
    realizada = models.BooleanField(null=True)


    def __str__(self) -> str:
        return self.nome
