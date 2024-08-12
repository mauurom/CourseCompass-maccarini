from django import forms
from .models import Tarea, Entrega

class TareaForm(forms.ModelForm):
    class Meta:
        # Define el modelo para el formulario y los campos que se incluyen
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_entrega']

class EntregaForm(forms.ModelForm):
    class Meta:
        # Define el modelo para el formulario y los campos que se incluyen
        model = Entrega
        fields = ['archivo', 'comentario']
