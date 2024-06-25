from django import forms
from .models import Tarea, Entrega

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_entrega']

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['archivo', 'comentario']
