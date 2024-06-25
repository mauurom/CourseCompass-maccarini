from django.db import models
from .usuario import Usuario

class Admin(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nombre_usuario = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.nombre_usuario} - Admin"
