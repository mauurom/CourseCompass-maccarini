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

User = get_user_model()

class UserLoginView(APIView):
    def post(self, request):
        dni = request.data.get('dni')
        password = request.data.get('password')
        usuario = authenticate(request, username=dni, password=password)
        if usuario is not None:
            login(request, usuario)
            refresh = RefreshToken.for_user(usuario)
            if password == dni:
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'redirect_url': 'change_password'
                })
            else:
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'redirect_url': 'campus'
                })
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            usuario.set_password(request.data['password'])
            usuario.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para manejar el cambio de contraseña
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente!')
            return redirect('campus')
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

# Vista para el campus
@login_required
def campus_view(request):
    return render(request, 'accounts/campus.html')
