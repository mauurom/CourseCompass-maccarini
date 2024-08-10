import csv
import os
import sys
import django

#Agrega el directorio acual al path de busqueda de modulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#Configura el modulo de ajustes de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CourseCompass.settings')
#Configura Django
django.setup()

from accounts.models.usuario import Usuario

def load_data():
    with open('accounts/data/alumnos.csv', newline='') as csvfile: #Abre el archivo CSV con los datos del alumnos
        reader = csv.DictReader(csvfile)
        for row in reader:
            Usuario.objects.create_user(                           # Crea un usuario con los datos del CSV
                dni=row['dni'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                fecha_nacimiento=row['fecha_nacimiento'],
                correo=row['correo'],
                password=row['dni']                                #Usar DNI como contraseña por defecto
            )
    print("Datos de los alumnos cargados correctamente.")

#Ejecuta la funcion load_data si el scrip se ejecuta directamente
if __name__ == "__main__":
    load_data()
