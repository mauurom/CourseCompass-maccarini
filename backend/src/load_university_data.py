import csv
import os
import sys
import django

# Configurar el entorno de Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CourseCompass.settings')
django.setup()

from accounts.models.usuario import Usuario

def load_data():
    with open('accounts/data/alumnos.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Usuario.objects.create_user(
                dni=row['dni'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                fecha_nacimiento=row['fecha_nacimiento'],
                correo=row['correo'],
                password=row['dni']  # Usar DNI como contraseña por defecto
            )
    print("Datos de los alumnos cargados correctamente.")

if __name__ == "__main__":
    load_data()
