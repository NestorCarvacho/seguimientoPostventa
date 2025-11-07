import csv
from django.contrib.auth.models import User

def cargar_usuarios_desde_csv(ruta_csv):
    """
    Carga usuarios desde un archivo CSV.
    El archivo debe tener las columnas: username, first_name, last_name, email.
    """
    with open(ruta_csv, newline='', encoding='utf-8') as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            username = fila['username']
            password = fila['username']  # La contraseña inicial es el mismo RUT
            first_name = fila.get('first_name', '')
            last_name = fila.get('last_name', '')
            email = fila.get('email', '')

            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                print(f"Usuario {username} creado exitosamente.")
            else:
                print(f"El usuario {username} ya existe.")

# Ejemplo de uso:
# cargar_usuarios_desde_csv('ruta_al_archivo.csv')