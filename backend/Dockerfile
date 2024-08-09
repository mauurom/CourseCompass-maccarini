# Usar una imagen base de Python
FROM python:3.10.12

# Establecer el directorio de trabajo en el contenedor
WORKDIR /CourseCompass

# Copiar el archivo requirements.txt y luego instalar las dependencias
COPY requirements.txt /CourseCompass/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . /CourseCompass/

# Establecer el directorio de trabajo donde está manage.py
WORKDIR /CourseCompass/src

# Ejecutar las migraciones y luego iniciar el servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
