from django.contrib import admin
from django.urls import path, include

#Definiciones de rutas principales
urlpatterns = [
    path('admin/', admin.site.urls),                #Ruta para la interfaz de administracion
    path('accounts/', include('accounts.urls')),    #Incluye la ruta de la app accounts 
    path('cursos/', include('cursos.urls')),        #Incluye la ruta de la app course
]
