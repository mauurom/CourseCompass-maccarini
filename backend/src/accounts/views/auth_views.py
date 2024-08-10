from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from ..models.usuario import Usuario
from ..serializers.usuario_serializer import UsuarioSerializer

User = get_user_model() #Obtiene el modelo del usuario personalizado 

#Vista del inicio de sesion del usuario
class UserLoginView(APIView):
    def post(self, request):
        dni = request.data.get('dni')               #Autentica al usuario con el DNI
        password = request.data.get('password')     #Autentica al usuario con la contraseña
        usuario = authenticate(request, username=dni, password=password)
        if usuario is not None:                     #Inicia sesion al usuario
            login(request, usuario)
            refresh = RefreshToken.for_user(usuario)
            if password == dni:
                return Response({                   #Redirige a cambiar la contraseña si es identica al DNI
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'redirect_url': 'change_password'
                })
            else:
                return Response({                   #Redirige al campus si DNI es diferente de contraseña
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'redirect_url': 'campus'
                })
        #Devuelve error si los datos de las credenciales son erroneos
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

#Vista para nuevos usuarios 
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():             #Guarda nuevo usuario
            usuario = serializer.save()       #Establece la contraseña
            usuario.set_password(request.data['password'])
            usuario.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) #Devuelve los datos del usuario creado
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #Devuelve error de validacion 


# Vista para manejar el cambio de contraseña
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():                   #Guarda la nueva contraseña
            user = form.save()                #Mensaje de contraseña guardada exitosamente
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente!')
            return redirect('campus')         #Redirige al campus
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        form = PasswordChangeForm(request.user) #Muestra si hay posibles errores
    return render(request, 'accounts/change_password.html', {'form': form}) #Renderiza el formulario de cambio de contraseña

# Vista para el campus
@login_required
def campus_view(request):                    #Renderiza la pagina del campus 
    return render(request, 'accounts/campus.html')
