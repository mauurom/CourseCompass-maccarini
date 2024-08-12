from django.db import models
from .usuario import Usuario

#Modelo que representa a un administrador en el sistema
class Admin(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True) #Relación uno a uno con el modelo Usuario, se elimina en cascada si el Usuario se elimina
    nombre_usuario = models.CharField(max_length=30, unique=True) #Nombre de usuario único para el administrador, con un máximo de 30 caracteres

    # Método para representar el objeto como una cadena
    def __str__(self):
        return f"{self.nombre_usuario} - Admin"
