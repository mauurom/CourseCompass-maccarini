from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models.usuario import Usuario
from .models.alumno import Alumno
from .models.profesor import Profesor
from .models.admin import Admin

# Formularios personalizados para crear y cambiar usuarios
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('dni', 'nombre', 'apellido', 'correo', 'fecha_nacimiento')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('dni', 'nombre', 'apellido', 'correo', 'fecha_nacimiento')

# Clase para administrar el modelo de Usuario en el panel de administración
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('dni', 'nombre', 'apellido', 'correo', 'tipo_usuario', 'is_admin')
    list_filter = ('is_admin', 'tipo_usuario')
    fieldsets = (
        (None, {'fields': ('dni', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'apellido', 'correo', 'fecha_nacimiento')}),
        ('Permisos', {'fields': ('is_admin', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('dni', 'password1', 'password2')}),
        ('Información Personal', {'fields': ('nombre', 'apellido', 'correo', 'fecha_nacimiento')}),
    )
    search_fields = ('dni', 'nombre', 'apellido', 'correo')
    ordering = ('dni',)
    filter_horizontal = ()

# Registrar los modelos y el administrador personalizado en el panel de administración
admin.site.register(Usuario, UserAdmin)
admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(Admin)
