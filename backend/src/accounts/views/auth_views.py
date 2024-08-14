from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from ..models.usuario import Usuario
from ..serializers.usuario_serializer import UsuarioSerializer
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Vista del inicio de sesión del usuario
class UserLoginView(APIView):
    def post(self, request):
        dni = request.data.get('dni')
        password = request.data.get('password')
        usuario = authenticate(request, username=dni, password=password)
        if usuario is not None:
            login(request, usuario)
            refresh = RefreshToken.for_user(usuario)
            redirect_url = 'change_password' if password == dni else 'campus'
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'redirect_url': redirect_url
            }, status=200)
        return JsonResponse({'error': 'Credenciales inválidas'}, status=401)

# Vista para nuevos usuarios 
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            usuario.set_password(request.data['password'])
            usuario.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Vista para manejar el cambio de contraseña
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            return JsonResponse({'message': 'Tu contraseña ha sido cambiada exitosamente!'}, status=200)
        else:
            return JsonResponse(form.errors, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

# Vista para el campus
@login_required
def campus_view(request):
    # Aquí podrías devolver datos relevantes para el campus
    return JsonResponse({'message': 'Bienvenido al campus'}, status=200)
